---
name: master-builder
description: >
  End-to-end workflow for creating a data-driven master in Motley.
  Guides through cube research, outline planning, master creation,
  slide layout selection, content configuration, and final review.
  Use when asked to create a master, build a deck, or make a presentation.
---

# Master Builder

End-to-end workflow for creating a data-driven master (parametrized slide deck template) in Motley.

## Overview

A **master** is a parametrized slide deck template. It accepts parameters (customer_name, start_date, end_date) and resolves into a fully data-driven presentation. Blocks within slides reference data queries, other blocks, and context variables to produce dynamic content.

The master-building workflow has 6 phases:

1. **Research & Plan** — explore data and layouts, write outline
2. **User Approval** — present outline for feedback
3. **Create Master** — initialize from layout library
4. **Understand the Master** — inspect slides and elements
5. **Build Each Slide** — configure content for each outlined slide
6. **Final Review** — verify everything looks correct

---

## Phase 1: Research & Plan

Enter plan mode. Research the available data and layouts to design the deck.

### 1a. Explore Cubes

Understand what data is available:

```
cubes_summary()
```

Then inspect relevant cubes to see measures, dimensions, and sample data:

```
inspect_cube(cube_name="revenue", num_rows=3)
inspect_cube(cube_name="customers", num_rows=3)
```

If the existing cubes don't have the data you need, you can create custom cubes from SQL (`create_cube`), add computed measures to existing cubes (`add_measures`), or add computed dimensions (`add_dimensions`). See the `explore-cube` skill for details.

### 1b. Explore Layout Library

See what slide layouts are available:

```
list_layout_libraries()
```

Inspect the structure of the target layout library:

```
inspect_layout_library(layout_library_id=<id>)
```

Visually inspect layouts using thumbnails:

```
get_thumbnails(master_props_id=<layout_library_id>, layout_names=["Cover", "KPI Dashboard", "Chart Slide", ...])
```

For each layout, document:
- Layout name
- Element names and types (chart, text, table)
- Visual arrangement (from thumbnails)

### 1c. Write Slide-by-Slide Outline

For each planned slide, specify:
- **Purpose**: What story does this slide tell?
- **Layout**: Which layout to use (from the library)
- **Blocks**: For each element, what content goes there:
  - Chart blocks: what chart type, measure, dimension, time range
  - Text blocks: what template, which queries needed
  - Table blocks: what data, shape, formatting

Keep the outline in the plan mode conversation — no need to use the outline MCP tools.

---

## Phase 2: User Approval

Present the outline to the user. Incorporate feedback before proceeding.

---

## Phase 3: Create Master

Initialize a master from the layout library:

```
create_master(
    layout_library_id=<id>,
    name="<descriptive name>",
    source_id=<source_id>
)
```

- `source_id` is optional — if provided, the master's `sample_parameters` (start_date, end_date, client_name) are derived from the source's default filters
- All slides start **hidden**
- Record the returned `master_id` for all subsequent operations

---

## Phase 4: Understand the Master

Get the full structure of the master:

```
get_master_summary(master_id=<id>)
```

This returns all slides with their block names and types. For each slide, note:
- Slide name
- Block names and types (chart, text, table, numerical_query)
- Which blocks correspond to which visual elements

Optionally get thumbnails to see the visual appearance:

```
get_thumbnails(master_props_id=<master_id>, layout_names=["Layout1", "Layout2", ...])
```

---

## Phase 5: Build Each Slide

For each slide in your outline:

### Step 1: Pick Layout

Among the hidden slides in the master, find the one whose element structure best matches the content you need. Consider:
- Number and types of elements (charts, text, tables)
- Visual layout from thumbnails
- Element sizes and positions

**Important**: A layout library is purely a visual template — it defines element positions, sizes, and types, nothing more. Any existing text, chart data, or table content in the layout's elements is placeholder content and must be ignored entirely. Do NOT let placeholder content influence what you put into the blocks. The only guidance for block content comes from the user's requirements and the outline you built in Phase 1.

### Step 2: Duplicate the Layout

```
copy_slide(
    master_id=<id>,
    slide_name="<hidden_layout_name>",
    new_slide_name="<descriptive_slide_name>",
    position=<N>,
    element_descriptions=[
        {"name": "element1", "description": "Purpose of this element"},
        {"name": "element2", "description": "Purpose of this element"}
    ],
    description="Overall slide purpose"
)
```

The copy is automatically **unhidden**. The `element_descriptions` help the query/chart LLMs understand the context.

### Step 3: Configure Blocks

For each block in the slide, use the appropriate tool:

#### Chart Blocks

```
update_chart_block(
    master_id=<id>,
    slide_name="<slide>",
    block_name="<chart_block>",
    prompt="<detailed chart description>",
    cube_name="<cube>"
)
```

Then verify:

```
render_chart(
    master_id=<id>,
    slide_name="<slide>",
    block_name="<chart_block>"
)
```

See the `update-chart` skill for writing effective chart prompts.

#### Text Blocks

First create query blocks for the data:

```
update_query_block(
    master_id=<id>,
    slide_name="<slide>",
    parent_block="<text_block>",
    query_name="<name>",
    prompt="<what data to fetch>",
    cube_name="<cube>"
)
```

Then set the template:

```
update_text_block(
    master_id=<id>,
    slide_name="<slide>",
    block_name="<text_block>",
    user_prompt="<template with {variables}>",
    call_llm=<true/false>
)
```

Text blocks resolve immediately — check the returned content. See the `update-text-block` skill.

#### Table Blocks

Same pattern as text — create query blocks first, then set the template:

```
update_query_block(
    master_id=<id>,
    slide_name="<slide>",
    parent_block="<table_block>",
    query_name="<name>",
    prompt="<what data to fetch>",
    mode="table",
    cube_name="<cube>"
)

update_table_block(
    master_id=<id>,
    slide_name="<slide>",
    block_name="<table_block>",
    user_prompt="{<query_name>}",
    target_shape=[<rows>, <cols>]
)
```

See the `update-table-block` skill.

### Step 4: Verify

- **Text/table blocks**: Resolve inline — check the returned content in the tool response
- **Chart blocks**: Call `render_chart` to see the rendered PNG
- **Overflow errors**: If content exceeds element size, adjust the content (shorten text, reduce table rows, etc.)

---

## Phase 6: Final Review

### Resolve All Blocks

```
resolve_master(master_id=<id>)
```

This resolves any remaining out-of-date blocks (mainly charts that haven't been individually rendered).

### Visual Verification

Get thumbnails of all visible slides:

```
get_thumbnails(master_props_id=<master_id>, layout_names=["Slide1", "Slide2", ...])
```

Check:
- All slides have content (no empty blocks)
- Charts look correct
- Text is readable (no overflow)
- Narrative flow matches the outline

---

## Key Conventions

### Resolution Behavior
- **Charts** resolve lazily — they're not resolved until you call `render_chart` or `resolve_master`
- **Text/table blocks** resolve eagerly — they're resolved immediately when you call `update_text_block`/`update_table_block`

### Variable Syntax
- `{var}` for same-slide queries and context variables
- `{Slide::Block}` for cross-slide references
- See the `update-text-block` skill for full syntax

### References Must Exist Before Use
**Critical rule**: Every `{variable}` or `{Slide::Block}` reference in a template must point to something that already exists at the time you call `update_text_block` or `update_table_block`. Concretely:
- **Query references** (`{query_name}`): call `update_query_block` to create the query BEFORE calling `update_text_block`/`update_table_block` with a template that references it
- **Cross-slide references** (`{Slide::Block}`): the referenced slide and block must already have content (i.e., be configured and resolved) before the referencing template is set
- **Context variables** (`{customer_name}`, `{end_month}`, etc.): these are always available — no prior setup needed
- **Chart data references** (`{chart_block_name}`): the chart block must exist on the slide (it does not need to be resolved yet — the reference will resolve lazily)

If a reference points to something that doesn't exist, resolution will fail.

### Query → Template Workflow
- Query blocks feed text/table blocks: create queries first, then reference as `{query_name}`
- The `query_name` in `update_query_block` must match the `{variable}` in the parent's `user_prompt`

### Content Overflow
- The tool returns an error if text/table content exceeds the element's physical size on the slide
- Fix by shortening content, reducing data, or using LLM with brevity instructions

### Limitations
- There is no `update_master` tool — master-level properties (name, sample_parameters) can only be set during `create_master`
- There is no `delete_query_block` tool — to remove a query, update the parent block's template to not reference it

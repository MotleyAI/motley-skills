---
name: create-report
description: >
  Create a report using Motley.

---

# Create Report

End-to-end workflow for creating a data-driven report using Motley.

## Overview

Motley helps to create reports based on the user's data and requirements.

A **report** in Motley is first created as a document consisting of blocks (markdown text, tables, and charts).
Blocks can reference data queries, other blocks, and context variables.

The deck creation workflow has 4 phases:

1. **Research & Plan** — understand the user's needs & the relevant data
2. **Creating a document in Motley** – based on the research, write the report content into a document
3. **User Approval** — render the report to the user, ask for approval
4. **Output** – on user request, export the report to the user's preferred format

---

## Phase 1: Research & Plan

Enter plan mode.

Make sure you understand **why** the user wants to create this report, **what** exactly they want to show.

### Explore Cubes

Data is central to the report generation. It can be used both for charts and inline queries
embedded in the text.

The purpose of this step is to find the relevant data for the queries and charts that should be in the report.
Data is represented as cubes (data models), containing measures and dimensions, that can be queried.

Understand what cubes are available:

```
cubes_summary()
```

Then inspect relevant cubes to see measures, dimensions, and sample data:

```
inspect_cube(cube_name="revenue", num_rows=3)
inspect_cube(cube_name="customers", num_rows=3)
```

If the existing cubes don't have the data you need, you can create custom cubes from SQL (`create_cube`), add computed measures to existing cubes (`add_measures`), or add computed dimensions (`add_dimensions`). See the `explore-cube` skill for details.

### Ask questions

Until it's completely clear what the user wants, ask them questions.

If it's unclear from where the data should come, ask them to point exactly.

If anything about the data is ambiguous, ask them for clarification, also listing the possible options.

---

## Phase 2: Create a document in Motley

A document is a flat sequence of text (Markdown) blocks, table blocks, and charts.
Text and table blocks can reference queries.

To create a document, use the `create_document` tool:

```
create_document(
    name="<descriptive name>",
    source_id=<source_id>
)
```

You need to provide the `source_id` of the cubes you are going to use. Currently, all the cubes in a document must
come from a single source. The `source_id` can be found in outputs of `cubes_summary` and `inspect_cube` tools.

### Set Context Variables

Documents have context variables (e.g. `client_name`, `start_date`, `end_date`) that are used during block resolution. When a query filter references a variable like `{client_name}`, it is substituted from the document's context variables at resolution time.

Default values are derived from `source_id` at document creation. To check current values:

```
get_doc_variables(doc_id=<id>)
```

To update them (e.g. to change the client or date range for the report):

```
set_doc_variables(
    doc_id=<id>,
    variables={"client_name": "Acme Corp", "start_date": "2025-01-01", "end_date": "2025-12-31"}
)
```

This merges the provided values with existing parameters and re-resolves all blocks. Only provide the keys you want to change.

### Create Blocks

Creating blocks and updating them is done using the tools:

- `update_text_block`
- `update_table_block`
- `update_chart_block`
- `update_query_block`

Each block must have a unique name by which it can be referenced.
To create a new block provide a new, unique name.

#### Chart Blocks

```
update_chart_block(
    location={doc_id: <id>, slide_name: "<slide>", block_name: "<chart_block>"},
    prompt="<detailed chart description>",
    cube_name="<cube>"
)
```

Then verify:

```
render_chart(
    location={doc_id: <id>, slide_name: "<slide>", block_name: "<chart_block>"}
)
```

See the `update-chart` skill for writing effective chart prompts.

#### Text Blocks

First create query blocks for the data:

```
update_query_block(
    location={doc_id: <id>, slide_name: "<slide>", parent_block: "<text_block>"},
    query_name="<name>",
    prompt="<what data to fetch>",
    cube_name="<cube>"
)
```

Then set the template:

```
update_text_block(
    location={doc_id: <id>, slide_name: "<slide>", block_name: "<text_block>"},
    user_prompt="<template with {variables}>",
    call_llm=<true/false>
)
```

Verify the text block by checking the returned content. See the `update-text-block` skill.

#### Table Blocks

Same pattern as text — create query blocks first, then set the template:

```
update_query_block(
    location={doc_id: <id>, slide_name: "<slide>", parent_block: "<table_block>"},
    query_name="<name>",
    prompt="<what data to fetch>",
    mode="table",
    cube_name="<cube>"
)

update_table_block(
    location={doc_id: <id>, slide_name: "<slide>", block_name: "<table_block>"},
    user_prompt="{<query_name>}",
    target_shape=[<rows>, <cols>]
)
```

See the `update-table-block` skill.

---

## Phase 3: User Approval

### Export as Markdown and review

Export the document to markdown format:

```
export_markdown(doc_id=<id>)
```

Check the output carefully. Does it look as expected? If not, go back and update the blocks.


### Render for the user

Show the user the rendered document using the frontend-slides skill. Ask for approval.

If the user is happy with the document, proceed to the next phase.

If not, understand the user's feedback and go back and update the blocks.

---

## Phase 4: Output

On user request, export the report to the user's preferred format.

If you need the data for the charts instead of images (say, for creating an HTML with a charting library), use

```
export_markdown(doc_id=<id>, mode="table")
```

This will embed the data for the charts as markdown tables, with chart metadata next to them. 
Again, use the frontend-slides skill to generate slides as needed.

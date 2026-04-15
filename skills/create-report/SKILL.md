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

### Explore Models

Data is central to the report generation. It can be used both for charts and inline queries
embedded in the text.

The purpose of this step is to find the relevant data for the queries and charts that should be in the report.
Data is represented as models (data models), containing measures and dimensions, that can be queried.

Understand what models are available:

```
models_summary()
```

Then inspect relevant models to see measures, dimensions, and sample data:

```
inspect_model(model_name="revenue", num_rows=3)
inspect_model(model_name="customers", num_rows=3)
```

If the existing models don't have the data you need, you can create custom models from SQL (`create_model`), or add computed measures/dimensions to existing models (`edit_model`). See the `explore-model` skill for details.

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

You need to provide the `source_id` of the models you are going to use. Currently, all the models in a document must
come from a single source. The `source_id` can be found in outputs of `models_summary` and `inspect_model` tools.

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

**IMPORTANT: NEVER call `update_text_block`, `update_table_block`, `update_chart_block`, or `update_query_block` directly.** Always delegate block creation and modification to the **block-modifier** sub-agent.

The only exception is `render_chart`, which is read-only and can be called directly to visually verify chart output.

#### Delegating to block-modifier

For each block you need to create or modify, launch the `block-modifier` sub-agent with clear instructions:

- The **doc_id**, **slide_name**, and **block_name** (via parent_location for queries)
- The **block type** (text, table, chart, or query)
- The **full content/configuration** for the block (template text, query parameters, chart configuration, etc.)
- Any relevant context (model names, variable names, etc.)

You can delegate multiple independent blocks in a single message by launching multiple sub-agents in parallel.

#### Chart Blocks

Delegate to block-modifier with:
- Block type: chart
- Location: `{doc_id: <id>, slide_name: "<slide>", block_name: "<chart_block>"}`
- Query configuration (measures, dimensions, time_dimension, filters, etc.)
- Chart details (chart type, axis labels, series config, etc.)
- Model name

After the sub-agent completes, verify the chart visually:

```
render_chart(
    location={doc_id: <id>, slide_name: "<slide>", block_name: "<chart_block>"}
)
```

See the `update-chart` skill for chart type guidance and configuration patterns.

#### Text Blocks

Delegate to block-modifier with:
1. First, the **query blocks** the text needs (type: query, with query_name, query config, mode, model context)
2. Then, the **text block** itself (type: text, with user_prompt template referencing `{query_name}` variables)

See the `update-text-block` skill for template syntax and modes.

#### Table Blocks

Same pattern as text — delegate query blocks first, then the table block:
1. Query blocks (type: query, mode="table" for multi-row data)
2. Table block (type: table, with user_prompt and target_shape)

See the `update-table-block` skill for table patterns.

---

## Phase 3: User Approval

### Export as Markdown and review

Export the document to markdown format:

```
export_document(document_id=<id>, format="markdown")
```

Check the output carefully. Does it look as expected? If not, delegate block updates to block-modifier.


### Render for the user

Show the user the rendered document as markdown. Ask for approval.

If the user is happy with the document, proceed to the next phase.

If not, understand the user's feedback and delegate corrections to block-modifier.

---

## Phase 4: Output

Use the make-slides skill to generate slides from the document you just created.
The make-slides skill will call `save_deck` to persist the deck and `export_document` to render it as HTML or PDF.

On user request, export the report to the user's preferred format.

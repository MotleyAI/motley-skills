# MCP Tools Reference

Comprehensive reference for all 20 tools available via the Motley MCP server.

## Overview

The MCP server provides tools for building data-driven reports programmatically. Tools are organized into four categories based on the resources they operate on.

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| [Cube](tools/cube.md) | 6 | Cube management and schema modification |
| [Element](tools/element.md) | 5 | Content block updates (text, table, chart, query) |
| Document | 8 | Document operations, inspection, and variables |
| Export | 1 | PDF export |

## Quick Reference

### Cube Tools

| Tool | Description |
|------|-------------|
| [`cubes_summary`](tools/cube.md#cubes_summary) | List all cubes with schemas |
| [`inspect_cube`](tools/cube.md#inspect_cube) | Get cube details with sample data |
| [`create_cube`](tools/cube.md#create_cube) | Create cube from SQL query |
| [`add_measures`](tools/cube.md#add_measures) | Add custom measures to cube |
| [`add_dimensions`](tools/cube.md#add_dimensions) | Add custom dimensions to cube |
| [`delete_measures_dimensions`](tools/cube.md#delete_measures_dimensions) | Remove measures/dimensions |

### Element Tools

| Tool | Description |
|------|-------------|
| [`update_text_block`](tools/element.md#update_text_block) | Set text template and resolve |
| [`update_table_block`](tools/element.md#update_table_block) | Set table template and resolve |
| [`update_chart_block`](tools/element.md#update_chart_block) | Update chart with structured query and chart details |
| [`update_query_block`](tools/element.md#update_query_block) | Create/update query with structured query |
| [`render_chart`](tools/element.md#render_chart) | Render chart to base64 PNG image |

### Document Tools

| Tool | Description |
|------|-------------|
| `create_document` | Create a new document with a data source |
| `export_markdown` | Export document as markdown (image or table mode) |
| `get_doc_summary` | Get document outline with slides and blocks |
| `get_doc_variables` | Get all variables and context for a document |
| `set_doc_variables` | Set document context variables (merges with existing) |
| `inspect_slide` | Get full slide content |
| `inspect_block` | Get specific block configuration and content |
| `move_block` | Move a block to a new position within the document |

### Export Tools

| Tool | Description |
|------|-------------|
| `html_to_pdf` | Convert self-contained HTML to PDF |

## Typical Workflow

### 1. Discover Available Data

```
cubes_summary()              → List available cubes
inspect_cube(cube_name="sales_data", num_rows=3)
                             → Schema and sample data
```

### 2. Create a Document

```
create_document(name="Q1 Report", source_id=1)
  → Returns doc_id

get_doc_summary(doc_id=42)
  → See slides and blocks

get_doc_variables(doc_id=42)
  → Check context variables

set_doc_variables(doc_id=42, variables={"client_name": "Acme"})
  → Update context
```

### 3. Create Content Blocks

```
update_query_block(
    location={doc_id: 42, slide_name: "Revenue", parent_block: "metrics"},
    query_name="total_revenue",
    query={measures: [{name: "total_revenue", cube_name: "sales"}]}
)

update_text_block(
    location={doc_id: 42, slide_name: "Revenue", block_name: "metrics"},
    user_prompt="Revenue: {currency(total_revenue)}"
)
```

### 4. Add Charts

```
update_chart_block(
    location={doc_id: 42, slide_name: "Revenue", block_name: "chart"},
    query={...},
    chart_details={...}
)

render_chart(
    location={doc_id: 42, slide_name: "Revenue", block_name: "chart"}
)
  → Verify rendered image
```

### 5. Export

```
export_markdown(doc_id=42)
  → Markdown with chart images

export_markdown(doc_id=42, mode="table")
  → Markdown with chart data as tables

html_to_pdf(html_content="<html>...</html>")
  → PDF output
```

## Error Handling

All tools return structured responses. On failure:

- `success: false` is returned (where applicable)
- `error` field contains the error message
- Common errors:
  - "Document not found or access denied"
  - "Slide 'X' not found in document Y"
  - "Block 'X' not found in slide 'Y'"
  - "Resolution failed: ..."

## See Also

- [Setup Guide](setup.md) — Installation and configuration
- [Skills Reference](skills.md) — Domain knowledge for queries, charts, text, and tables
- [Bundle Overview](README.md) — MCP bundle features and architecture

# MCP Tools Reference

Comprehensive reference for all tools available via the Motley MCP server.

## Overview

The MCP server provides tools for building data-driven reports programmatically. Tools are organized into four categories based on the resources they operate on.

## Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| [Model](tools/model.md) | 4 | Model management and schema modification |
| [Element](tools/element.md) | 5 | Content block updates (text, table, chart, query) |
| [Document](tools/document.md) | 7 | Document operations, inspection, and variables |
| Deck | 3 | Persist DeckSpec, render to HTML/PDF, list layouts |
| Export | 2 | PDF export, HTML save |

## Quick Reference

### Model Tools

| Tool | Description |
|------|-------------|
| [`models_summary`](tools/model.md#models_summary) | List all models with schemas |
| [`inspect_model`](tools/model.md#inspect_model) | Get model details with sample data |
| [`create_model`](tools/model.md#create_model) | Create model from SQL query |
| [`edit_model`](tools/model.md#edit_model) | Add/delete measures and dimensions |

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
| [`create_document`](tools/document.md#create_document) | Create a new document with a data source |
| [`inspect_document`](tools/document.md#inspect_document) | Inspect a document, slide, or block (doc outline / slide content / block detail) |
| [`get_doc_variables`](tools/document.md#get_doc_variables) | Get all variables and context for a document |
| [`set_doc_variables`](tools/document.md#set_doc_variables) | Set document context variables (merges with existing) |
| [`move_block`](tools/document.md#move_block) | Move a block to a new position within the document |

### Deck Tools

| Tool | Description |
|------|-------------|
| `save_deck` | Persist a DeckSpec to the database, copying referenced blocks from a source document and resolving them. Returns a `document_id`. |
| `export_document` | Export a saved document to HTML, PDF, or markdown. |
| `read_layouts` | List available slide layouts for a brand style. |

## Typical Workflow

### 1. Discover Available Data

```
list_resources(what="datasources") → List available datasources
models_summary()             → List available models
inspect_model(model_name="sales_data", num_rows=3)
                             → Schema and sample data
```

### 2. Create a Document

```
create_document(name="Q1 Report", source_id=1)
  → Returns doc_id

inspect_document(doc_id=42)
  → See slides and blocks

get_doc_variables(doc_id=42)
  → Check context variables

set_doc_variables(doc_id=42, variables={"client_name": "Acme"})
  → Update context
```

### 3. Create Content Blocks

```
update_query_block(
    parent_location={doc_id: 42, slide_name: "Revenue", block_name: "metrics"},
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
export_document(document_id=42, format="markdown")
  → Markdown with chart images

export_document(document_id=42, format="markdown", mode="table")
  → Markdown with chart data as tables

```

### 6. Create a Branded Deck (DeckSpec workflow)

```
list_resources(what="styles")       → Available brand styles
list_resources(what="datasources")  → Available datasources
read_layouts(style_name="Cledara")
                             → Layout catalog for the brand

save_deck(
    deck_spec={...},
    style_name="Cledara",
    source_document_id=42,
    title="Q1 Report"
)
  → Persists deck, copies blocks from source, resolves them
  → Returns {document_id: 99}

export_document(document_id=99, format="html")
  → Rendered HTML URL

export_document(document_id=99, format="pdf")
  → Rendered PDF URL
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

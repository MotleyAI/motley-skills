# Motley MCP Bundle

An MCP (Model Context Protocol) bundle that connects Claude to the Motley data storytelling platform, enabling AI-powered data visualization and report generation.

## Overview

This bundle provides a passthrough MCP server that forwards requests to a remote Motley backend. It allows Claude (via Claude Desktop or other MCP clients) to:

- Query data from your semantic layer
- Create and modify chart configurations
- Generate text and table content blocks
- Build complete data-driven reports

## Features

- **Semantic Layer Queries**: Access your data through a unified semantic layer with measures, dimensions, and filters
- **Chart Generation**: Create bar charts, line charts, pie charts, and funnels with structured configuration
- **Text Templates**: Generate data-driven text with variable substitution and optional LLM enhancement
- **Table Blocks**: Create formatted tables with pivoting and flexible layouts
- **Time Intelligence**: Built-in support for time filters, period comparisons, and date range calculations

## Quick Start

1. **Install the bundle** in Claude Desktop or your MCP client

2. **Configure** with your Motley API credentials:
   - `api_url`: Your Motley MCP endpoint (e.g., `https://your-instance.com/api/v1/mcp/`)
   - `api_key`: Your API key (starts with `sk_`)

3. **Start using** the Motley tools through Claude

See [setup.md](setup.md) for detailed installation instructions.

## Available Tools

The Motley MCP server provides 18 tools organized into four categories:

| Category | Tools | Description |
|----------|-------|-------------|
| **Model** | 4 | Data modeling and schema management |
| **Element** | 5 | Content blocks (text, table, chart, query, render) |
| **Document** | 8 | Document operations, inspection, and variables |
| **Export** | 1 | PDF export |

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
| [`update_text_block`](tools/element.md#update_text_block) | Update text block template and resolve |
| [`update_table_block`](tools/element.md#update_table_block) | Update table block template and resolve |
| [`update_chart_block`](tools/element.md#update_chart_block) | Update chart with structured query and chart details |
| [`update_query_block`](tools/element.md#update_query_block) | Create/update numerical query with structured query |
| [`render_chart`](tools/element.md#render_chart) | Render chart to base64 PNG image |

### Document Tools

| Tool | Description |
|------|-------------|
| [`create_document`](tools/document.md#create_document) | Create a new document |
| [`export_markdown`](tools/document.md#export_markdown) | Export document as markdown |
| [`inspect_document`](tools/document.md#inspect_document) | Inspect a document, slide, or block |
| [`get_doc_variables`](tools/document.md#get_doc_variables) | Get all variables for a document |
| [`set_doc_variables`](tools/document.md#set_doc_variables) | Set document context variables |
| [`move_block`](tools/document.md#move_block) | Move a block to a new position |

### Deck Tools

| Tool | Description |
|------|-------------|
| `save_deck` | Persist a DeckSpec to the database, returns `document_id` |
| `get_document` | Render a saved deck to HTML or PDF |
| `read_layouts` | List available slide layouts for a brand style |

See [tools.md](tools.md) for the complete tool reference with detailed documentation:
- [Model Tools](tools/model.md) — Model management and schema modification
- [Element Tools](tools/element.md) — Content block updates (text, table, chart, query)
- [Document Tools](tools/document.md) — Document operations, inspection, and variables

## Skills Reference

This bundle includes skill documentation to help Claude understand the Motley domain model:

| Skill | Purpose |
|-------|---------|
| [create-report](../skills/create-report/SKILL.md) | End-to-end report creation workflow |
| [update-chart](../skills/update-chart/SKILL.md) | Chart creation via structured configuration |
| [update-text-block](../skills/update-text-block/SKILL.md) | Text content with variable substitution |
| [update-table-block](../skills/update-table-block/SKILL.md) | Table formatting and constraints |
| [update-query-block](../skills/update-query-block/SKILL.md) | Query blocks for data retrieval |
| [explore-model](../skills/explore-model/SKILL.md) | Model exploration and custom data modeling |

See [skills.md](skills.md) for the complete skills reference.

## Architecture

```
+------------------+     stdio      +-------------------+     HTTP/JSON-RPC     +------------------+
|  Claude Desktop  | <------------> |  Passthrough      | <------------------> |  Motley Backend  |
|  (MCP Client)    |                |  MCP Server       |    + Bearer Auth      |  (Remote)        |
+------------------+                +-------------------+                       +------------------+
```

The passthrough server:
- Accepts MCP protocol messages via stdio
- Forwards them as JSON-RPC 2.0 HTTP POST requests
- Adds Bearer token authentication
- Returns responses back through stdio

## Requirements

- Node.js 18.0.0 or later
- Access to a Motley backend instance
- Valid API key with appropriate permissions

## License

MIT

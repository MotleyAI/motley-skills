# Document Tools

Tools for document operations — creating documents, inspecting slides and blocks, managing variables, and exporting.

[Back to Tools Overview](../tools.md)

---

## create_document

Create a new document with a data source.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | **Yes** | Descriptive name for the document. |
| `source_id` | integer | **Yes** | Data source ID (from `cubes_summary` or `inspect_cube`). All cubes in the document must come from this source. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `doc_id` | integer | The newly created document's ID |
| `name` | string | Document name |
| `source_id` | integer | The associated data source |

### Notes

- The `source_id` determines which cubes are available for queries within the document
- Default context variables (e.g. date ranges) are derived from the source at creation time

---

## export_markdown

Export a document as markdown.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document to export. |
| `mode` | string | No | Export mode: `"image"` (default) embeds chart images, `"table"` renders chart data as markdown tables with metadata. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `markdown` | string | The full document exported as markdown |

### Notes

- `"image"` mode is best for visual review — charts appear as embedded images
- `"table"` mode is useful when you need the underlying chart data (e.g. for re-rendering with a different charting library)

---

## get_doc_summary

Get the outline of a document including slide names, positions, descriptions, and block names.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document's ID. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Document identifier |
| `title` | string | Document title |
| `slides` | array | List of slide summaries |

Each slide in the array contains:
- `id` - Slide database ID
- `position` - Position in the document (1-indexed)
- `name` - Slide name (use this to reference the slide)
- `description` - Slide description
- `blocks` - Array of block names in the slide

---

## get_doc_variables

Get all variables and their values for a document, optionally filtered to a specific slide.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document to query. |
| `slide_name` | string | No | Filter to a specific slide. If omitted, returns variables from all slides. |
| `show_content` | boolean | No | Include full payload content for each variable. Default: false. |
| `show_context_vars` | boolean | No | Include context variables (magic keys, resolution context). Default: true. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `doc_id` | integer | The document queried |
| `variables` | array | List of variable definitions |

Each variable includes:
- `name` - Variable name (usable in templates as `{name}`)
- `slide_name` - Source slide (or null for context variables)
- `type` - Variable type (context, text, table, chart, numerical_query)
- `payload_type` - Payload type (if applicable)
- `content` - Full payload (only if `show_content=true`)

---

## set_doc_variables

Set document context variables. Merges provided values with existing parameters and re-resolves all blocks.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document to update. |
| `variables` | object | **Yes** | Key-value pairs to set (e.g. `{"client_name": "Acme", "start_date": "2025-01-01"}`). Only provide the keys you want to change. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `doc_id` | integer | The document that was updated |
| `variables` | object | The full set of context variables after the update |

### Notes

- This merges with existing variables — you only need to provide keys you want to change
- After setting variables, all blocks are re-resolved with the updated context
- Common variables include `client_name`, `start_date`, `end_date`

---

## inspect_slide

Get the full content of a specific slide including layout, blocks, and available variables.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document containing the slide. |
| `slide_name` | string | **Yes** | The exact name of the slide to inspect (from `get_doc_summary`). |

### Returns

Returns the full slide domain model as a JSON object, including:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Slide name |
| `layout` | object | Full layout structure with all blocks |
| `variables` | array | Available variables for this slide |

The `variables` array includes context variables and block-generated variables that can be used in templates.

### Notes

- Heavy fields (like chart images) are stripped from the response to reduce size
- Block directives are stripped from the response

---

## inspect_block

Get the complete configuration of a specific content block.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document containing the block. |
| `slide_name` | string | **Yes** | The slide containing the block. |
| `block_name` | string | **Yes** | The specific block to inspect (from `get_doc_summary` or `inspect_slide`). |

### Returns

Returns the full block domain model as a JSON object. The structure varies by block type but typically includes:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Block name |
| `type` | string | Block type (text, table, chart, etc.) |
| `description` | string | Block description |
| `template` | object | Template configuration (if applicable) |
| `content` | varies | Resolved content (if available) |
| `queries` | array | Associated queries (for text/table blocks) |
| `is_out_of_date` | boolean | Whether the block needs re-resolution |

---

## move_block

Move a block to a new position within the document.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `doc_id` | integer | **Yes** | The document containing the block. |
| `block_name` | string | **Yes** | The block to move. |
| `location` | integer | No | New 1-indexed position. Provide either `location` or `after_block`. |
| `after_block` | string | No | Name of the block after which to place this block. Provide either `location` or `after_block`. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `block_name` | string | The block that was moved |
| `new_position` | integer | The block's new position |

### Notes

- Provide exactly one of `location` or `after_block`
- Other blocks are renumbered automatically

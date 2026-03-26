# Element Tools

Tools for updating content blocks within slides - text, tables, charts, and queries.

[Back to Tools Overview](../tools.md)

---

## update_text_block

Update the template of a text block and resolve it to generate content.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `master_id` | integer | **Yes** | The master containing the slide. |
| `slide_name` | string | **Yes** | The slide containing the text block. |
| `block_name` | string | **Yes** | The text block to update. |
| `user_prompt` | string | **Yes** | The template content with `{variable}` placeholders. Valid CommonMark markdown. |
| `call_llm` | boolean | No | When true, pass template to LLM for generation. Default: false (direct variable substitution). |
| `allowed_outputs` | array[string] | No | Constrain LLM to these exact outputs. Only valid when `call_llm=true`. |
| `behavior_if_query_fails` | string | No | What happens if a child query fails: `"drop_slide"` (skip slide gracefully) or `"fail_resolution"` (raise error). If not provided, unchanged. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `slide_name` | string | The slide that was updated |
| `block_name` | string | The block that was updated |
| `block` | object | The updated block domain model |

### Notes

- When `call_llm=false`, variables in `{curly_braces}` are directly substituted
- When `call_llm=true`, the template is sent to an LLM for generation with variable context
- Use `allowed_outputs` to constrain LLM responses to specific values (e.g., sentiment classification)

### Example Template

```markdown
## {client_name} Performance Summary

Revenue for the period was {revenue_query}, representing a {growth_pct}% change.
```

---

## update_table_block

Update the template of a table block and resolve it to generate content.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `master_id` | integer | **Yes** | The master containing the slide. |
| `slide_name` | string | **Yes** | The slide containing the table block. |
| `block_name` | string | **Yes** | The table block to update. |
| `user_prompt` | string | **Yes** | The template content for the table. Uses markdown table syntax or variable references. |
| `call_llm` | boolean | No | When true, use LLM to generate table content. Default: false. |
| `target_shape` | tuple | No | Table dimension constraints. See below for format. |
| `behavior_if_query_fails` | string | No | What happens if a child query fails: `"drop_slide"` (skip slide gracefully) or `"fail_resolution"` (raise error). If not provided, unchanged. |

### target_shape Format

The `target_shape` parameter constrains table dimensions as `(rows, columns)`. Each dimension can be:

| Value | Meaning |
|-------|---------|
| `null` | No constraint on this dimension |
| `int` | Exact count required |
| `[min, max]` | Range (inclusive) |

**Examples:**
- `[null, 2]` - Any number of rows, exactly 2 columns
- `[[1, 11], 2]` - Between 1 and 11 rows, exactly 2 columns
- `[5, null]` - Exactly 5 rows, any number of columns

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `slide_name` | string | The slide that was updated |
| `block_name` | string | The block that was updated |
| `block` | object | The updated block domain model |

---

## update_chart_block

Create or update a chart block from a structured query and chart configuration. Validates the query against Cube.js and renders the chart. When location is omitted, creates a transient chart.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | object | No | `{doc_id, slide_name, block_name}` — location of the chart block. If omitted, creates a transient chart without saving. |
| `query` | object | **Yes** | MinimalSemanticLayerQueryForLLM as JSON. Contains `measures`, `dimensions`, `time_dimension` (singular object, not a list), `filters`, `limit`, `order`. |
| `chart_details` | object | **Yes** | ChartDetailsTemplate as JSON. Contains series configuration, axis settings, title, color_scheme, etc. |
| `sample_values` | object | No | Override filter values (e.g. `start_date`, `end_date`, `client_name`). |
| `max_return_rows` | integer | No | Maximum data rows in the response preview (default: 20). |
| `add_default_filters` | boolean | No | Whether to apply default cube filters (default: true). |

**Note:** `cube_name` is automatically derived from the query measures/dimensions — do not pass it explicitly.

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `doc_id` | integer | The deck ID (null for transient) |
| `slide_name` | string | The slide |
| `block_name` | string | The chart block |
| `preview_rows` | array | Preview of the query result data |

### Notes

- Validates the query against Cube.js before rendering
- The `time_dimension` field is a **singular object** (not a list) with `dimension`, `granularity`, and optional time filter fields
- The chart is marked as out-of-date and needs resolution via `render_chart`

---

## update_query_block

Create or update a numerical query within a parent text or table block's queries list.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `master_id` | integer | **Yes** | The master containing the slide. |
| `slide_name` | string | **Yes** | The slide containing the parent block. |
| `parent_block` | string | **Yes** | The text or table block containing the queries list. |
| `query_name` | string | **Yes** | Identifier for the query within the parent's queries list. Creates new if not found. |
| `prompt` | string | **Yes** | Natural language description of the query. |
| `cube_name` | string | No | Limit to a specific cube. If omitted, all cubes are available. |
| `mode` | string | No | Query mode. Default: `"single_number"`. |
| `pivot_dimension` | string | No | Dimension to pivot into columns (table mode only). Format: `"dim_name"` or `"cube_name.dim_name"`. |
| `transpose` | boolean | No | Swap rows and columns (table mode only). Default: false. |

### Query Modes

| Mode | Description |
|------|-------------|
| `single_number` | Returns a single aggregate value (e.g., total revenue). Use for KPIs. |
| `table` | Returns a full result set with multiple rows/columns. Supports pivoting and transpose. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `master_id` | integer | The master |
| `slide_name` | string | The slide |
| `parent_block` | string | The parent block name |
| `query_name` | string | The query identifier |
| `action` | string | Either `"created"` or `"updated"` |
| `block` | object | The generated query block |

### Notes

- Uses Claude Opus 4.5 for query generation from natural language
- The query is added to `parent_block.queries` and can be referenced as `{query_name}` in the parent's template
- If updating an existing query, context from the previous query is provided to the LLM

### Example Prompts

**Single number mode:**
```
Total revenue for the selected date range
```

**Table mode:**
```
Monthly revenue breakdown by product category
```

**Table mode with pivot:**
```
Sales by region with months as columns (set pivot_dimension="month")
```

---

## render_chart

Render a chart block to a PNG image and return it as base64-encoded data.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `master_id` | integer | **Yes** | The master containing the slide. |
| `slide_name` | string | **Yes** | The slide containing the chart. |
| `block_name` | string | **Yes** | The chart block to render. |
| `width` | integer | No | Image width in pixels. Default: 800. |
| `height` | integer | No | Image height in pixels. Default: 600. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether rendering succeeded |
| `master_id` | integer | The master ID |
| `slide_name` | string | The slide name |
| `block_name` | string | The block name |
| `image_base64` | string | Base64-encoded PNG image data |
| `width` | integer | Actual image width used |
| `height` | integer | Actual image height used |
| `resolved` | boolean | Whether resolution was triggered (true if chart had no content) |
| `error` | string | Error message (only if success=false) |

### Notes

- If the chart has not been resolved (no content), resolution is triggered automatically first
- The image is rendered using ECharts and returned as base64-encoded PNG data
- Default dimensions are 800x600 pixels
- Uses 100 DPI internally for converting pixels to inches

### Example Usage

```
render_chart(master_id=42, slide_name="Overview", block_name="revenue_chart")
```

```
render_chart(master_id=42, slide_name="Detail", block_name="trend_chart", width=1200, height=800)
```

---

## copy_block

Copy content from one block to another. Supports copying between slides within the same master, or between different masters. If the block types differ, the target block is automatically converted to match the source block type while preserving its layout properties (width, height, placeholder, description). For numerical_query source blocks, the copied query is attached to a parent text or table block in the target slide.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_master_id` | integer | **Yes** | The master containing the source block. |
| `source_slide_name` | string | **Yes** | The slide containing the source block. |
| `source_block_name` | string | **Yes** | The block to copy from. |
| `target_master_id` | integer | **Yes** | The master containing the target block. |
| `target_slide_name` | string | **Yes** | The slide containing the target block. |
| `target_block_name` | string | **Yes** | The block to copy to (or query name when copying a query). |
| `parent_block_name` | string | No | Required when source is a `numerical_query` block. Name of a text or table block in the target slide whose queries list the copied query will be attached to. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `source_master_id` | integer | Source master ID |
| `source_slide_name` | string | Source slide name |
| `source_block_name` | string | Source block name |
| `target_master_id` | integer | Target master ID |
| `target_slide_name` | string | Target slide name |
| `target_block_name` | string | Target block name |
| `type_converted` | boolean | Whether the target block type was converted to match the source |
| `copied_content` | boolean | Whether content was copied |
| `parent_block_name` | string | The parent block name (when a query was attached) |
| `message` | string | Confirmation message |

### Notes

- If block types differ, the target is automatically converted to match the source type while preserving layout properties (width, height, placeholder, description)
- Templates are always copied for non-query blocks; child queries are never copied
- For `numerical_query` source blocks, `parent_block_name` is required and the query is deep-copied and attached to the parent block's queries list
- Target block is marked as out-of-date after copy
- Supports cross-master copying (source and target can be in different masters)
- Use with `match_slides` to bulk-copy content between masters after layout library import

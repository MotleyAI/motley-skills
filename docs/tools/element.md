# Element Tools

Tools for updating content blocks within slides — text, tables, charts, and queries.

[Back to Tools Overview](../tools.md)

---

## update_text_block

Update the template of a text block and resolve it to generate content.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | object | **Yes** | `{doc_id: int, slide_name: str, block_name: str}` — the block to update. |
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
| `content` | string | The resolved text content |

### Notes

- When `call_llm=false`, variables in `{curly_braces}` are directly substituted
- When `call_llm=true`, the template is sent to an LLM for generation with variable context
- Use `allowed_outputs` to constrain LLM responses to specific values (e.g., sentiment classification)

### Example Template

```markdown
## {client_name} Performance Summary

Revenue for the period was {currency(revenue_query)}, representing a {percent(growth_pct)} change.
```

---

## update_table_block

Update the template of a table block and resolve it to generate content.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | object | **Yes** | `{doc_id: int, slide_name: str, block_name: str}` — the block to update. |
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
| `content` | string | The resolved table content as markdown |

---

## update_chart_block

Create or update a chart block with a structured query and chart configuration.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | object | No | `{doc_id: int, slide_name: str, block_name: str}` — the chart block. If omitted, creates a transient chart. |
| `query` | object | **Yes** | Semantic layer query (MinimalSemanticLayerQueryForLLM as JSON). Contains `measures`, `dimensions`, `time_dimension`, `filters`, `limit`, `order`. |
| `chart_details` | object | **Yes** | Chart rendering configuration (ChartDetailsTemplate as JSON). Contains `series`, `x_axis`, `y_axis`, `y_right_axis`, `series_default`, `color_scheme`, `title`, `legend`. |
| `sample_values` | object | No | Override filter values (e.g., `{"start_date": "2025-01-01"}`). Takes priority over document parameters. |
| `max_return_rows` | integer | No | Maximum rows in response preview. Default: 20. |
| `add_default_filters` | boolean | No | Apply default cube filters (time range, tenant). Default: true. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `doc_id` | integer | The document ID |
| `slide_name` | string | The slide |
| `block_name` | string | The chart block |
| `data_preview` | string | Preview of the query results |

### Notes

- The chart is saved but NOT rendered immediately — use `render_chart` to see the output
- Query and chart_details schemas are defined in the tool definition; see the `update-chart` skill for usage guidance

### Example

```
update_chart_block(
    location={doc_id: 42, slide_name: "Revenue", block_name: "revenue_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "revenue"}],
        time_dimension: {dimension: {name: "created_at", cube_name: "revenue"}, granularity: "month"}
    },
    chart_details={
        series_default: {type: "LINE", y_axis: "left"},
        x_axis: {lines: false},
        y_axis: {lines: true, label: "Revenue"},
        y_right_axis: {lines: false}
    }
)
```

---

## update_query_block

Create or update a numerical query within a parent text or table block's queries list.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | object | No | `{doc_id: int, slide_name: str, parent_block: str}` — the parent block. If omitted, creates a transient query. |
| `query_name` | string | **Yes** | Identifier for the query within the parent's queries list. Creates new if not found. |
| `query` | object | **Yes** | Semantic layer query (MinimalSemanticLayerQueryForLLM as JSON). Contains `measures`, `dimensions`, `time_dimension`, `filters`, `limit`, `order`. |
| `mode` | string | No | Query mode. Default: `"single_number"`. |
| `pivot_dimension` | string | No | Dimension to pivot into columns (table mode only). Format: `"dim_name"` or `"cube_name.dim_name"`. |
| `transpose` | boolean | No | Swap rows and columns (table mode only). Default: false. |
| `sample_values` | object | No | Override filter values. Takes priority over document parameters. |
| `max_return_rows` | integer | No | Max rows in response preview. Default: 20. |
| `add_default_filters` | boolean | No | Apply default cube filters. Default: true. |

### Query Modes

| Mode | Description |
|------|-------------|
| `single_number` | Returns a single aggregate value (e.g., total revenue). Use for KPIs. |
| `table` | Returns a full result set with multiple rows/columns. Supports pivoting and transpose. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `doc_id` | integer | The document ID |
| `slide_name` | string | The slide |
| `parent_block` | string | The parent block name |
| `query_name` | string | The query identifier |
| `action` | string | Either `"created"` or `"updated"` |
| `result` | string | The query result (value or markdown table) |

### Notes

- The query is added to `parent_block.queries` and can be referenced as `{query_name}` in the parent's template
- If updating an existing query, the previous query provides context

### Example

```
update_query_block(
    location={doc_id: 42, slide_name: "Overview", parent_block: "metrics_text"},
    query_name="total_revenue",
    query={measures: [{name: "total_revenue", cube_name: "revenue"}]}
)
```

---

## render_chart

Render a chart block to a PNG image and return it as base64-encoded data.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | object | **Yes** | `{doc_id: int, slide_name: str, block_name: str}` — the chart block to render. |
| `width` | integer | No | Image width in pixels. Default: 800. |
| `height` | integer | No | Image height in pixels. Default: 600. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether rendering succeeded |
| `doc_id` | integer | The document ID |
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

### Example Usage

```
render_chart(location={doc_id: 42, slide_name: "Overview", block_name: "revenue_chart"})
```

```
render_chart(location={doc_id: 42, slide_name: "Detail", block_name: "trend_chart"}, width=1200, height=800)
```

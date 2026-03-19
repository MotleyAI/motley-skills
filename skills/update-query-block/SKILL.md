---
name: update-query-block
description: >
  Create or modify numerical query blocks within text or table blocks using
  update_query_block. Queries provide data values referenced as {query_name}
  in parent templates.
---

# Update Query Block

Create or update numerical queries inside text or table blocks. Queries execute against a cube and make their results available as `{query_name}` variables in the parent block's `user_prompt`.

## How It Works

1. You call `update_query_block` with a natural language `prompt` describing the data you want
2. An LLM internally generates the full query (measures, dimensions, filters) from your prompt
3. The query result becomes available as `{query_name}` in the parent text/table block's `user_prompt`
4. When the parent block is resolved (via `update_text_block` or `update_table_block`), the query value is substituted in

You do NOT construct queries manually — just describe what you want in plain English.

## Tool Signature

```
update_query_block(
    location: {                # Location of the query's parent block
        doc_id: int,           # The deck ID
        slide_name: str,       # The slide containing the parent block
        parent_block: str      # Name of the text or table block containing this query
    },
    query_name: str,          # Name for this query (used as {query_name} in parent's user_prompt)
    prompt: str,              # Natural language description of the desired query
    cube_name: str?,          # Optional: constrain to this cube only
    mode: str?,               # "single_number" (default) or "table"
    pivot_dimension: str?,    # Dimension to pivot into columns (table mode only)
    transpose: bool?          # Swap rows/columns (table mode only)
)
```

**Returns**: The query result — a single value for `single_number` mode, or a markdown table for `table` mode.

## Query Modes

### `single_number` (default)

Returns a single aggregate value. Use for KPIs, metrics, and inline numbers in text.

**Example prompts**:
- "Total revenue for the reporting period"
- "Number of active customers"
- "Average order value this quarter"
- "Percentage of deals closed vs opened"

The result substitutes directly into text: `Revenue grew to {total_revenue} this quarter.`

### `table`

Returns the full query result as a markdown table. Use when you need multi-row data for LLM analysis or table blocks.

**Example prompts**:
- "Monthly revenue breakdown for the last 12 months"
- "Top 10 customers by order count"
- "Revenue by region and product category"

The result is a formatted markdown table that the LLM can analyze or display.

## Writing Effective Prompts

Be specific about:
- **What measure**: "total revenue", "count of orders", "average deal size"
- **What filters**: "for active customers only", "where status is completed"
- **What grouping** (for table mode): "by region", "by month", "by product category"
- **What ordering**: "sorted by revenue descending", "top 10 by count"
- **What time range**: "for the last 12 months", "year to date" (or rely on master's sample_parameters)

The query LLM automatically has access to the master's `sample_parameters` (customer name, date range), so filters for the reporting period and customer are applied automatically unless you specify otherwise.

## Workflow

**Important**: You must create query blocks BEFORE referencing them in `update_text_block` or `update_table_block`.

1. Create queries with `update_query_block`:
   ```
   update_query_block(
       location={doc_id: 42, slide_name: "Overview", parent_block: "metrics_text"},
       query_name="total_revenue",
       prompt="Total revenue for the reporting period",
       cube_name="revenue"
   )
   ```

2. Then set the parent template referencing the query:
   ```
   update_text_block(
       location={doc_id: 42, slide_name: "Overview", block_name: "metrics_text"},
       user_prompt="Revenue reached {currency(total_revenue)} this quarter, up {percent(revenue_growth)} from last quarter."
   )
   ```

The `query_name` ("total_revenue") must match the `{variable}` reference in the parent's `user_prompt`.

## Pivot and Transpose (Table Mode)

### pivot_dimension

Pivots a dimension's values into column headers. Useful for creating cross-tab tables.

```
update_query_block(
    location={doc_id: 42, slide_name: "Breakdown", parent_block: "data_table"},
    query_name="revenue_by_region_month",
    prompt="Revenue by region and month for the last 6 months",
    mode="table",
    pivot_dimension="time"
)
```

Result without pivot:
| Region | Month | Revenue |
|--------|-------|---------|
| US | Jan | 100K |
| US | Feb | 120K |
| EU | Jan | 80K |

Result with `pivot_dimension="time"`:
| Region | Jan | Feb |
|--------|-----|-----|
| US | 100K | 120K |
| EU | 80K | 90K |

### transpose

Swaps rows and columns. Combine with `pivot_dimension` for flexible layouts.

```
update_query_block(
    ...,
    mode="table",
    pivot_dimension="time",
    transpose=true
)
```

## Examples

### Single Number — KPI

```
update_query_block(
    location={doc_id: 42, slide_name: "Executive Summary", parent_block: "kpi_text"},
    query_name="active_users",
    prompt="Count of active users in the current period",
    cube_name="users"
)
```

### Single Number — Comparison Value

```
update_query_block(
    location={doc_id: 42, slide_name: "Executive Summary", parent_block: "kpi_text"},
    query_name="prev_active_users",
    prompt="Count of active users in the previous period (same length as reporting period, immediately before start_date)",
    cube_name="users"
)
```

Then in the parent: `Active users: {active_users} ({percent((active_users - prev_active_users) / prev_active_users)} vs previous period)`

### Table — Monthly Breakdown

```
update_query_block(
    location={doc_id: 42, slide_name: "Trends", parent_block: "trend_table"},
    query_name="monthly_data",
    prompt="Monthly revenue and order count for the last 12 months, sorted chronologically",
    mode="table",
    cube_name="orders"
)
```

### Table — Pivoted Cross-Tab

```
update_query_block(
    location={doc_id: 42, slide_name: "Comparison", parent_block: "comparison_table"},
    query_name="region_quarterly",
    prompt="Revenue by region and quarter for the last 4 quarters",
    mode="table",
    pivot_dimension="time",
    cube_name="revenue"
)
```

## Related Skills

- For exploring cubes before writing prompts: see the `explore-cube` skill
- For expression syntax in templates: see [variable-reference-syntax.md](../_shared/variable-reference-syntax.md)
- For context variables: see [resolution-context.md](../_shared/resolution-context.md)

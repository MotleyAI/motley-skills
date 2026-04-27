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

1. You call `update_query_block` with a structured `query` describing the data you want
2. The query is validated and executed against the semantic layer
3. The query result becomes available as `{query_name}` in the parent text/table block's `user_prompt`
4. When the parent block is resolved (via `update_text_block` or `update_table_block`), the query value is substituted in

## Tool Signature

```
update_query_block(
    parent_location: {         # Location of the query's parent block
        doc_id: int,           # The document ID
        slide_name: str,       # The slide containing the parent block
        block_name: str        # Name of the text or table block containing the queries list
    },
    query_name: str,           # Name for this query (used as {query_name} in parent's user_prompt)
    query: {                   # Semantic layer query (MinimalSemanticLayerQueryForLLM)
        measures: [            # List of measures to aggregate
            {name: str, cube_name: str?}
        ],
        dimensions: [          # List of dimensions to group by
            {name: str, cube_name: str?}
        ]?,
        time_dimension: {      # Single time dimension (NOT a list)
            dimension: {name: str, cube_name: str?},
            granularity: str?  # "day", "week", "month", "quarter", "year"
        }?,
        filters: [...]?,       # Filters array
        limit: int?,           # Max rows to return
        order: [               # Ordering
            {column: {name: str, cube_name: str?}, order: "ASC"|"DESC"}
        ]?
    },
    mode: str? = "single_number",  # "single_number" or "table"
    pivot_dimension: str?,     # Dimension to pivot into columns (table mode only)
    transpose: bool?,          # Swap rows/columns (table mode only)
    sample_values: {str: str}?,    # Override filter values (e.g. start_date, end_date)
    max_return_rows: int? = 20,    # Max rows in response preview
    add_default_filters: bool? = true  # Apply default time/tenant filters
)
```

**Returns**: The query result — a single value for `single_number` mode, or a markdown table for `table` mode.

The full nested schema for `query` comes from the tool definition. The above shows the most commonly used fields.

When `add_default_filters=true` (the default), the cube's default time dimension is filtered between the document's `start_date` and `end_date` automatically — you don't need to add a time filter to your `query` spec. Set it to `false` only for queries that should ignore the document's date range (e.g. "all-time" totals).

## Query Modes

### `single_number` (default)

Returns a single aggregate value. Use for KPIs, metrics, and inline numbers in text.

**Example**: A query with `measures: [{name: "total_revenue", cube_name: "revenue"}]` and no dimensions returns the total.

The result substitutes directly into text: `Revenue grew to {total_revenue} this quarter.`

### `table`

Returns the full query result as a markdown table. Use when you need multi-row data for LLM analysis or table blocks.

**Example**: A query with measures + dimensions returns grouped results as a table.

## Workflow

**Important**: You must create query blocks BEFORE referencing them in `update_text_block` or `update_table_block`.

1. Create queries with `update_query_block`:
   ```
   update_query_block(
       parent_location={doc_id: 42, slide_name: "Overview", block_name: "metrics_text"},
       query_name="total_revenue",
       query={
           measures: [{name: "total_revenue", cube_name: "revenue"}]
       }
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
    parent_location={doc_id: 42, slide_name: "Breakdown", block_name: "data_table"},
    query_name="revenue_by_region_month",
    query={
        measures: [{name: "total_revenue", cube_name: "revenue"}],
        dimensions: [{name: "region", cube_name: "revenue"}],
        time_dimension: {
            dimension: {name: "created_at", cube_name: "revenue"},
            granularity: "month"
        }
    },
    mode="table",
    pivot_dimension="created_at"
)
```

Result without pivot:
| Region | Month | Revenue |
|--------|-------|---------|
| US | Jan | 100K |
| US | Feb | 120K |
| EU | Jan | 80K |

Result with `pivot_dimension="created_at"`:
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
    pivot_dimension="created_at",
    transpose=true
)
```

## Examples

### Single Number — KPI

```
update_query_block(
    parent_location={doc_id: 42, slide_name: "Executive Summary", block_name: "kpi_text"},
    query_name="active_users",
    query={
        measures: [{name: "active_user_count", cube_name: "users"}]
    }
)
```

### Single Number — Comparison Value

```
update_query_block(
    parent_location={doc_id: 42, slide_name: "Executive Summary", block_name: "kpi_text"},
    query_name="prev_active_users",
    query={
        measures: [{name: "active_user_count", cube_name: "users"}],
        filters: [{"member": "users.period", "operator": "equals", "values": ["previous"]}]
    }
)
```

Then in the parent: `Active users: {active_users} ({percent((active_users - prev_active_users) / prev_active_users)} vs previous period)`

### Table — Monthly Breakdown

```
update_query_block(
    parent_location={doc_id: 42, slide_name: "Trends", block_name: "trend_table"},
    query_name="monthly_data",
    query={
        measures: [
            {name: "total_revenue", cube_name: "orders"},
            {name: "order_count", cube_name: "orders"}
        ],
        time_dimension: {
            dimension: {name: "created_at", cube_name: "orders"},
            granularity: "month"
        },
        limit: 12,
        order: [{column: {name: "created_at", cube_name: "orders"}, order: "ASC"}]
    },
    mode="table"
)
```

### Table — Pivoted Cross-Tab

```
update_query_block(
    parent_location={doc_id: 42, slide_name: "Comparison", block_name: "comparison_table"},
    query_name="region_quarterly",
    query={
        measures: [{name: "total_revenue", cube_name: "revenue"}],
        dimensions: [{name: "region", cube_name: "revenue"}],
        time_dimension: {
            dimension: {name: "created_at", cube_name: "revenue"},
            granularity: "quarter"
        },
        limit: 20
    },
    mode="table",
    pivot_dimension="created_at"
)
```

## Related Skills

- For exploring models before writing queries: see the `explore-model` skill
- For expression syntax in templates: see [variable-reference-syntax.md](../../shared/variable-reference-syntax.md)
- For context variables: see [resolution-context.md](../../shared/resolution-context.md)

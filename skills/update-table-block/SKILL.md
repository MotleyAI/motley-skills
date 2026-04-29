---
name: update-table-block
description: >
  Create or modify table blocks using update_table_block. Covers template syntax,
  target_shape constraints, and table generation patterns.
---

# Update Table Block

Create or modify table blocks using the `update_table_block` MCP tool. Table blocks support variable substitution, LLM-generated tables, and size constraints via `target_shape`.

## How It Works

1. Call `update_table_block` with a `user_prompt` template
2. The block resolves **immediately** — variables are substituted and (optionally) LLM generates the table
3. The resolved table content is returned inline in the tool response

**Returns**: The resolved table content as markdown.

## target_shape Format

Controls the expected table dimensions as `[rows, cols]`. Each dimension can be:

| Value | Meaning | Example |
|-------|---------|---------|
| `null` | No constraint | `[null, 3]` — any rows, exactly 3 columns |
| `int` | Exact count | `[5, 3]` — exactly 5 rows and 3 columns |
| `[min, max]` | Range | `[[3, 8], 4]` — 3-8 rows, exactly 4 columns |

**Examples**:
- `[5, 3]` — exactly 5 rows, 3 columns
- `[null, 4]` — any number of rows, 4 columns
- `[[1, 10], null]` — 1-10 rows, any columns
- `[[3, 8], [2, 5]]` — 3-8 rows, 2-5 columns

Row count does NOT include the header row.

## Three Patterns

### Pattern A: Raw Query Output

Pass a `table` mode query result directly as the table. No LLM needed.

```
# First, create a table-mode query:
update_query_block(
    parent_location={doc_id: 42, slide_name: "Data", block_name: "data_table"},
    query_name="monthly_data",
    prompt="Monthly revenue and order count for last 12 months",
    mode="table",
    model_name="orders"
)

# Then set the table template to just reference the query:
update_table_block(
    location={doc_id: 42, slide_name: "Data", block_name: "data_table"},
    user_prompt="{monthly_data}",
    target_shape=[[1, 12], 3]
)
```

### Pattern B: Markdown Template with Variables

Build a table template with inline variable substitution.

```
update_table_block(
    location={doc_id: 42, slide_name: "KPIs", block_name: "kpi_table"},
    user_prompt="| Metric | Value |\n|--------|-------|\n| Revenue | {currency(total_revenue)} |\n| Customers | {integer(active_customers)} |\n| Growth | {percent(revenue_growth)} |",
    target_shape=[3, 2]
)
```

### Pattern C: LLM-Generated from Data

Let the LLM build the table from query data.

```
update_table_block(
    location={doc_id: 42, slide_name: "Analysis", block_name: "summary_table"},
    user_prompt="Create a summary table from this data:\n\n{detailed_data}\n\nShow the top 5 items by revenue with columns: Name, Revenue, Growth %, Status",
    call_llm=true,
    target_shape=[5, 4]
)
```

## Template Syntax

Same as text blocks — supports `{variable}`, `{Slide::Block}`, arithmetic, and formatting functions.

See [variable-reference-syntax.md](../../shared/variable-reference-syntax.md) for full details.

## Workflow

**Every reference in the template must exist before you call `update_table_block`.** The block resolves immediately, so any `{variable}` that can't be found will cause a resolution failure.

- `{query_name}` → call `update_query_block` first
- `{Slide::Block}` → the referenced slide/block must already have content
- `{context_var}` (e.g. `{end_month}`, or any source-specific key from `get_doc_variables`) → no setup needed if `get_doc_variables` lists it

Create query blocks first, then set the table template:

1. Create data queries:
   ```
   update_query_block(
       parent_location={doc_id: 42, slide_name: "Performance", block_name: "perf_table"},
       query_name="region_data",
       prompt="Revenue and customer count by region, top 5 regions by revenue",
       mode="table",
       model_name="sales"
   )
   ```

2. Set the table template:
   ```
   update_table_block(
       location={doc_id: 42, slide_name: "Performance", block_name: "perf_table"},
       user_prompt="{region_data}",
       target_shape=[5, 3]
   )
   ```

## Examples

### Simple Data Table

```
update_table_block(
    location={doc_id: 42, slide_name: "Revenue", block_name: "revenue_table"},
    user_prompt="{quarterly_revenue}",
    target_shape=[4, 3]
)
```

### KPI Scorecard

```
update_table_block(
    location={doc_id: 42, slide_name: "Scorecard", block_name: "scorecard_table"},
    user_prompt="| KPI | Target | Actual | Status |\n|-----|--------|--------|--------|\n| Revenue | {currency(target_revenue)} | {currency(actual_revenue)} | {revenue_status} |\n| Users | {integer(target_users)} | {integer(actual_users)} | {users_status} |\n| NPS | {target_nps} | {actual_nps} | {nps_status} |",
    target_shape=[3, 4]
)
```

### LLM-Summarized Table

```
update_table_block(
    location={doc_id: 42, slide_name: "Executive View", block_name: "exec_table"},
    user_prompt="Based on the following monthly performance data, create a table summarizing each quarter with columns: Quarter, Revenue, Trend, Key Highlight.\n\n{monthly_data}\n\nKeep highlights to one short sentence each.",
    call_llm=true,
    target_shape=[4, 4]
)
```

### Pivoted Cross-Tab

```
# Create a pivoted query first:
update_query_block(
    parent_location={doc_id: 42, slide_name: "Matrix", block_name: "matrix_table"},
    query_name="product_region_matrix",
    prompt="Revenue by product and region",
    mode="table",
    pivot_dimension="region",
    model_name="sales"
)

# Display it:
update_table_block(
    location={doc_id: 42, slide_name: "Matrix", block_name: "matrix_table"},
    user_prompt="{product_region_matrix}",
    target_shape=[null, null]
)
```

## Overflow Handling

If the resolved table exceeds the element's size on the slide, the tool returns an overflow error. To fix:
- **Reduce rows**: Use `target_shape` with a lower row count, or add "top N" to your query prompt
- **Reduce columns**: Select fewer measures/dimensions in the query
- **Shorten content**: Use abbreviations or shorter labels
- **Use LLM**: Set `call_llm=true` and instruct it to be concise

## Error Handling — `behavior_if_query_fails`

Same as text blocks:
- `"drop_slide"` — Slide is silently skipped during export
- `"fail_resolution"` — Resolution raises an error
- `null` (default) — Keeps existing behavior

## Related Skills

- For creating query blocks: see the `update-query-block` skill
- For expression syntax: see [variable-reference-syntax.md](../../shared/variable-reference-syntax.md)
- For context variables: see [resolution-context.md](../../shared/resolution-context.md)

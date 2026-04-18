# Resolution Context — Auto-Generated Variables

When a master is resolved, context variables are automatically generated from the base parameters (sample_parameters) configured on the master.

## Base Variables (User-Provided)

These are set on the master via `sample_parameters` (configured when creating a master with `source_id`, or edited later):

| Variable | Type | Description |
|----------|------|-------------|
| `end_date` | date | End date for time-based filters |
| `start_date` | date | Start date for time-based filters |
| `client_name` | string | Customer/client name for filtering |

## Auto-Generated Variables

These are automatically derived from base variables during resolution:

| Variable | Source | Format | Example |
|----------|--------|--------|---------|
| `end_month` | Formatted from `end_date` | `%B %Y` | "December 2025" |
| `start_month` | Formatted from `start_date` | `%B %Y` | "September 2025" |
| `quarter` | Derived from `end_date` (minus 30 days) | `QN YYYY` | "Q4 2025" |
| `now_date` | Current date | date | 2025-01-08 |
| `now_month` | Formatted from `now_date` | `%B %Y` | "January 2025" |
| `customer_name` | Copy of `client_name` | string | "Acme Corp" |

## Using in Templates

Reference any context variable in `user_prompt` for `update_text_block` or `update_table_block`:

```
Report Period: {start_month} to {end_month}
Quarter: {quarter}
Customer: {customer_name}
```

These variables are available alongside query block results — no query block is needed for context variables.

## Checking Available Variables

Use the `get_master_variables` MCP tool to see all available variables for a master:

```
get_master_variables(master_id=..., show_context_vars=true)
```

This returns:
- Context variables (from `sample_parameters` and auto-generated ones)
- Query block results (from `update_query_block` calls)
- Cross-slide references available via `{Slide::Block}` syntax

## How Context Flows to Queries

When you write prompts for `update_query_block` or `update_chart_block`, the LLM that generates the query automatically has access to:
- The master's `sample_parameters` (to generate appropriate time filters and customer filters)
- The cube schema (to pick the right measures/dimensions)

You don't need to manually specify filters for `end_date`, `start_date`, or `client_name` — the query LLM handles this. Just mention the intent in your prompt (e.g., "for the current reporting period" or "for the selected customer").

## Related Documentation

- For expression syntax using variables: see [variable-reference-syntax.md](variable-reference-syntax.md)

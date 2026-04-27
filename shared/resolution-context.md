# Resolution Context — Document & Master Variables

When a document or master is resolved, context variables become available to templates. Some are universally available; others are source-specific.

## Universal Variables (always available)

These exist on every document/master regardless of the data source — they're driven by the date parameters set at creation time (and refreshable via `set_doc_variables` on documents or master `sample_parameters`).

| Variable | Type | Description |
|----------|------|-------------|
| `start_date` | date | Start date for time-based filters |
| `end_date` | date | End date for time-based filters |

### Auto-Generated From Dates

| Variable | Source | Format | Example |
|----------|--------|--------|---------|
| `end_month` | Formatted from `end_date` | `%B %Y` | "December 2025" |
| `start_month` | Formatted from `start_date` | `%B %Y` | "September 2025" |
| `quarter` | Derived from `end_date` (minus 30 days) | `QN YYYY` | "Q4 2025" |
| `now_date` | Current date | date | 2025-01-08 |
| `now_month` | Formatted from `now_date` | `%B %Y` | "January 2025" |

## Source-Specific Variables

Anything beyond the date keys above (e.g. `client_name`, `customer_name`, `region`) only exists when the **data source declares it via a default filter**. For sources without such declarations (e.g. demo sources like Jaffle Shop), these variables are NOT available — referencing them in a template will fail at resolution time.

Always discover what's actually available for the current document with:

```
get_doc_variables(doc_id=..., show_context_vars=true)
```

(For masters: `get_master_variables(master_id=..., show_context_vars=true)`.)

The response lists every variable the document can resolve — universal date keys plus whatever source-specific keys the source has declared.

## Using in Templates

Reference any available context variable in `user_prompt` for `update_text_block` or `update_table_block`:

```
Report Period: {start_month} to {end_month}
Quarter: {quarter}
```

If `get_doc_variables` shows a `client_name` (or any other source-specific variable), it can be referenced the same way:

```
Customer: {client_name}
```

These variables are available alongside query block results — no query block is needed.

## How Context Flows to Queries

When you write prompts for `update_query_block` or `update_chart_block`, the query-generating LLM automatically has access to:
- The document's resolved parameters (to generate appropriate time filters and any source-specific filters)
- The cube schema (to pick the right measures/dimensions)

You don't need to manually specify filters for `start_date` / `end_date` — the query LLM handles them. The same goes for source-specific filters that the source declares; mention the intent in your prompt (e.g. "for the current reporting period" or "for the selected customer") and the query LLM applies the relevant default filter.

## Related Documentation

- For expression syntax using variables: see [variable-reference-syntax.md](variable-reference-syntax.md)

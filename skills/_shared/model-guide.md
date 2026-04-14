# Model Guide

This document covers data modeling concepts for working with models in Motley. The MCP tools handle query construction internally via LLM — you describe what data you want in natural language prompts. This guide helps you understand what's expressible.

## Concepts

### Models

A **model** is a data model backed by a SQL query or table. Each model has:
- **Measures** — aggregate values (revenue, count, average)
- **Dimensions** — grouping/filtering columns (region, status, category)
- **Derived dimensions** — computed columns from sub-queries

Use `models_summary()` to list all available models and their schemas, or `models_summary(verbose=false)` for a compact name-only listing.
Use `inspect_model(model_name=..., num_rows=3)` to see sample data.

### Measures

Measures are aggregate columns. Each has a type that defines how it's aggregated.

| Type | Description | Example |
|------|-------------|---------|
| `count` | Count of rows | Total orders |
| `count_distinct` | Count of unique values | Unique customers |
| `count_distinct_approx` | Approximate count distinct (faster) | Approximate unique visitors |
| `sum` | Sum of values | Total revenue |
| `avg` | Average of values | Average order value |
| `min` | Minimum value | Earliest date |
| `max` | Maximum value | Latest date |
| `number` | Pre-computed numeric expression | Ratio, percentage |

### Dimensions

Dimensions are grouping/filtering columns.

| Type | Description | Examples |
|------|-------------|----------|
| `string` | Text values | Region, product name, status |
| `time` | Timestamps with granularity support | Created at, order date |
| `date` | Date values | Birth date, start date |
| `boolean` | True/false values | Is active, has subscription |
| `number` | Numeric values (non-aggregated) | Age, employee count |

### Time Granularities

Time dimensions can be grouped at different granularities:

| Granularity | Description | Example output |
|-------------|-------------|----------------|
| `DAY` | Daily | 2025-01-15 |
| `WEEK` | Weekly (start of week) | 2025-01-13 |
| `MONTH` | Monthly | 2025-01 |
| `QUARTER` | Quarterly | Q1 2025 |
| `YEAR` | Yearly | 2025 |

## Dimension Constraints for Charts

When writing chart prompts, be aware of these constraints on the underlying query:

| Dimensions | Time Dimensions | Total | Measures Allowed |
|------------|-----------------|-------|------------------|
| 0 | 0 | 0 | Multiple |
| 1 | 0 | 1 | Multiple |
| 0 | 1 | 1 | Multiple |
| 2 | 0 | 2 | Exactly 1 |
| 1 | 1 | 2 | Exactly 1 |

- Time dimensions count toward the total dimension count
- With 2 total dimensions, the second dimension is pivoted into series on the chart
- Maximum 2 total dimensions for charts

These constraints are enforced by the backend — if your chart prompt implies more than 2 dimensions, the LLM will simplify. But knowing these limits helps you write better prompts.

## Filter Concepts

When writing prompts for `update_chart_block` or `update_query_block`, you can express filters in natural language. The LLM translates them to the appropriate filter types:

- **Value filters**: "only active customers", "where region is North America"
- **Time filters**: "for the last 12 months", "year to date", "Q4 2025"
- **Comparison filters**: "where revenue > 1000", "with at least 5 orders"
- **Null checks**: "where email is set", "excluding empty values"
- **String matching**: "names starting with A", "containing 'enterprise'"
- **Composite filters**: "active customers in North America OR Europe"
- **Period-to-date**: "year to date", "quarter to date", "month to date"
- **Future ranges**: "next 3 months" (negative count internally)
- **Date ranges**: "between January 2025 and March 2025"

The query LLM also automatically applies customer and time range filters from the master's `sample_parameters` when relevant.

## Format Options

When creating custom measures with `edit_model`, you can specify display formats:

| Format | Description | Example output |
|--------|-------------|----------------|
| `percent` | Percentage | 45.2% |
| `currency` | Currency with symbol | $1,234.56 |
| `integer` | Whole number | 1,234 |
| `float` | Decimal number | 1,234.56 |

## Creating Custom Models and Measures

### Custom Models

Use `create_model` when existing models don't have the data you need:

```
create_model(
    source_model_name="orders",        -- existing model for DB connection
    model_name="monthly_summary",      -- name for new model
    sql="SELECT DATE_TRUNC('month', created_at) AS month, COUNT(*) AS order_count, SUM(amount) AS total FROM orders GROUP BY 1",
    column_descriptions=[
        {"name": "month", "description": "Order month"},
        {"name": "order_count", "description": "Number of orders"},
        {"name": "total", "description": "Total revenue"}
    ]
)
```

### Editing a Model — Custom Measures, Dimensions, and Deletion

Use `edit_model` to add computed measures, add computed dimensions, and/or delete existing measures/dimensions:

```
edit_model(
    model_name="orders",
    measures=[
        {
            "name": "active_count",
            "sql": "CASE WHEN status = 'active' THEN 1 ELSE 0 END",
            "type": "sum",
            "description": "Count of active orders"
        },
        {
            "name": "avg_order_value",
            "sql": "amount",
            "type": "avg",
            "format": "currency",
            "description": "Average order value"
        }
    ],
    dimensions=[
        {
            "name": "order_size_bucket",
            "sql": "CASE WHEN amount < 100 THEN 'Small' WHEN amount < 1000 THEN 'Medium' ELSE 'Large' END",
            "type": "string",
            "description": "Order size category"
        }
    ],
    delete_names=["old_measure", "unused_dimension"]
)
```

All parameters except `model_name` are optional — include only what you need.

## Tips for Master Building

1. **Always inspect models first**: Run `models_summary()` then `inspect_model(model_name=..., num_rows=3)` on relevant models before writing any prompts
2. **Know exact names**: Use the exact measure/dimension names from the schema in your prompts for clarity
3. **Check data quality**: Look at sample rows to understand value formats, null patterns, and data ranges
4. **Mention the model**: When writing prompts for `update_chart_block` or `update_query_block`, specify `cube_name` if you know which model to use — this constrains the LLM to that model's schema

## Related Documentation

- For exploring models: see the `explore-model` skill
- For creating queries within blocks: see the `update-query-block` skill

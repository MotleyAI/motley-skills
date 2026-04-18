---
name: explore-model
description: >
  Explore available models before building documents. Covers listing models,
  inspecting schemas, and creating custom models/measures.
---

# Explore Model

Explore available models to understand what data is available before building documents. This is typically the first step in any report creation workflow.

## Listing Models

Use `models_summary` to see all available models and their schemas:

```
models_summary()
```

Returns for each model:
- Model name
- Measures (with types: count, sum, avg, etc.)
- Dimensions (with types: string, time, date, boolean, number)
- Derived dimensions (computed columns)

For a compact overview (names only, no types/descriptions):
```
models_summary(verbose=false)
```

## Inspecting a Model

Use `inspect_model` to get detailed information including sample data:

```
inspect_model(
    model_name="revenue",
    num_rows=3,
    show_sql=false
)
```

Returns:
- Full schema (measures, dimensions, types)
- Sample data rows (to understand value formats and data quality)
- Optionally: the underlying SQL definition (`show_sql=true`)

**Tip**: Always inspect models relevant to your document before writing chart/query prompts. Knowing exact measure and dimension names leads to better results.

## Understanding Schemas

### Measures vs Dimensions

- **Measures** are aggregate values: things you count, sum, or average (revenue, order count, avg deal size)
- **Dimensions** are grouping columns: things you slice data by (region, product, status, time)
- **Derived dimensions** are computed from sub-queries: things like "week-over-week change" or "running total"

### Time Granularities

Time dimensions can be grouped at: `DAY`, `WEEK`, `MONTH`, `QUARTER`, `YEAR`

When writing prompts, specify the granularity you want (e.g., "monthly revenue", "quarterly breakdown").

For full details on data types and constraints, see [model-guide.md](../../shared/model-guide.md).

## Creating Custom Models

When existing models don't have the data you need, create a new model from a SQL query:

```
create_model(
    model_name="monthly_order_summary",
    sql="SELECT DATE_TRUNC('month', created_at) AS month, customer_id, COUNT(*) AS order_count, SUM(amount) AS total_amount FROM orders GROUP BY 1, 2",
    column_descriptions=[
        {"name": "month", "description": "Order month"},
        {"name": "customer_id", "description": "Customer identifier"},
        {"name": "order_count", "description": "Number of orders"},
        {"name": "total_amount", "description": "Total order value"}
    ],
    datasource_name="my_datasource"  -- optional if only one datasource exists
)
```

The new model:
- Uses the database connection from the specified datasource (or the only available one)
- Auto-detects column types (measures vs dimensions)
- Is immediately available for queries

## Editing a Model — Adding and Removing Measures/Dimensions

Use `edit_model` to add computed measures, add computed dimensions, and/or delete existing measures/dimensions on a model, all in a single call:

```
edit_model(
    model_name="orders",
    measures=[
        {
            "name": "large_order_count",
            "sql": "CASE WHEN amount >= 1000 THEN 1 ELSE 0 END",
            "type": "sum",
            "description": "Count of orders >= $1000"
        },
        {
            "name": "revenue_per_order",
            "sql": "amount",
            "type": "avg",
            "format": "currency",
            "description": "Average revenue per order"
        }
    ],
    dimensions=[
        {
            "name": "size_bucket",
            "sql": "CASE WHEN amount < 100 THEN 'Small' WHEN amount < 1000 THEN 'Medium' ELSE 'Large' END",
            "type": "string",
            "description": "Order size category"
        }
    ],
    delete_names=["old_measure", "unused_dimension"]
)
```

All parameters except `model_name` are optional — include only what you need:
- **measures** — list of measures to add (same format as before)
- **dimensions** — list of dimensions to add
- **delete_names** — list of measure/dimension names to remove

**Measure types**: `count`, `count_distinct`, `count_distinct_approx`, `sum`, `avg`, `min`, `max`, `number`

**Format options**: `percent`, `currency`, `integer`, `float`

**Dimension types**: `string`, `time`, `date`, `boolean`, `number`

## Tips for Report Building

1. **Start with `models_summary`** — get the big picture of available data
2. **Inspect relevant models** — `inspect_model` with `num_rows=3` to see real data
3. **Note exact names** — use precise measure/dimension names from the schema in your chart and query configurations
4. **Check for time dimensions** — if you need time series charts, confirm the model has a time dimension and what it's called
5. **Create models when needed** — if the data model doesn't fit, create a custom model from SQL rather than fighting with the existing schema
6. **Add measures for derived metrics** — if you need ratios, percentages, or conditional counts, add them as custom measures

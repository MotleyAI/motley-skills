---
name: explore-cube
description: >
  Explore available cubes before building masters. Covers listing cubes,
  inspecting schemas, and creating custom cubes/measures.
---

# Explore Cube

Explore available cubes to understand what data is available before building masters. This is typically the first step in any master-building workflow.

## Listing Cubes

Use `cubes_summary` to see all available cubes and their schemas:

```
cubes_summary()
```

Returns for each cube:
- Cube name
- Measures (with types: count, sum, avg, etc.)
- Dimensions (with types: string, time, date, boolean, number)
- Derived dimensions (computed columns)

## Inspecting a Cube

Use `inspect_cube` to get detailed information including sample data:

```
inspect_cube(
    cube_name="revenue",
    num_rows=3,
    show_sql=false
)
```

Returns:
- Full schema (measures, dimensions, types)
- Sample data rows (to understand value formats and data quality)
- Optionally: the underlying SQL definition (`show_sql=true`)

**Tip**: Always inspect cubes relevant to your master before writing chart/query prompts. Knowing exact measure and dimension names leads to better results.

## Understanding Schemas

### Measures vs Dimensions

- **Measures** are aggregate values: things you count, sum, or average (revenue, order count, avg deal size)
- **Dimensions** are grouping columns: things you slice data by (region, product, status, time)
- **Derived dimensions** are computed from sub-queries: things like "week-over-week change" or "running total"

### Time Granularities

Time dimensions can be grouped at: `DAY`, `WEEK`, `MONTH`, `QUARTER`, `YEAR`

When writing prompts, specify the granularity you want (e.g., "monthly revenue", "quarterly breakdown").

For full details on data types and constraints, see [cube-guide.md](../_shared/cube-guide.md).

## Creating Custom Cubes

When existing cubes don't have the data you need, create a new cube from a SQL query:

```
create_cube(
    source_cube_name="orders",
    cube_name="monthly_order_summary",
    sql="SELECT DATE_TRUNC('month', created_at) AS month, customer_id, COUNT(*) AS order_count, SUM(amount) AS total_amount FROM orders GROUP BY 1, 2",
    column_descriptions=[
        {"name": "month", "description": "Order month"},
        {"name": "customer_id", "description": "Customer identifier"},
        {"name": "order_count", "description": "Number of orders"},
        {"name": "total_amount", "description": "Total order value"}
    ]
)
```

The new cube:
- Uses the database connection from `source_cube_name`
- Auto-detects column types (measures vs dimensions)
- Is immediately available for queries

## Adding Custom Measures

Add computed measures to an existing cube:

```
add_measures(
    cube_name="orders",
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
    ]
)
```

**Measure types**: `count`, `count_distinct`, `count_distinct_approx`, `sum`, `avg`, `min`, `max`, `number`

**Format options**: `percent`, `currency`, `integer`, `float`

## Adding Custom Dimensions

Add computed dimensions to an existing cube:

```
add_dimensions(
    cube_name="orders",
    dimensions=[
        {
            "name": "size_bucket",
            "sql": "CASE WHEN amount < 100 THEN 'Small' WHEN amount < 1000 THEN 'Medium' ELSE 'Large' END",
            "type": "string",
            "description": "Order size category"
        }
    ]
)
```

**Dimension types**: `string`, `time`, `date`, `boolean`, `number`

## Removing Measures/Dimensions

Clean up unused or incorrect measures and dimensions:

```
delete_measures_dimensions(
    cube_name="orders",
    names=["old_measure", "unused_dimension"]
)
```

## Tips for Master Building

1. **Start with `cubes_summary`** — get the big picture of available data
2. **Inspect relevant cubes** — `inspect_cube` with `num_rows=3` to see real data
3. **Note exact names** — use precise measure/dimension names from the schema in your chart and query prompts
4. **Check for time dimensions** — if you need time series charts, confirm the cube has a time dimension and what it's called
5. **Create cubes when needed** — if the data model doesn't fit, create a custom cube from SQL rather than fighting with the existing schema
6. **Add measures for derived metrics** — if you need ratios, percentages, or conditional counts, add them as custom measures

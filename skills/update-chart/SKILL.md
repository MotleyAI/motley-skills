---
name: update-chart
description: >
  Create or modify charts using update_chart_block. Covers the structured
  direct-input interface with query and chart_details JSON.
---

# Update Chart

Create or modify chart blocks using the `update_chart_block` MCP tool. You provide a structured query and chart configuration, which are validated against Cube.js and rendered.

## How It Works

1. Call `update_chart_block` with a `query` (MinimalSemanticLayerQueryForLLM) and `chart_details` (ChartDetailsTemplate)
2. The query is validated against Cube.js
3. The chart configuration is applied and saved to the block (but NOT resolved immediately)
4. Call `render_chart` to see the rendered PNG (this also triggers resolution)

## Tool Signature

```
update_chart_block(
    location: {                # Optional — location of the chart block
        doc_id: int,           # The deck ID
        slide_name: str,       # The slide containing the chart block
        block_name: str        # The name of the chart block
    },
    query: {                   # Required — MinimalSemanticLayerQueryForLLM as JSON
        measures: [...],       # List of measures (e.g. [{name: "count", cube_name: "orders"}])
        dimensions: [...],     # List of dimensions
        time_dimension: {      # Singular object (NOT a list)
            dimension: str,    # e.g. "orders.created_at"
            granularity: str,  # e.g. "month"
            ...                # Optional time filter fields
        },
        filters: [...],        # Optional filters
        limit: int,            # Optional row limit
        order: [...]           # Optional ordering
    },
    chart_details: {           # Required — ChartDetailsTemplate as JSON
        title: str,            # Chart title
        series: {...},         # Series configuration
        y_axis: {...},         # Y-axis settings
        color_scheme: str,     # Optional color scheme
        ...
    },
    sample_values: {...},      # Optional: override filter values
    max_return_rows: int,      # Default: 20
    add_default_filters: bool  # Default: true
)
```

**Note:** `cube_name` is automatically derived from the query measures/dimensions — do not pass it.

**Returns**: Confirmation that the chart was updated plus a data preview. Does NOT return rendered output — use `render_chart` for that.

## Key Points

- **`time_dimension` is singular** — pass a single object, not a list called `time_dimensions`
- **No `cube_name` parameter** — it is auto-derived from the first measure or dimension in the query
- **`location` is optional** — omit it to create a transient chart without saving to any deck

## Chart Type Guidance

| Type | Best For | Example |
|------|----------|---------|
| **Bar** | Categorical comparisons, rankings, time series with few points | Revenue by region |
| **Line** | Trends over time, continuous data, multiple series comparison | Monthly active users over 12 months |
| **Pie** | Part-to-whole relationships (max 5-7 segments) | Revenue distribution by category |
| **Funnel** | Conversion stages, sequential process drop-off | Sales funnel from lead to closed deal |

### Tips

- **Bar vs Line**: Use bars for categorical comparisons or few time points. Use lines for trends with many time points.
- **Pie charts**: Only effective with 5-7 or fewer segments. For more categories, use a bar chart.
- **Dual axis**: Useful when comparing measures with different scales (e.g., revenue in dollars vs count of orders).
- **Stacked bars**: Use series configuration to set stacking mode.
- **Horizontal bars**: Set orientation in chart_details.

## Examples

### Time Series — Monthly Revenue
```
update_chart_block(
    location={doc_id: 42, slide_name: "Revenue Trends", block_name: "revenue_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "revenue"}],
        time_dimension: {
            dimension: "revenue.created_at",
            granularity: "month"
        }
    },
    chart_details={title: "Monthly Revenue", series_default: {type: "line"}}
)
```

### Categorical — Top Regions
```
update_chart_block(
    location={doc_id: 42, slide_name: "Regional Performance", block_name: "region_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "sales"}],
        dimensions: [{name: "region", cube_name: "sales"}],
        limit: 10,
        order: [{column: {name: "total_revenue", cube_name: "sales"}, direction: "desc"}]
    },
    chart_details={title: "Top 10 Regions by Revenue", series_default: {type: "bar"}}
)
```

### Pie — Distribution
```
update_chart_block(
    location={doc_id: 42, slide_name: "Breakdown", block_name: "pie_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "products"}],
        dimensions: [{name: "category", cube_name: "products"}],
        limit: 5
    },
    chart_details={title: "Revenue by Category", series_default: {type: "pie"}}
)
```

## Resolution Behavior

Charts are **NOT resolved immediately** after `update_chart_block`. The chart config is saved, but no data is fetched or rendered yet.

To see the chart:
- **Individual chart**: Call `render_chart(location={doc_id: ..., slide_name: ..., block_name: ...})` — this triggers resolution and returns a PNG image
- **Batch resolution**: Call `resolve_master(doc_id=...)` — resolves all outdated blocks in the master

## Verifying Charts

**Always call `render_chart` after `update_chart_block`** to visually verify the result.

```
render_chart(
    location={doc_id: 42, slide_name: "Revenue Trends", block_name: "revenue_chart"},
    width=800,
    height=600
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong chart type | Set `series_default.type` explicitly in chart_details |
| Missing data points | Check that the cube has data for the requested time range. Use `inspect_cube` to verify. |
| Too many categories | Add `limit` to the query |
| Wrong time granularity | Set `granularity` in `time_dimension` (month, quarter, week, etc.) |
| `list index out of range` | Ensure query has at least one dimension or time_dimension for the x-axis |

## Related Skills

- For exploring cubes before writing queries: see the `explore-cube` skill
- For understanding cube schemas: see [cube-guide.md](../_shared/cube-guide.md)

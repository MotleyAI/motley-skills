---
name: update-chart
description: >
  Create or modify charts using update_chart_block. Covers writing effective
  natural language prompts for bar, line, pie, and funnel charts.
---

# Update Chart

Create or modify chart blocks using the `update_chart_block` MCP tool. You provide a natural language prompt, and an LLM internally generates the full chart configuration (query, chart type, series, axes, formatting).

## How It Works

You do NOT construct chart objects, queries, or series configs. Instead:
1. Call `update_chart_block` with a descriptive `prompt`
2. An LLM generates the complete chart — query, type, axes, series, colors, legend
3. The chart is saved to the block but NOT resolved immediately
4. Call `render_chart` to see the rendered PNG (this also triggers resolution)

## Tool Signature

```
update_chart_block(
    location: {                # Location of the chart block
        doc_id: int,           # The deck ID
        slide_name: str,       # The slide containing the chart block
        block_name: str        # The name of the chart block
    },
    prompt: str,               # Natural language description of the desired chart
    cube_name: str?            # Optional: constrain to this cube only
)
```

**Returns**: Confirmation that the chart was updated. Does NOT return rendered output — use `render_chart` for that.

## Writing Effective Prompts

Be specific about these aspects in your prompt:

- **Chart type**: "bar chart", "line chart", "pie chart", "funnel chart"
- **Measure(s)**: "total revenue", "count of orders", "average session duration"
- **Dimension(s)**: "by region", "over time monthly", "by product category"
- **Time range**: "for the last 12 months", "year to date", "last 4 quarters"
- **Ordering/limit**: "top 10 by revenue", "sorted chronologically"
- **Dual axis**: "revenue on left axis, count on right axis"
- **Period comparison**: "compare to same period last year"
- **Filters**: "for active customers only", "excluding test accounts"

The chart LLM automatically applies customer and time filters from the master's `sample_parameters`.

## Chart Type Guidance

| Type | Best For | Example |
|------|----------|---------|
| **Bar** | Categorical comparisons, rankings, time series with few points | "Revenue by region as a bar chart" |
| **Line** | Trends over time, continuous data, multiple series comparison | "Monthly active users over the last 12 months as a line chart" |
| **Pie** | Part-to-whole relationships, distribution (use sparingly, max 5-7 segments) | "Revenue distribution by product category as a pie chart" |
| **Funnel** | Conversion stages, sequential process drop-off | "Sales funnel from lead to closed deal" |

### Tips

- **Bar vs Line**: Use bars for categorical comparisons or few time points. Use lines for trends with many time points.
- **Pie charts**: Only effective with 5-7 or fewer segments. For more categories, use a bar chart.
- **Dual axis**: Useful when comparing measures with different scales (e.g., revenue in dollars vs count of orders).
- **Stacked bars**: Request "stacked bar chart" when showing composition over categories.
- **Horizontal bars**: Request "horizontal bar chart" for long category labels or ranking displays.

## Prompt Examples

### Time Series — Monthly Revenue
```
update_chart_block(
    location={doc_id: 42, slide_name: "Revenue Trends", block_name: "revenue_chart"},
    prompt="Line chart showing monthly total revenue for the last 12 months",
    cube_name="revenue"
)
```

### Categorical — Top Regions
```
update_chart_block(
    location={doc_id: 42, slide_name: "Regional Performance", block_name: "region_chart"},
    prompt="Horizontal bar chart of total revenue by region, top 10, sorted descending",
    cube_name="sales"
)
```

### Period Comparison — Year over Year
```
update_chart_block(
    location={doc_id: 42, slide_name: "YoY Comparison", block_name: "yoy_chart"},
    prompt="Bar chart of monthly revenue for the last 12 months, compared to the same period last year",
    cube_name="revenue"
)
```

### Dual Axis — Revenue vs Count
```
update_chart_block(
    location={doc_id: 42, slide_name: "Overview", block_name: "dual_chart"},
    prompt="Monthly chart with revenue as bars on the left axis and order count as a line on the right axis, last 12 months",
    cube_name="orders"
)
```

### Pie — Distribution
```
update_chart_block(
    location={doc_id: 42, slide_name: "Breakdown", block_name: "pie_chart"},
    prompt="Pie chart showing revenue distribution by product category, top 5 categories with the rest grouped as Other",
    cube_name="products"
)
```

### Funnel — Conversion
```
update_chart_block(
    location={doc_id: 42, slide_name: "Sales Funnel", block_name: "funnel_chart"},
    prompt="Funnel chart showing the count at each stage: Lead, Qualified, Proposal, Negotiation, Closed Won",
    cube_name="deals"
)
```

### Stacked Bar — Composition Over Time
```
update_chart_block(
    location={doc_id: 42, slide_name: "Mix Analysis", block_name: "stacked_chart"},
    prompt="Stacked bar chart of monthly revenue broken down by product category for the last 6 months",
    cube_name="revenue"
)
```

### Two Measures — Side by Side
```
update_chart_block(
    location={doc_id: 42, slide_name: "Efficiency", block_name: "comparison_chart"},
    prompt="Grouped bar chart comparing total revenue and total cost by quarter for the last 4 quarters",
    cube_name="financials"
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

Check the returned image for:
- Correct chart type
- Appropriate axis labels and scales
- Data looks reasonable (no obviously wrong values)
- Legend is readable
- Time series is in chronological order

If the chart doesn't look right, call `update_chart_block` again with a refined prompt.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong chart type | Be explicit: "as a bar chart", "as a line chart" |
| Missing data points | Check that the cube has data for the requested time range. Use `inspect_cube` to verify. |
| Too many categories | Add "top N" or "limit to N" to your prompt |
| Wrong time granularity | Specify: "monthly", "quarterly", "weekly" |
| Axis scale issues | Mention "use logarithmic scale" or "dual axis with right axis for counts" |
| Period comparison not working | Ensure the cube has enough historical data for the comparison period |
| Wrong cube | Specify `cube_name` explicitly to constrain the LLM |

## Related Skills

- For exploring cubes before writing prompts: see the `explore-cube` skill
- For understanding cube schemas: see [cube-guide.md](../_shared/cube-guide.md)

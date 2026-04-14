# Model Tools

Tools for working with models - listing, inspecting, and modifying their schemas.

[Back to Tools Overview](../tools.md)

---

## models_summary

List all available models with their dimensions, measures, and derived dimensions.

### Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `verbose` | boolean | `true` | If true, show full tables with type and description. If false, show comma-separated names only. |

### Returns

Markdown-formatted summary of all models. For each model:
- Model name and description
- `source_id`
- **Dimensions**, **Measures**, and **Derived dimensions** -- as tables (verbose) or comma-separated name lists (compact)

### Notes

- Does **not** include sample data - use `inspect_model` for that
- Use this tool to discover available models and their schemas
- Use `verbose=false` for a quick overview when you already know the model schemas

---

## inspect_model

Get detailed information about a specific model including sample data.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | **Yes** | Exact name of the model to inspect. |
| `num_rows` | integer | No | Number of sample rows to include. Default: 3. |
| `show_sql` | boolean | No | Include the SQL query/table definition. Default: false. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Model name |
| `description` | string | Model description |
| `dimensions` | array | Dimension definitions with `name`, `type`, `description` |
| `measures` | array | Measure definitions with `name`, `type`, `description` |
| `derived_dimensions` | array | Derived dimension definitions with `name`, `expression`, `description` |
| `extended_summary` | string | Formatted summary including sample data |
| `sql` | string | SQL query (only if `show_sql=true`) |
| `sql_table` | string | Table name (only if `show_sql=true`) |
| `sample_data_error` | string | Error message if sample data fetch failed |

---

## create_model

Create a new model from a SQL SELECT query.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_model_name` | string | **Yes** | Existing model whose database connection is used for introspection. This becomes the `data_source` on the new model. |
| `model_name` | string | **Yes** | Name for the new model being created. |
| `sql` | string | **Yes** | A valid SQL SELECT query. Column types are introspected from the database. |
| `column_descriptions` | array[object] | No | Per-column descriptions. Each entry has `name` (column name) and `description` (human-readable text). Not every column needs a description. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `model_name` | string | Name of the created model |
| `source_model_name` | string | The model used for database connection |
| `dimensions` | array | Auto-generated dimensions from the query |
| `measures` | array | Auto-generated measures from the query |

### Notes

- Column types are automatically introspected from the database
- Dimensions and measures are inferred based on column types
- The `source_model_name` parameter specifies which existing model's database connection to use

---

## edit_model

Add or delete measures, dimensions, and derived dimensions on an existing model in a single operation.

### Arguments

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | **Yes** | The model to modify. |
| `measures` | array[MeasureSpec] | No | List of measure specifications to add. |
| `dimensions` | array[DimensionSpec] | No | List of dimension specifications to add. |
| `delete_names` | array[string] | No | Names of measures, dimensions, or derived dimensions to delete. |

Each **MeasureSpec** contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | **Yes** | Measure identifier. Must not already exist on the model. |
| `sql` | string | **Yes** | SQL expression (e.g., `"CASE WHEN status = 'active' THEN 1 ELSE 0 END"`). |
| `type` | string | **Yes** | Aggregation type. One of: `count`, `count_distinct`, `count_distinct_approx`, `sum`, `avg`, `min`, `max`, `number`. |
| `description` | string | No | Human-readable description. |
| `format` | string | No | Display format: `percent`, `currency`, `integer`, `float`. |
| `currency_symbol` | string | No | Currency symbol when `format='currency'`. Defaults to `'$'`. |

Each **DimensionSpec** contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | **Yes** | Dimension identifier. Must not already exist on the model. |
| `sql` | string | **Yes** | SQL expression for the dimension. |
| `type` | string | **Yes** | Data type. One of: `string`, `time`, `date`, `boolean`, `number`. |
| `description` | string | No | Human-readable description. |

### Returns

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `model_name` | string | The model that was modified |
| `added_measures` | array | List of added measures with `name`, `type`, `sql` |
| `added_dimensions` | array | List of added dimensions with `name`, `type`, `sql` |
| `deleted` | array | List of deleted items with `name` and `kind` |
| `message` | string | Summary message |

### Valid Measure Types

| Type | Description |
|------|-------------|
| `count` | Count of rows |
| `count_distinct` | Count of distinct values |
| `count_distinct_approx` | Approximate distinct count (faster) |
| `sum` | Sum of values |
| `avg` | Average of values |
| `min` | Minimum value |
| `max` | Maximum value |
| `number` | Raw number (no aggregation) |

### Valid Dimension Types

| Type | Description |
|------|-------------|
| `string` | Text values |
| `time` | Timestamp/datetime values |
| `date` | Date values (no time component) |
| `boolean` | True/false values |
| `number` | Numeric values |

### Notes

- At least one of `measures`, `dimensions`, or `delete_names` must be provided
- For deletions, the tool searches measures first, then dimensions, then derived dimensions
- If a name in `delete_names` is not found in any category, an error is raised

---
name: layout-library-sync
description: Import a Google Slides presentation as a layout library, create a master from it, and sync element content from a reference master by matching similar slides.
---

# Layout Library Import and Sync Workflow

This skill guides you through importing a Google Slides presentation as a layout library, creating a master from it, and syncing content from an existing reference master.

## Overview

The workflow consists of these steps:
1. **Import** a Google Slides presentation as a layout library
2. **Create** a master from the layout library
3. **Match** slides between the new master and a reference master
4. **For each matched slide**: unhide it and copy element content from the reference

---

## Step 1: Import Layout Library

Use `import_layout_library` to import a Google Slides presentation.

**Tool**: `import_layout_library`

**Parameters**:
- `presentation_url` (required): Google Slides URL or presentation ID
- `name` (required): Name for the layout library

**Example**:
```
import_layout_library(
    presentation_url="https://docs.google.com/presentation/d/1G5UFoE9U_DMtuMqeG_WQ1oWF-I4NR5AK3koAZw1ye58/edit",
    name="Q1 Report Template"
)
```

**Returns**:
- `layout_library_id`: Use this to create a master
- `deck_id`: The underlying deck ID
- `slide_count`: Number of slides imported

**Notes**:
- The presentation is copied to the user's Google Drive
- All slides and elements are automatically named using LLM
- This may take 30-60 seconds depending on presentation size

---

## Step 2: Create Master from Layout Library

Use `create_master` to create an editable master from the layout library.

**Tool**: `create_master`

**Parameters**:
- `layout_library_id` (required): From step 1
- `name` (optional): Custom name for the master

**Example**:
```
create_master(
    layout_library_id=<layout_library_id from step 1>,
    name="Q1 Report Master"
)
```

**Returns**:
- `master_id`: Use this for all subsequent operations
- `deck_id`: The master's deck ID
- All slides are created **hidden** by default

---

## Step 3: Match Slides with Reference Master

Use `match_slides` to find corresponding slides between your new master and a reference master.

**Tool**: `match_slides`

**Parameters**:
- `source_master_id` (required): The new master from step 2
- `target_master_id` (required): The reference master with existing content
- `slide_name` (optional): Match only a specific slide
- `include_thumbnails` (optional): Use thumbnail comparison (slower)

**Example**:
```
match_slides(
    source_master_id=<new_master_id>,
    target_master_id=1  # Reference master
)
```

**Returns**:
- `matches`: List of matched slide pairs with:
  - `source_slide_name`: Slide in new master
  - `target_slide_name`: Corresponding slide in reference
  - `similarity_score`: 0.0-1.0 confidence score
  - `match_reason`: "exact_name_match" or "element_overlap"
  - `element_matches`: Matched elements between slides
- `unmatched_source_slides`: Slides in new master with no match
- `unmatched_target_slides`: Slides in reference with no match

**Matching Algorithm**:
1. **Exact name match**: Slides with identical names (score=1.0)
2. **Element overlap**: Jaccard similarity of element names (threshold: 0.3)

---

## Step 4: Process Each Matched Slide

For each match, perform these operations:

### 4a. Unhide the Slide

Use `update_slide` to make the slide visible.

**Tool**: `update_slide`

**Parameters**:
- `master_id` (required): The new master ID
- `slide_name` (required): Name of the slide to update
- `hidden` (optional): Set to `false` to show the slide
- `new_name` (optional): Rename the slide
- `description` (optional): Update slide description

**Example**:
```
update_slide(
    master_id=<new_master_id>,
    slide_name="Intro",
    hidden=false
)
```

### 4b. Copy Element Content

Use `copy_block_content` to copy content from reference slide elements.

**Tool**: `copy_block_content`

**Parameters**:
- `source_master_id` (required): Reference master ID
- `source_slide_name` (required): Slide name in reference
- `source_block_name` (required): Element name to copy from
- `target_master_id` (required): New master ID
- `target_slide_name` (required): Slide name in new master
- `target_block_name` (required): Element name to copy to
- `copy_template` (optional, default=true): Copy templates
- `copy_queries` (optional, default=true): Copy nested queries

**Example**:
```
copy_block_content(
    source_master_id=1,  # Reference
    source_slide_name="Intro",
    source_block_name="title",
    target_master_id=<new_master_id>,
    target_slide_name="Intro",
    target_block_name="title"
)
```

**Notes**:
- If block types differ, the target is automatically converted to match the source type while preserving its layout properties (width, height, placeholder, description)
- Target block is marked as out-of-date after copy

---

## Complete Workflow Example

```python
# Step 1: Import the presentation
result = import_layout_library(
    presentation_url="https://docs.google.com/presentation/d/1G5UFoE9U_DMtuMqeG_WQ1oWF-I4NR5AK3koAZw1ye58/edit",
    name="New Template"
)
library_id = result["layout_library_id"]

# Step 2: Create master
master_result = create_master(
    layout_library_id=library_id,
    name="New Template Master"
)
new_master_id = master_result["master_id"]

# Step 3: Match slides with reference master (deck_id=1)
matches_result = match_slides(
    source_master_id=new_master_id,
    target_master_id=1  # Reference master ID
)

# Step 4: Process each match
for match in matches_result["matches"]:
    source_slide = match["source_slide_name"]
    target_slide = match["target_slide_name"]

    # 4a: Unhide the slide
    update_slide(
        master_id=new_master_id,
        slide_name=source_slide,
        hidden=false
    )

    # 4b: Copy each matched element
    for elem_match in match["element_matches"]:
        copy_block_content(
            source_master_id=1,
            source_slide_name=target_slide,
            source_block_name=elem_match["target_element"],
            target_master_id=new_master_id,
            target_slide_name=source_slide,
            target_block_name=elem_match["source_element"]
        )

# Step 5: Resolve to populate content
resolve_master(master_id=new_master_id)
```

---

## Useful Related Tools

- `list_layout_libraries`: List all available layout libraries
- `list_masters`: List all masters
- `inspect_layout_library`: See structure of a layout library
- `get_master_summary`: See structure of a master
- `inspect_slide`: Get detailed slide content
- `resolve_master`: Trigger resolution of outdated blocks

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Layout library not found" | Invalid ID or no access | Verify library ID exists |
| "Slide not found" | Slide name doesn't exist | Use `get_master_summary` to list slides |
| "Block types incompatible" | Deprecated — type conversion is now automatic | Target block is converted to match source type |
| "Master not found" | Invalid master ID | Use `list_masters` to find valid IDs |

---

## Best Practices

1. **Always check matches first**: Review `match_slides` results before copying
2. **Handle unmatched slides**: Decide what to do with slides that don't match
3. **Copy templates**: Keep `copy_template=true` to preserve formatting rules
4. **Resolve after copying**: Call `resolve_master` to update content after copies
5. **Batch operations**: Process all matched slides before resolving once

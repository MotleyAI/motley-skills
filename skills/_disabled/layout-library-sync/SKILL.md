---
name: layout-library-sync
description: >
  Import a Google Slides presentation as a layout library, create a master
  from it, and sync element content from a reference master.
---

# Layout Library Import and Sync Workflow

This skill guides you through importing a Google Slides presentation as a layout library, creating a master from it, and syncing content from an existing reference master.

## Overview

The workflow consists of these steps:
1. **Import** a Google Slides presentation as a layout library
2. **Create** a master from the layout library
3. **Match** slides between the new master and a reference master
4. **For each matched slide**: unhide it and copy element content from the reference
5. **Resolve** to populate content

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
- `source_doc_id` (required): The new master's deck ID from step 2
- `target_doc_id` (required): The reference master's deck ID with existing content
- `slide_name` (optional): Match only a specific slide
- `include_thumbnails` (optional): Use thumbnail comparison (slower)

**Example**:
```
match_slides(
    source_doc_id=<new_master_deck_id>,
    target_doc_id=<reference_deck_id>
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

```
update_slide(
    doc_id=<new_master_deck_id>,
    slide_name="Intro",
    hidden=false
)
```

### 4b. Copy Element Content

For each matched element pair:

```
copy_block(
    source={doc_id: <reference_deck_id>, slide_name: "Intro", block_name: "title"},
    target={doc_id: <new_master_deck_id>, slide_name: "Intro", block_name: "title"}
)
```

**Notes**:
- If block types differ, the target is automatically converted to match the source type while preserving its layout properties (width, height, placeholder, description)
- Templates are always copied; child queries are never copied
- For query blocks, use `parent_block_name` to attach the copied query to a parent block
- Target block is marked as out-of-date after copy

---

## Complete Workflow

1. **Import** the presentation:
   ```
   import_layout_library(presentation_url="https://docs.google.com/...", name="New Template")
   ```
   → Record `layout_library_id`

2. **Create** master:
   ```
   create_master(layout_library_id=<library_id>, name="New Template Master")
   ```
   → Record `master_id` and `deck_id`

3. **Match** slides with reference:
   ```
   match_slides(source_doc_id=<new_deck_id>, target_doc_id=<reference_deck_id>)
   ```
   → Get list of matches

4. **For each match**: unhide the slide and copy each matched element:
   ```
   update_slide(doc_id=<new_deck_id>, slide_name=<source_slide_name>, hidden=false)

   copy_block(
       source={doc_id: <reference_deck_id>, slide_name: <target_slide_name>, block_name: <target_element>},
       target={doc_id: <new_deck_id>, slide_name: <source_slide_name>, block_name: <source_element>}
   )
   ```
   Repeat `copy_block` for each element match in the slide.

5. **Resolve** to populate content:
   ```
   resolve_master(doc_id=<new_deck_id>)
   ```

---

## Useful Related Tools

- `list_layout_libraries`: List all available layout libraries
- `list_masters`: List all masters
- `inspect_layout_library`: See structure of a layout library
- `get_doc_summary`: See structure of a master
- `inspect_slide`: Get detailed slide content
- `resolve_master`: Trigger resolution of outdated blocks

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Layout library not found" | Invalid ID or no access | Verify library ID exists |
| "Slide not found" | Slide name doesn't exist | Use `get_doc_summary` to list slides |
| "Block types incompatible" | Deprecated — type conversion is now automatic | Target block is converted to match source type |
| "Master not found" | Invalid master ID | Use `list_masters` to find valid IDs |

---

## Best Practices

1. **Always check matches first**: Review `match_slides` results before copying
2. **Handle unmatched slides**: Decide what to do with slides that don't match
3. **Templates are always copied**: Templates are automatically preserved during copy
4. **Resolve after copying**: Call `resolve_master` to update content after all copies
5. **Batch operations**: Process all matched slides before resolving once

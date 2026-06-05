# Zotero Reference Search

This template includes `.github/workflows/zotero-reference-search.yml` and `scripts/zotero_search.py`. When a new repository is created with GitHub `Use this template`, these files are copied into the new repository.

## Recommended Input

Prefer collection/folder extraction when the relevant papers are already grouped in Zotero.

```text
case_id: case_report_001
reference_source: collection
zotero_collection_names: <Zotero collection/folder name>
zotero_collection_key:
search_keywords: renal trauma urinary extravasation pediatric
max_results: 50
debug: true
```

## Input Fields

- `case_id`: Output folder under `manuscripts/{case_id}/generated/`.
- `reference_source`: Use `collection` for Zotero folders, `keyword` for full-library keyword search, or `auto` to try collection first and fall back to keyword search.
- `zotero_collection_names`: Zotero collection/folder names, separated by commas or new lines. Exact matches are preferred; partial matches are attempted if exact matching fails.
- `zotero_collection_key`: Zotero collection key or keys. Use this when known; it is more stable than a folder name.
- `search_keywords`: Optional in collection mode. Used for fallback search and evidence/PDF scoring, not for excluding collection items.
- `max_results`: Maximum number of citable Zotero items to extract.
- `debug`: Writes detailed diagnostics.

## Outputs

The workflow writes shared reference outputs:

```text
references/zotero_search_results.md
references/citation_evidence_cards.md
references/pdf_fulltext_review.md
```

It also writes case-specific outputs:

```text
manuscripts/{case_id}/generated/zotero_collection_inventory.md
manuscripts/{case_id}/generated/zotero_api_diagnostics.md
manuscripts/{case_id}/generated/zotero_search_results.md
manuscripts/{case_id}/generated/citation_evidence_cards.md
manuscripts/{case_id}/generated/pdf_fulltext_review.md
manuscripts/{case_id}/generated/02_zotero_search_results.md
manuscripts/{case_id}/generated/03_selected_references.md
manuscripts/{case_id}/generated/08_notes_for_revision.md
```

## Troubleshooting

If evidence cards are empty, inspect `zotero_api_diagnostics.md` first.

Common causes:

- Required GitHub secrets are missing: `ZOTERO_API_KEY`, `ZOTERO_USER_ID`.
- The folder name did not match a Zotero collection.
- The selected collection contains only attachments or notes, not citable parent items.
- `reference_source` was set to `keyword` and the keyword string was too specific.

Use `zotero_collection_inventory.md` to copy the exact collection key or exact collection/folder name for the next run.

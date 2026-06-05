#!/usr/bin/env python3
"""Extract Zotero references from collections or keyword search."""

from __future__ import annotations

import argparse
import os
import sys
import traceback
from pathlib import Path
from typing import Any

import requests

AUTO_HEADER = "<!-- AUTO-GENERATED FILE. DO NOT EDIT MANUALLY. -->"
BASE_URL = "https://api.zotero.org"
REDACTED = "[REDACTED]"


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def split_values(value: str) -> list[str]:
    normalized = value.replace("\r", "\n").replace(",", "\n")
    return [part.strip() for part in normalized.split("\n") if part.strip()]


def write_file(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{AUTO_HEADER}\n\n{body}", encoding="utf-8")


def sanitize(note: str, secrets: list[str]) -> str:
    out = note
    for secret in secrets:
        if secret:
            out = out.replace(secret, REDACTED)
    return out


def clean(params: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v not in {None, ""}}


def root(library_type: str, user_id: str) -> str:
    return f"{BASE_URL}/{library_type}s/{user_id}"


def api_get(url: str, params: dict[str, Any], headers: dict[str, str]) -> requests.Response:
    return requests.get(url, params=clean(params), headers=headers, timeout=30)


def get_all(url: str, params: dict[str, Any], headers: dict[str, str], max_items: int) -> tuple[list[dict[str, Any]], list[tuple[str, str, int, str]]]:
    items: list[dict[str, Any]] = []
    statuses: list[tuple[str, str, int, str]] = []
    start = 0
    while len(items) < max_items:
        limit = min(100, max_items - len(items))
        response = api_get(url, {**params, "start": start, "limit": limit}, headers)
        status = f"{response.status_code} {response.reason}"
        if response.status_code >= 400:
            statuses.append((f"GET {url}", status, len(items), response.text[:1000]))
            break
        page = response.json()
        statuses.append((f"GET {url} start={start}", status, len(page), ""))
        if not page:
            break
        items.extend(page)
        if len(page) < limit:
            break
        start += len(page)
    return items, statuses


def citable(item: dict[str, Any]) -> bool:
    return item.get("data", {}).get("itemType") not in {"attachment", "note"}


def meta(item: dict[str, Any]) -> dict[str, Any]:
    data = item.get("data", {})
    authors = []
    for creator in data.get("creators") or []:
        name = " ".join(x for x in [creator.get("firstName", ""), creator.get("lastName", "")] if x).strip()
        if name:
            authors.append(name)
    return {
        "key": data.get("key", ""),
        "type": data.get("itemType", ""),
        "title": data.get("title", ""),
        "authors": authors,
        "year": (data.get("date", "") or "")[:4],
        "journal": data.get("publicationTitle", ""),
        "volume": data.get("volume", ""),
        "issue": data.get("issue", ""),
        "pages": data.get("pages", ""),
        "doi": data.get("DOI", ""),
        "pmid": data.get("PMID", ""),
        "url": data.get("url", ""),
        "abstract": data.get("abstractNote", ""),
    }


def collection_name(collection: dict[str, Any]) -> str:
    return collection.get("data", {}).get("name", "")


def collection_key(collection: dict[str, Any]) -> str:
    return collection.get("data", {}).get("key", "")


def resolve_names(names: list[str], collections: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    notes: list[str] = []
    for name in names:
        target = name.lower().strip()
        exact = [c for c in collections if collection_name(c).lower().strip() == target]
        matches = exact or [c for c in collections if target in collection_name(c).lower().strip()]
        keys = [collection_key(c) for c in matches if collection_key(c)]
        if keys:
            resolved.extend(keys)
            match_type = "exact" if exact else "partial"
            notes.append(f"`{name}` resolved by {match_type} match to: {', '.join(keys)}")
        else:
            notes.append(f"`{name}` did not match any Zotero collection.")
    return list(dict.fromkeys(resolved)), notes


def strength(item: dict[str, Any], keywords: str, from_collection: bool) -> str:
    if from_collection:
        return "High"
    m = meta(item)
    haystack = " ".join([m["title"], m["abstract"], m["journal"]]).lower()
    tokens = [t.lower() for t in keywords.split() if t.strip()]
    hits = sum(1 for token in tokens if token in haystack)
    if hits >= 3:
        return "High"
    if hits >= 1:
        return "Moderate"
    return "Low"


def format_ref(item: dict[str, Any], index: int, evidence: str, source: str) -> str:
    m = meta(item)
    authors = ", ".join(m["authors"]) or "Author not available"
    return "\n".join([
        f"## {index}. {m['title'] or 'Title not available'}", "",
        f"- Zotero key: {m['key']}",
        f"- Item type: {m['type']}",
        f"- Authors: {authors}",
        f"- Year: {m['year'] or 'Not available'}",
        f"- Journal: {m['journal'] or 'Not available'}",
        f"- Volume: {m['volume'] or 'Not available'}",
        f"- Issue: {m['issue'] or 'Not available'}",
        f"- Pages: {m['pages'] or 'Not available'}",
        f"- DOI: {m['doi'] or 'Not available'}",
        f"- PMID: {m['pmid'] or 'Not available'}",
        f"- URL: {m['url'] or 'Not available'}",
        f"- Evidence strength: {evidence}",
        f"- Evidence source: {source}",
        "- Recommended use: Use only if the manuscript claim is supported by Zotero metadata, abstract, or confirmed full text.", "",
        "### Abstract Or Zotero Note", "", m["abstract"] or "Not available from Zotero API.", "",
    ])


def diagnostics(statuses: list[tuple[str, str, int, str]], collection_keys: list[str], collection_names: list[str], notes: list[str], source: str, debug: bool, missing: str | None, exception: str | None = None) -> str:
    lines = [
        "# Zotero API Diagnostics", "",
        f"- API access status: {'Blocked' if missing else 'Needs review' if exception else 'OK'}",
        f"- Reference source: {source}",
        f"- Diagnostic status: {'Debug enabled' if debug else 'Debug disabled'}",
        f"- Collection keys requested/resolved: {', '.join(collection_keys) if collection_keys else 'None'}",
        f"- Collection names requested: {', '.join(collection_names) if collection_names else 'None'}", "",
    ]
    if missing:
        lines.append(f"- Estimated cause: {missing}")
        lines.append("- Next action: Set required GitHub Secrets and rerun the workflow.")
    elif exception:
        lines.extend(["## Exception", "", "```text", exception[:4000], "```", ""])
    if notes:
        lines.extend(["## Collection Name Resolution", ""])
        lines.extend(f"- {note}" for note in notes)
        lines.append("")
    lines.extend(["## Tests And Fetches", ""])
    for label, status, count, error in statuses:
        lines.append(f"- {label}: {status}; items returned: {count}")
        if debug and error:
            lines.append(f"  - Error excerpt: {error[:1000]}")
    return "\n".join(lines) + "\n"


def inventory(collections: list[dict[str, Any]]) -> str:
    lines = ["# Zotero Collection Inventory", "", "Use exact collection/folder names or collection keys in the workflow input.", ""]
    for collection in sorted(collections, key=lambda c: collection_name(c).lower()):
        lines.append(f"- {collection_name(collection) or 'Untitled'}: `{collection_key(collection)}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--reference-source", default="collection", choices=["collection", "keyword", "auto"])
    parser.add_argument("--search-keywords", default="")
    parser.add_argument("--zotero-collection-key", default="")
    parser.add_argument("--zotero-collection-names", default="")
    parser.add_argument("--max-results", default="50")
    parser.add_argument("--debug", default="true")
    args = parser.parse_args()

    api_key = os.environ.get("ZOTERO_API_KEY", "").strip()
    user_id = os.environ.get("ZOTERO_USER_ID", "").strip()
    library_type = (os.environ.get("ZOTERO_LIBRARY_TYPE", "user") or "user").strip()
    env_collection_key = os.environ.get("ZOTERO_COLLECTION_KEY", "")
    collection_keys = split_values(args.zotero_collection_key or env_collection_key)
    collection_names = split_values(args.zotero_collection_names)
    max_results = max(1, int(args.max_results))
    debug = parse_bool(args.debug)
    generated_dir = Path("manuscripts") / args.case_id / "generated"
    references_dir = Path("references")
    secrets = [api_key]

    missing = "; ".join(name for name, value in [("ZOTERO_API_KEY is not set", api_key), ("ZOTERO_USER_ID is not set", user_id)] if not value)
    if missing:
        write_file(generated_dir / "zotero_api_diagnostics.md", diagnostics([], collection_keys, collection_names, [], args.reference_source, debug, missing))
        print("Zotero API extraction skipped because required secrets are missing.")
        return 0

    headers = {"Zotero-API-Version": "3", "Zotero-API-Key": api_key}
    statuses: list[tuple[str, str, int, str]] = []
    resolution_notes: list[str] = []
    items_by_key: dict[str, dict[str, Any]] = {}
    source_by_key: dict[str, str] = {}
    try:
        collections, collection_statuses = get_all(f"{root(library_type, user_id)}/collections", {}, headers, 1000)
        statuses.extend((label, status, count, sanitize(error, secrets)) for label, status, count, error in collection_statuses)
        write_file(generated_dir / "zotero_collection_inventory.md", inventory(collections))
        if collection_names:
            resolved, resolution_notes = resolve_names(collection_names, collections)
            collection_keys = list(dict.fromkeys(collection_keys + resolved))
        if args.reference_source in {"collection", "auto"} and collection_keys:
            for key in collection_keys:
                fetched, fetch_statuses = get_all(f"{root(library_type, user_id)}/collections/{key}/items", {"itemType": "-attachment"}, headers, max_results)
                statuses.extend((f"Collection {key}: {label}", status, count, sanitize(error, secrets)) for label, status, count, error in fetch_statuses)
                for item in fetched:
                    if not citable(item):
                        continue
                    m = meta(item)
                    items_by_key[m["key"]] = item
                    source_by_key[m["key"]] = f"Zotero collection `{key}`"
        if not items_by_key and args.reference_source in {"keyword", "auto"}:
            response = api_get(f"{root(library_type, user_id)}/items", {"q": args.search_keywords, "qmode": "everything", "limit": max_results, "itemType": "-attachment"}, headers)
            status = f"{response.status_code} {response.reason}"
            if response.status_code >= 400:
                statuses.append(("Keyword search", status, 0, sanitize(response.text[:1000], secrets)))
            else:
                fetched = [item for item in response.json() if citable(item)]
                statuses.append(("Keyword search", status, len(fetched), ""))
                for item in fetched:
                    m = meta(item)
                    items_by_key[m["key"]] = item
                    source_by_key[m["key"]] = "Zotero keyword search"
    except Exception:
        note = sanitize(traceback.format_exc(), secrets)
        write_file(generated_dir / "zotero_api_diagnostics.md", diagnostics(statuses, collection_keys, collection_names, resolution_notes, args.reference_source, debug, None, note))
        print("Zotero API extraction failed before completion.")
        return 0

    items = list(items_by_key.values())[:max_results]
    strengths = {meta(item)["key"]: strength(item, args.search_keywords, source_by_key.get(meta(item)["key"], "").startswith("Zotero collection")) for item in items}
    all_refs = "# Zotero Search Results\n\n" + ("\n".join(format_ref(item, i, strengths[meta(item)["key"]], source_by_key.get(meta(item)["key"], "Unknown")) for i, item in enumerate(items, 1)) or "No items returned by the selected Zotero extraction mode.\n")
    evidence = "# Citation Evidence Cards\n\n" + ("\n".join(format_ref(item, i, strengths[meta(item)["key"]], source_by_key.get(meta(item)["key"], "Unknown")) for i, item in enumerate(items, 1) if strengths[meta(item)["key"]] in {"High", "Moderate"}) or "No citation evidence cards generated.\n")
    selected = "# Selected References\n\n" + ("\n".join(f"{i}. {meta(item)['title'] or 'Title not available'}\n   - Zotero key: {meta(item)['key']}\n   - Evidence strength: {strengths[meta(item)['key']]}" for i, item in enumerate(items, 1) if strengths[meta(item)["key"]] in {"High", "Moderate"}) or "No High or Moderate references selected.\n")
    pdf_review = "# PDF Fulltext Review\n\nFulltext review is not implemented in this generic template script. Use citation evidence cards and Zotero/PDF confirmation before making claims beyond metadata or abstract.\n"
    notes = "# Notes For Revision\n\n- Collection/folder inputs directly extract citable items from matched Zotero collections.\n- `search_keywords` is optional in collection mode and is mainly for keyword fallback/evidence scoring.\n- Confirm journal requirements, consent/ethics/COI, and full text before final manuscript claims.\n"

    for base in [references_dir, generated_dir]:
        write_file(base / "zotero_search_results.md", all_refs)
        write_file(base / "citation_evidence_cards.md", evidence)
        write_file(base / "pdf_fulltext_review.md", pdf_review)
    write_file(generated_dir / "zotero_api_diagnostics.md", diagnostics(statuses, collection_keys, collection_names, resolution_notes, args.reference_source, debug, None))
    write_file(generated_dir / "02_zotero_search_results.md", all_refs)
    write_file(generated_dir / "03_selected_references.md", selected)
    write_file(generated_dir / "08_notes_for_revision.md", notes)
    print(f"Zotero reference extraction complete. Items returned: {len(items)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

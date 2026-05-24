from __future__ import annotations

from typing import Dict, List, Tuple
from .parsers import split_multi


IDENTIFIER_FIELDS = ["ko", "ec", "pfam", "interpro", "go", "mapman_bin"]
TEXT_FIELDS = ["gene_symbol", "aliases", "annotation_text", "best_hit", "notes"]
MODULE_TEXT_FIELDS = ["gene_symbol", "aliases", "keywords"]


def norm(value: str) -> str:
    return str(value or "").strip().lower()


def token_set(row: Dict[str, str], field: str) -> set[str]:
    return {norm(x) for x in split_multi(row.get(field, "")) if norm(x)}


def text_blob(row: Dict[str, str], fields: List[str]) -> str:
    return " ; ".join(str(row.get(f, "")) for f in fields if row.get(f, "")).lower()


def match_module_entry(module_row: Dict[str, str], annotation_row: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """Return matched fields and values for one module row vs one annotation row."""
    matched_fields: List[str] = []
    matched_values: List[str] = []

    # Identifier exact matching: KO, EC, Pfam, InterPro, GO, etc.
    for field in IDENTIFIER_FIELDS:
        module_tokens = token_set(module_row, field)
        annotation_tokens = token_set(annotation_row, field)
        overlap = sorted(module_tokens & annotation_tokens)
        if overlap:
            matched_fields.append(field)
            matched_values.extend(overlap)

    # Gene symbol / alias exact-ish matching.
    module_symbols = set()
    for field in ["gene_symbol", "aliases"]:
        module_symbols.update(token_set(module_row, field))
        if module_row.get(field, "").strip():
            module_symbols.add(norm(module_row.get(field, "")))

    annotation_symbols = set()
    for field in ["gene_symbol", "aliases"]:
        annotation_symbols.update(token_set(annotation_row, field))
        if annotation_row.get(field, "").strip():
            annotation_symbols.add(norm(annotation_row.get(field, "")))

    symbol_overlap = sorted(x for x in (module_symbols & annotation_symbols) if x)
    if symbol_overlap:
        matched_fields.append("symbol_or_alias")
        matched_values.extend(symbol_overlap)

    # Keyword substring matching against text blob.
    blob = text_blob(annotation_row, TEXT_FIELDS)
    keywords = []
    for field in MODULE_TEXT_FIELDS:
        keywords.extend(split_multi(module_row.get(field, "")))

    keyword_hits = []
    for kw in keywords:
        nkw = norm(kw)
        if len(nkw) >= 3 and nkw in blob:
            keyword_hits.append(nkw)

    if keyword_hits:
        matched_fields.append("keyword")
        matched_values.extend(sorted(set(keyword_hits)))

    return sorted(set(matched_fields)), sorted(set(matched_values))


def match_modules(module_rows: List[Dict[str, str]], annotation_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Match all module entries against annotation rows."""
    candidates: List[Dict[str, str]] = []

    for module_row in module_rows:
        module = module_row.get("module", "")
        expected_gene = module_row.get("gene_symbol", "")
        required = module_row.get("required", "")

        for ann in annotation_rows:
            matched_fields, matched_values = match_module_entry(module_row, ann)
            if not matched_fields:
                continue

            evidence_count = len(matched_values)
            status = "ambiguous" if evidence_count <= 1 and matched_fields == ["keyword"] else "candidate"

            candidates.append({
                "module": module,
                "expected_gene": expected_gene,
                "required": required,
                "gene_id": ann.get("gene_id", ""),
                "species": ann.get("species", ""),
                "annotation_gene_symbol": ann.get("gene_symbol", ""),
                "annotation_text": ann.get("annotation_text", ""),
                "matched_fields": ";".join(matched_fields),
                "matched_values": ";".join(matched_values),
                "evidence_count": str(evidence_count),
                "status": status,
            })

    return candidates

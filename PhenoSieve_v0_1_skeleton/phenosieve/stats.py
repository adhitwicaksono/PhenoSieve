from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple


def summarize_module(module_rows: List[Dict[str, str]], candidates: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]], List[Dict[str, str]], List[Dict[str, str]]]:
    """Create presence/absence, copy-number, missing, and warning tables."""
    by_expected = defaultdict(list)
    for cand in candidates:
        key = (cand.get("module", ""), cand.get("expected_gene", ""))
        by_expected[key].append(cand)

    presence_rows: List[Dict[str, str]] = []
    copy_rows: List[Dict[str, str]] = []
    missing_rows: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    for mod in module_rows:
        module = mod.get("module", "")
        expected = mod.get("gene_symbol", "")
        required = mod.get("required", "")
        key = (module, expected)
        hits = by_expected.get(key, [])
        n = len({h.get("gene_id", "") for h in hits if h.get("gene_id", "")})

        if n == 0:
            status = "missing"
            missing_rows.append({
                "module": module,
                "expected_gene": expected,
                "required": required,
                "message": "No candidate gene detected",
            })
            if str(required).lower() in {"yes", "true", "1", "required"}:
                warnings.append({
                    "module": module,
                    "expected_gene": expected,
                    "warning_type": "missing_required",
                    "message": "Required expected gene was not detected",
                })
        elif n == 1:
            status = "present"
        else:
            status = "duplicated"
            warnings.append({
                "module": module,
                "expected_gene": expected,
                "warning_type": "duplicated",
                "message": f"{n} candidate genes detected",
            })

        presence_rows.append({
            "module": module,
            "expected_gene": expected,
            "required": required,
            "status": status,
            "candidate_count": str(n),
            "candidate_gene_ids": ";".join(sorted({h.get("gene_id", "") for h in hits if h.get("gene_id", "")})),
        })

        copy_rows.append({
            "module": module,
            "expected_gene": expected,
            "copy_number": str(n),
        })

    ambiguous_rows = []
    for cand in candidates:
        if cand.get("status") == "ambiguous":
            ambiguous_rows.append({
                "module": cand.get("module", ""),
                "expected_gene": cand.get("expected_gene", ""),
                "gene_id": cand.get("gene_id", ""),
                "matched_fields": cand.get("matched_fields", ""),
                "matched_values": cand.get("matched_values", ""),
                "message": "Weak keyword-only evidence; manual inspection recommended",
            })
            warnings.append({
                "module": cand.get("module", ""),
                "expected_gene": cand.get("expected_gene", ""),
                "warning_type": "ambiguous",
                "message": f"Weak evidence candidate: {cand.get('gene_id', '')}",
            })

    return presence_rows, copy_rows, missing_rows, warnings, ambiguous_rows


def module_summary_numbers(presence_rows: List[Dict[str, str]]) -> Dict[str, int | float]:
    expected = len(presence_rows)
    present = sum(1 for r in presence_rows if r.get("status") == "present")
    duplicated = sum(1 for r in presence_rows if r.get("status") == "duplicated")
    missing = sum(1 for r in presence_rows if r.get("status") == "missing")
    detected = present + duplicated
    completeness = round((detected / expected * 100), 2) if expected else 0.0

    return {
        "expected": expected,
        "present": present,
        "duplicated": duplicated,
        "missing": missing,
        "detected": detected,
        "completeness": completeness,
    }

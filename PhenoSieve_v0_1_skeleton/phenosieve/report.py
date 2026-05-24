from __future__ import annotations

from pathlib import Path
from typing import Dict, List
from .stats import module_summary_numbers


def write_markdown_report(
    path: str | Path,
    module_rows: List[Dict[str, str]],
    candidate_rows: List[Dict[str, str]],
    presence_rows: List[Dict[str, str]],
    warning_rows: List[Dict[str, str]],
) -> None:
    """Write a simple Markdown audit report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    numbers = module_summary_numbers(presence_rows)

    modules = sorted(set(r.get("module", "") for r in module_rows))

    lines = []
    lines.append("# PhenoSieve Module Audit Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Modules: {', '.join(modules) if modules else 'NA'}")
    lines.append(f"- Expected genes: {numbers['expected']}")
    lines.append(f"- Detected genes/modules: {numbers['detected']}")
    lines.append(f"- Present single-copy expected genes: {numbers['present']}")
    lines.append(f"- Duplicated expected genes: {numbers['duplicated']}")
    lines.append(f"- Missing expected genes: {numbers['missing']}")
    lines.append(f"- Module completeness: {numbers['completeness']}%")
    lines.append("")
    lines.append("## Presence / absence")
    lines.append("")
    lines.append("| Module | Expected gene | Status | Candidate count | Candidate gene IDs |")
    lines.append("|---|---|---:|---:|---|")
    for row in presence_rows:
        lines.append(
            f"| {row.get('module','')} | {row.get('expected_gene','')} | "
            f"{row.get('status','')} | {row.get('candidate_count','')} | "
            f"{row.get('candidate_gene_ids','')} |"
        )

    lines.append("")
    lines.append("## Candidate count")
    lines.append("")
    lines.append(f"- Candidate rows: {len(candidate_rows)}")
    lines.append("")

    if warning_rows:
        lines.append("## Warnings")
        lines.append("")
        lines.append("| Module | Expected gene | Type | Message |")
        lines.append("|---|---|---|---|")
        for row in warning_rows:
            lines.append(
                f"| {row.get('module','')} | {row.get('expected_gene','')} | "
                f"{row.get('warning_type','')} | {row.get('message','')} |"
            )
    else:
        lines.append("## Warnings")
        lines.append("")
        lines.append("No warnings generated.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

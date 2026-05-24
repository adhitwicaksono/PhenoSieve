from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Dict

from .parsers import read_tsv, write_tsv, require_columns
from .matcher import match_modules
from .fasta import read_fasta, write_fasta, subset_records
from .stats import summarize_module
from .report import write_markdown_report


CANDIDATE_FIELDS = [
    "module",
    "expected_gene",
    "required",
    "gene_id",
    "species",
    "annotation_gene_symbol",
    "annotation_text",
    "matched_fields",
    "matched_values",
    "evidence_count",
    "status",
]


def run(args: argparse.Namespace) -> None:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    module_rows = read_tsv(args.module)
    annotation_rows = read_tsv(args.annotation)

    require_columns(module_rows, ["module", "gene_symbol"], "module TSV")
    require_columns(annotation_rows, ["gene_id"], "annotation TSV")

    candidates = match_modules(module_rows, annotation_rows)

    presence_rows, copy_rows, missing_rows, warning_rows, ambiguous_rows = summarize_module(module_rows, candidates)

    write_tsv(out / "candidate_genes.tsv", candidates, CANDIDATE_FIELDS)
    write_tsv(out / "module_presence_absence.tsv", presence_rows, [
        "module", "expected_gene", "required", "status", "candidate_count", "candidate_gene_ids"
    ])
    write_tsv(out / "module_copy_number.tsv", copy_rows, [
        "module", "expected_gene", "copy_number"
    ])
    write_tsv(out / "missing_expected_genes.tsv", missing_rows, [
        "module", "expected_gene", "required", "message"
    ])
    write_tsv(out / "warnings.tsv", warning_rows, [
        "module", "expected_gene", "warning_type", "message"
    ])
    write_tsv(out / "ambiguous_matches.tsv", ambiguous_rows, [
        "module", "expected_gene", "gene_id", "matched_fields", "matched_values", "message"
    ])

    # Protein sequence extraction
    protein_records = read_fasta(args.fasta)
    candidate_ids = []
    seen = set()
    for cand in candidates:
        gid = cand.get("gene_id", "")
        if gid and gid not in seen:
            seen.add(gid)
            candidate_ids.append(gid)

    selected_proteins = subset_records(protein_records, candidate_ids)
    fasta_dir = out / "fasta"
    write_fasta(fasta_dir / "all_candidates.faa", selected_proteins)

    # Per expected gene FASTA
    for row in presence_rows:
        expected = row.get("expected_gene", "unknown") or "unknown"
        ids = [x for x in row.get("candidate_gene_ids", "").split(";") if x]
        recs = subset_records(protein_records, ids)
        if recs:
            write_fasta(fasta_dir / f"{expected}.faa", recs)

    # Missing FASTA warnings
    protein_missing = [gid for gid in candidate_ids if gid not in protein_records]
    if protein_missing:
        extra_warnings = [
            {
                "module": "",
                "expected_gene": "",
                "warning_type": "missing_protein_sequence",
                "message": gid,
            }
            for gid in protein_missing
        ]
        warning_rows.extend(extra_warnings)
        write_tsv(out / "warnings.tsv", warning_rows, [
            "module", "expected_gene", "warning_type", "message"
        ])

    # Optional CDS sequence extraction
    if args.cds:
        cds_records = read_fasta(args.cds)
        selected_cds = subset_records(cds_records, candidate_ids)
        cds_dir = out / "cds"
        write_fasta(cds_dir / "all_candidates.fna", selected_cds)

        for row in presence_rows:
            expected = row.get("expected_gene", "unknown") or "unknown"
            ids = [x for x in row.get("candidate_gene_ids", "").split(";") if x]
            recs = subset_records(cds_records, ids)
            if recs:
                write_fasta(cds_dir / f"{expected}.fna", recs)

        cds_missing = [gid for gid in candidate_ids if gid not in cds_records]
        if cds_missing:
            extra_warnings = [
                {
                    "module": "",
                    "expected_gene": "",
                    "warning_type": "missing_cds_sequence",
                    "message": gid,
                }
                for gid in cds_missing
            ]
            warning_rows.extend(extra_warnings)
            write_tsv(out / "warnings.tsv", warning_rows, [
                "module", "expected_gene", "warning_type", "message"
            ])

    write_markdown_report(
        out / "module_audit_report.md",
        module_rows,
        candidates,
        presence_rows,
        warning_rows,
    )

    print(f"PhenoSieve run complete: {out}")
    print(f"Candidates: {len(candidates)}")
    print(f"Outputs written to: {out.resolve()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phenosieve",
        description="Curated gene-set sequence extraction and audit for comparative genomics",
    )
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="Run curated module matching and FASTA extraction")
    run_parser.add_argument("--module", required=True, help="Curated module TSV")
    run_parser.add_argument("--annotation", required=True, help="Normalized annotation TSV")
    run_parser.add_argument("--fasta", required=True, help="Protein FASTA")
    run_parser.add_argument("--cds", required=False, help="Optional CDS FASTA")
    run_parser.add_argument("--out", required=True, help="Output directory")
    run_parser.set_defaults(func=run)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()

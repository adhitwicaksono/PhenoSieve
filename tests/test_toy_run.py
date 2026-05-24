from pathlib import Path
from phenosieve.cli import main


def test_toy_run(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "toy_results"

    main([
        "run",
        "--module", str(root / "examples/toy_anthocyanin/modules/anthocyanin_demo.tsv"),
        "--annotation", str(root / "examples/toy_anthocyanin/annotation/toy_annotation.tsv"),
        "--fasta", str(root / "examples/toy_anthocyanin/fasta/toy_proteins.faa"),
        "--cds", str(root / "examples/toy_anthocyanin/fasta/toy_cds.fna"),
        "--out", str(out),
    ])

    assert (out / "candidate_genes.tsv").exists()
    assert (out / "module_presence_absence.tsv").exists()
    assert (out / "module_audit_report.md").exists()
    assert (out / "fasta/all_candidates.faa").exists()
    assert (out / "cds/all_candidates.fna").exists()

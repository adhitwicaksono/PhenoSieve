from pathlib import Path
from phenosieve.cli import main


def test_toy_multimodule_carotenoid(tmp_path):
    root = Path(__file__).resolve().parents[1]
    out = tmp_path / "carotenoid_results"

    main([
        "run",
        "--module", str(root / "examples/toy_multimodule/modules/carotenoid_core.tsv"),
        "--annotation", str(root / "examples/toy_multimodule/annotation/toy_multimodule_annotation.tsv"),
        "--fasta", str(root / "examples/toy_multimodule/fasta/toy_multimodule_proteins.faa"),
        "--cds", str(root / "examples/toy_multimodule/fasta/toy_multimodule_cds.fna"),
        "--out", str(out),
    ])

    assert (out / "candidate_genes.tsv").exists()
    assert (out / "module_presence_absence.tsv").exists()
    assert (out / "module_audit_report.md").exists()
    assert (out / "fasta/all_candidates.faa").exists()
    assert (out / "cds/all_candidates.fna").exists()

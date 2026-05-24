# Toy anthocyanin example

This tiny example is designed to test the PhenoSieve v0.1 logic without requiring large external datasets.

Run:

```bash
phenosieve run \
  --module examples/toy_anthocyanin/modules/anthocyanin_demo.tsv \
  --annotation examples/toy_anthocyanin/annotation/toy_annotation.tsv \
  --fasta examples/toy_anthocyanin/fasta/toy_proteins.faa \
  --cds examples/toy_anthocyanin/fasta/toy_cds.fna \
  --out results/toy_anthocyanin
```

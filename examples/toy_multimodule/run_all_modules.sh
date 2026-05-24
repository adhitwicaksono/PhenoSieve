#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="examples/toy_multimodule/modules"
ANNOTATION="examples/toy_multimodule/annotation/toy_multimodule_annotation.tsv"
PROTEINS="examples/toy_multimodule/fasta/toy_multimodule_proteins.faa"
CDS="examples/toy_multimodule/fasta/toy_multimodule_cds.fna"
OUTDIR="results/toy_multimodule"

for module_file in "$MODULE_DIR"/*.tsv; do
    module_name=$(basename "$module_file" .tsv)
    echo "Running PhenoSieve module: $module_name"
    phenosieve run \
      --module "$module_file" \
      --annotation "$ANNOTATION" \
      --fasta "$PROTEINS" \
      --cds "$CDS" \
      --out "$OUTDIR/$module_name"
done

echo "All toy multimodule runs completed."

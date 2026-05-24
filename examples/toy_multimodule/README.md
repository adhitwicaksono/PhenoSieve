# Toy multimodule examples

This folder adds five additional curated module examples for PhenoSieve v0.1 testing:

1. `carotenoid_core`
2. `lignin_core`
3. `cellulose_wall_core`
4. `aba_signaling_core`
5. `nitrogen_assimilation_core`

These are **manual toy/prototype annotations**. They are designed to test PhenoSieve logic, not to replace KEGG, InterProScan, KofamKOALA, Mercator4, or expert biological curation.

## Run one module

Example:

```bash
phenosieve run \
  --module examples/toy_multimodule/modules/carotenoid_core.tsv \
  --annotation examples/toy_multimodule/annotation/toy_multimodule_annotation.tsv \
  --fasta examples/toy_multimodule/fasta/toy_multimodule_proteins.faa \
  --cds examples/toy_multimodule/fasta/toy_multimodule_cds.fna \
  --out results/toy_multimodule/carotenoid_core
```

## Run all five modules

From the repository root:

```bash
bash examples/toy_multimodule/run_all_modules.sh
```

## Why these examples exist

The original anthocyanin demo tests a flavonoid/pigment module.

These five modules broaden testing across:

- pigment biosynthesis;
- phenylpropanoid/lignin metabolism;
- cell wall biosynthesis/remodeling;
- hormone biosynthesis/signaling;
- nutrient assimilation.

That helps reveal whether PhenoSieve behaves consistently across different biological module styles.

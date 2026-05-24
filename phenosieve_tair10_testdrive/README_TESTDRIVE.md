# PhenoSieve TAIR10 Test Drive Package

This package contains a compact Arabidopsis anthocyanin/flavonoid demo dataset for developing PhenoSieve v0.1.

## What is included

```text
modules/
  anthocyanin_demo_module.tsv

annotation/
  ath_manual_anthocyanin_annotation.tsv

id_maps/
  ath_anthocyanin_id_map.tsv

expected/
  expected_anthocyanin_genes.tsv

extracted/
  anthocyanin_demo_proteins.faa
  anthocyanin_demo_cds.fna
  protein_by_gene/
  cds_by_gene/

stats/
  module_presence_absence.tsv
  module_copy_number.tsv
  module_audit_report.md
```

## What is not included

The full TAIR10 protein/CDS FASTA files are not copied here to keep the demo package small.
Use the uploaded original files as the main input FASTA files.

## Purpose

This is a development test package, not a final biological annotation resource.
It is meant to test whether PhenoSieve can:

1. read a module definition;
2. read a normalized annotation table;
3. match gene IDs;
4. extract protein/CDS sequences;
5. generate BUSCO-like module statistics.

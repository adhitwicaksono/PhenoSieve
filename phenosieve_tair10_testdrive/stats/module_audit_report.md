# PhenoSieve TAIR10 Test Drive: Anthocyanin Demo

This is a small curated demo package generated from the uploaded TAIR10 representative gene model protein and CDS FASTA files.

## Input files inspected

- TAIR10 protein representative gene model FASTA: `TAIR10_pep_20110103_representative_gene_model.fasta`
- TAIR10 CDS representative gene model FASTA: `TAIR10_cds_20110103_representative_gene_model.fasta`

## FASTA summary

| File | Entries |
|---|---:|
| Protein representative gene model FASTA | 27416 |
| CDS representative gene model FASTA | 27416 |

## Demo module summary

| Module | Expected entries | Present in uploaded protein FASTA | Completeness |
|---|---:|---:|---:|
| anthocyanin_demo | 17 | 17 | 100.0% |

## Notes

- This demo uses manually curated Arabidopsis anthocyanin/flavonoid-related genes.
- This is not yet a KEGG/Kofam/InterPro-derived annotation table.
- The table `annotation/ath_manual_anthocyanin_annotation.tsv` is a PhenoSieve-friendly normalized demo annotation table.
- The file `modules/anthocyanin_demo_module.tsv` is a draft module definition file.
- Protein and CDS sequences have been extracted for the listed demo genes.
- Future PhenoSieve tests should replace or supplement this manual demo with KofamScan, eggNOG-mapper, InterProScan, or Mercator4 annotation output.

## Suggested first CLI target

```bash
phenosieve run \
  --module modules/anthocyanin_demo_module.tsv \
  --annotation annotation/ath_manual_anthocyanin_annotation.tsv \
  --fasta TAIR10_pep_20110103_representative_gene_model.fasta \
  --id-map id_maps/ath_anthocyanin_id_map.tsv \
  --out anthocyanin_sieve/
```

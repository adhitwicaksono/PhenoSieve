# PhenoSieve Araport11 + InterPro Test Drive

This package is a small PhenoSieve v0.1-style test dataset built from uploaded Araport11 representative gene-model sequences and InterPro reference mapping files.

## Uploaded sequence input inspected

- Araport11 peptide representative gene model FASTA: 27,650 entries
- Araport11 CDS representative gene model FASTA: 27,562 entries
- Peptide loci: 27,650
- CDS loci: 27,562
- Shared loci between peptide and CDS files: 27,561
- Peptide-only loci: 89
- CDS-only loci: 1

Important note: the peptide and CDS files are from different Araport dates, so they are highly overlapping but not perfectly identical. For PhenoSieve v0.1 protein extraction, use the peptide FASTA as the primary sequence source.

## Uploaded InterPro reference input inspected

- InterPro entry list entries: 51,489
- InterPro2GO mapping lines: 30,200
- Unique InterPro IDs with GO mappings: 14,799

These InterPro files are reference dictionaries. They do not tell us which Araport11 proteins contain which InterPro domains. For that, we still need InterProScan output run on the Araport11 peptide FASTA.

## Demo module

The demo module is `modules/anthocyanin_interpro_enriched_module.tsv`.

It includes:
- core anthocyanin/flavonoid biosynthesis genes
- transport/storage genes
- regulatory genes
- broad InterPro evidence terms where available

## Important limitation

This package does not replace a real InterProScan run. It only enriches the curated module definition with relevant InterPro IDs from the uploaded InterPro dictionaries.

For full PhenoSieve evidence scoring, the next needed file is:

```text
Araport11_pep_20250411_representative_gene_model.interproscan.tsv
```

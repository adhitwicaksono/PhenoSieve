# PhenoSieve input formats

## Module TSV

Minimum columns:

```text
module
gene_symbol
```

Recommended columns:

```text
aliases
keywords
ko
ec
pfam
interpro
go
required
```

## Annotation TSV

Minimum column:

```text
gene_id
```

Recommended columns:

```text
species
source
gene_symbol
aliases
annotation_text
ko
ec
pfam
interpro
go
mapman_bin
best_hit
evalue
bitscore
notes
```

## FASTA

The first whitespace-delimited token in each FASTA header is treated as the sequence ID.

Example:

```fasta
>AT5G13930 description
MASS...
```

The sequence ID is `AT5G13930`.

# PhenoSieve

**PhenoSieve** is a small Python toolkit for **curated gene-set sequence extraction and audit** in comparative genomics.

It is designed to sit downstream of functional annotation tools and, later, orthology tools.

```text
Curated gene/pathway module
        ↓
Functional annotation table
        ↓
Gene ID matching
        ↓
FASTA sequence extraction
        ↓
Presence / missing / duplicated / ambiguous statistics
        ↓
Markdown audit report
```

## What PhenoSieve is

PhenoSieve is a **curated gene-set sequence caller**.

It asks:

> Given a curated biological module, which genes in my annotation table match it, and can I extract their sequences?

Example modules:

- anthocyanin / flavonoid core genes;
- lignin biosynthesis genes;
- carotenoid biosynthesis genes;
- cell-wall-remodeling genes;
- aroma-associated genes;
- stress-response gene modules.

## What PhenoSieve is not

PhenoSieve is not a phenotype oracle.

It does not infer phenotype from raw genome sequence.  
It does not replace KEGG, GO, InterProScan, eggNOG-mapper, KofamKOALA, Mercator4/MapMan, OrthoFinder, or BUSCO.

Instead, it uses curated gene/module definitions and existing annotation results to extract usable sequences and generate audit-style summaries.

## Current prototype scope: v0.1

The v0.1 skeleton supports:

- reading a curated module TSV;
- reading a normalized annotation TSV;
- matching module definitions against annotations;
- extracting protein FASTA sequences;
- optionally extracting CDS FASTA sequences;
- writing per-gene FASTA files;
- writing an all-candidates FASTA;
- writing candidate tables;
- writing module presence/absence and copy-number tables;
- writing a Markdown audit report.

Not yet implemented:

- OrthoFinder integration;
- InterProScan parser;
- KEGG/Kofam parser;
- GFF/genome extraction;
- alignment/supermatrix helper;
- TraitLexicon / human trait phrase translation.

## Installation for development

From the repository root:

```bash
pip install -e .
```

## Quick test

Run the toy example:

```bash
phenosieve run \
  --module examples/toy_anthocyanin/modules/anthocyanin_demo.tsv \
  --annotation examples/toy_anthocyanin/annotation/toy_annotation.tsv \
  --fasta examples/toy_anthocyanin/fasta/toy_proteins.faa \
  --cds examples/toy_anthocyanin/fasta/toy_cds.fna \
  --out results/toy_anthocyanin
```

Expected output:

```text
results/toy_anthocyanin/
├── candidate_genes.tsv
├── module_presence_absence.tsv
├── module_copy_number.tsv
├── missing_expected_genes.tsv
├── ambiguous_matches.tsv
├── warnings.tsv
├── module_audit_report.md
├── fasta/
│   ├── all_candidates.faa
│   ├── CHS.faa
│   ├── CHI.faa
│   ├── DFR.faa
│   └── ANS.faa
└── cds/
    ├── all_candidates.fna
    ├── CHS.fna
    ├── CHI.fna
    ├── DFR.fna
    └── ANS.fna
```

## Required input files

### 1. Curated module TSV

Required columns:

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

Example:

```tsv
module	gene_symbol	aliases	keywords	ko	ec	pfam	interpro	go	required
anthocyanin	CHS	TT4; chalcone synthase	chalcone synthase; naringenin-chalcone synthase	K00660	2.3.1.74	PF00195	IPR018088	GO:0009813	yes
```

### 2. Normalized annotation TSV

Required columns:

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

Example:

```tsv
gene_id	species	source	gene_symbol	aliases	annotation_text	ko	ec	pfam	interpro	go	notes
AT5G13930	Arabidopsis_thaliana	manual	CHS	TT4; chalcone synthase	chalcone synthase	K00660	2.3.1.74	PF00195	IPR018088	GO:0009813	known anthocyanin/flavonoid gene
```

### 3. Protein FASTA

The FASTA header ID must match `gene_id` in the annotation table, unless an ID-mapping layer is added later.

Accepted simple header:

```fasta
>AT5G13930
MASS...
```

Also accepted:

```fasta
>AT5G13930 some description here
MASS...
```

PhenoSieve currently uses the first whitespace-delimited token as the FASTA ID.

## Matching logic

PhenoSieve v0.1 uses simple evidence rules:

- exact case-insensitive match for identifiers such as KO, EC, Pfam, InterPro, and GO;
- exact/synonym match for gene symbols and aliases;
- case-insensitive substring match for keywords against annotation text, gene symbol, aliases, and notes.

Each candidate receives:

- `matched_fields`;
- `matched_values`;
- `evidence_count`;
- `status`.

Possible status values:

| Status | Meaning |
|---|---|
| `present` | One candidate found for an expected gene |
| `duplicated` | More than one candidate found for an expected gene |
| `missing` | No candidate found |
| `ambiguous` | Candidate found but evidence is weak |

## Relationship to existing tools

PhenoSieve is not intended to replace existing tools.

| Tool/resource | Main purpose | Relationship to PhenoSieve |
|---|---|---|
| BUSCO | Genome/transcriptome/proteome completeness using conserved single-copy orthologs | Inspiration for audit vocabulary |
| OrthoFinder | Orthogroup and orthology inference | Planned optional upstream input |
| KEGG / KofamKOALA / KAAS | KO assignment and pathway reconstruction | Annotation/module source |
| eggNOG-mapper | Functional annotation through orthology | Annotation source |
| InterProScan | Protein family/domain annotation | Annotation source |
| Mercator4 / MapMan | Plant functional bin assignment | Plant-focused annotation source |
| PlantCyc / PMN | Plant metabolic pathway knowledge | Curated module source |

The niche of PhenoSieve is:

> **curated gene-set sequence calling and audit for comparative genomics.**

## Planned roadmap

### v0.1
Curated module + normalized annotation + FASTA extraction.

### v0.2
Converters for common annotation formats:

- eggNOG-mapper;
- InterProScan TSV;
- KofamScan/KofamKOALA;
- Mercator4/MapMan;
- BLAST/DIAMOND tabular output.

### v0.3
OrthoFinder-aware extraction:

- orthogroup-aware expansion;
- species-by-species copy-number matrix;
- duplication warnings.

### v0.4
Supermatrix helper:

- one FASTA per expected gene;
- alignment-ready exports;
- occupancy matrix;
- concatenation;
- partition file.

### v1.0
Reproducible curated gene-module comparative genomics toolkit.

## Database and licensing note

Some resources such as KEGG, PlantCyc/PMN, InterPro, Pfam, eggNOG, and MapMan/Mercator have their own licensing and access rules.

PhenoSieve should not redistribute restricted database content unless permitted.  
Users should provide their own annotation outputs or locally prepared module definition files.

## Author

Developed by **Adhityo Wicaksono** as part of an ongoing ecosystem of practical bioinformatics tools for plant and comparative genomics.

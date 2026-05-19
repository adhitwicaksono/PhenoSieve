# PhenoSieve

**Curated gene-set sequence calling for comparative genomics.**

> PhenoSieve is a planned Python toolkit for extracting, auditing, and preparing curated pathway/gene-module sequences from annotated genomes, proteomes, transcriptomes, and orthogroup results.

PhenoSieve is designed for researchers who already have functional annotation outputs and sequence files, but still need a reproducible way to ask focused biological questions such as:

- Which genes from this curated pathway are present in each species?
- Which expected genes are missing, duplicated, ambiguous, or expanded?
- Can I extract standardized FASTA files for a curated gene set?
- Can I build a pathway/module-specific supermatrix for phylogenetic analysis?
- Can I compare a biologically meaningful gene module rather than the entire orthogroup universe?

PhenoSieve is **not** a phenotype oracle. It does not claim that a gene set directly explains a phenotype. Instead, it helps users extract and audit curated biological gene modules for comparative genomics.

---

## Project Status

**Current stage:** concept / early development design.

Planned first stable target:

```text
v0.1 = curated gene/module sequence extraction + basic audit table
```

PhenoSieve is being designed as part of a broader lightweight bioinformatics toolkit ecosystem for plant and non-model organism comparative genomics.

---

## Core Idea

Many tools already annotate genes, infer orthogroups, reconstruct pathways, or evaluate genome completeness.

However, researchers often still need ad hoc scripts to do this:

```text
"I have a curated list of genes for a pathway/module.
Can I pull those genes from my annotated proteomes,
check which species have them,
count duplications,
flag missing genes,
and export FASTA files for downstream alignment?"
```

PhenoSieve aims to make this step reproducible.

```text
Curated gene/module definition
        ↓
Functional annotation table
        ↓
Gene ID matching
        ↓
Optional orthogroup mapping
        ↓
Sequence extraction from FASTA
        ↓
Presence / absence / copy-number audit
        ↓
Per-gene FASTA output
        ↓
Future: alignment and supermatrix helper
```

---

## What PhenoSieve Does

PhenoSieve will take a curated gene/pathway/module definition and use functional annotation tables, FASTA files, and optional orthogroup files to:

- identify candidate genes matching the curated module;
- extract matched protein or nucleotide sequences;
- summarize presence, absence, duplication, ambiguity, and possible fragmentation;
- generate BUSCO-like module statistics;
- prepare standardized per-gene FASTA files;
- support future pathway/module-based supermatrix construction for phylogenetic analysis.

---

## What PhenoSieve Does Not Do

PhenoSieve does **not** perform de novo functional annotation by itself in early versions.

It does not replace:

- KEGG, KofamKOALA/KofamScan, KAAS, BlastKOALA, or GhostKOALA for KEGG Orthology assignment;
- eggNOG-mapper, InterProScan, Mantis, BLAST, or DIAMOND for functional annotation;
- OrthoFinder for orthogroup and orthology inference;
- BUSCO for genome/transcriptome/proteome completeness assessment;
- PlantCyc/PMN, MetaCyc, Mercator4, or MapMan4 for pathway knowledge and functional classification;
- enrichment tools such as clusterProfiler or keggtools.

Instead, PhenoSieve occupies a downstream **curated sequence extraction and audit layer**.

---

## Relationship to Existing Tools

PhenoSieve is not intended to replace existing annotation, orthology, pathway, or enrichment tools.

In simple terms:

```text
Functional annotation tools tell us what genes might do.
Orthology tools tell us how genes are related.
BUSCO tells us whether conserved universal markers are present.
PhenoSieve asks whether a curated biological gene set is present, duplicated, missing, ambiguous, and extractable as sequence data.
```

### Similar or related tools/resources

| Tool/resource | Main purpose | Relationship to PhenoSieve |
|---|---|---|
| **BUSCO** | Evaluates genome, transcriptome, or proteome completeness using conserved single-copy orthologs | Conceptual inspiration for present/duplicated/fragmented/missing statistics |
| **OrthoFinder** | Infers orthogroups, orthologs, gene trees, duplications, and comparative genomics statistics | Optional upstream orthology input |
| **BuscoPhylo** | BUSCO-based phylogenomic analysis and supermatrix/tree generation | Similar future phylogenomics direction, but BUSCO-marker-based rather than custom curated module-based |
| **KEGG / KAAS / KofamKOALA / BlastKOALA / GhostKOALA** | Assigns KEGG Orthology identifiers and reconstructs pathways/modules | Provides annotation IDs and pathway definitions usable by PhenoSieve |
| **eggNOG-mapper** | Functional annotation through orthology assignment | Provides annotation tables usable by PhenoSieve |
| **InterProScan** | Protein family/domain annotation | Provides domain and GO evidence usable by PhenoSieve |
| **Mantis** | Flexible consensus-driven genome/protein annotation | Provides annotation tables usable by PhenoSieve |
| **Mercator4 / MapMan4** | Plant protein functional annotation and MapMan bin assignment | Useful plant-focused annotation input |
| **PlantCyc / PMN** | Curated and predicted plant metabolic pathway knowledge | Useful source for curated plant pathway modules |
| **clusterProfiler** | GO/KEGG enrichment and gene-list interpretation | Related to pathway interpretation, but not sequence extraction |
| **keggtools** | KEGG pathway enrichment and pathway rendering library | Related to KEGG analysis, but not curated FASTA sequence calling |
| **KEGG_Extractor** | Extracts and classifies amino acid/nucleotide sequences and species information from KEGG annotation results | Close neighbor, especially for KEGG-based sequence extraction, but not focused on plant comparative gene modules, OrthoFinder-aware extraction, BUSCO-like module stats, or supermatrix preparation |
| **GPATHEX** | Biological pathway and taxonomic information extraction from KEGG | Related KEGG extraction utility, but not identical to PhenoSieve's planned comparative genomics workflow |
| **DRAM / METABOLIC / GapMind** | Microbial metabolism annotation, pathway profiling, or pathway-gap detection | Conceptually related, especially in microbial metabolism, but outside PhenoSieve's intended plant/comparative gene-set extraction niche |

### Proposed niche

To our knowledge, PhenoSieve differs from existing tools by combining:

1. user-defined or database-derived curated gene/pathway modules;
2. annotation-table parsing;
3. optional orthogroup-aware expansion;
4. FASTA sequence extraction;
5. BUSCO-like module completeness statistics;
6. ambiguity and duplication reporting;
7. future standardized pathway/module supermatrix construction.

The goal is not pathway enrichment or pathway visualization.

The goal is:

> **Curated gene-set sequence calling for comparative genomics.**

---

## Example Use Case

Suppose the user wants to study the anthocyanin pathway across several plant genomes.

Instead of manually searching annotation tables and copying gene IDs one by one, the user provides a curated module file:

```tsv
module	gene_symbol	aliases	keywords	ko	pfam	ec	go
anthocyanin	CHS	chalcone synthase; naringenin-chalcone synthase	chalcone synthase	K00660	PF00195	2.3.1.74	GO:0009813
anthocyanin	CHI	chalcone isomerase	chalcone isomerase	K01859	PF02431	5.5.1.6	
anthocyanin	F3H	flavanone 3-hydroxylase	flavanone 3-hydroxylase	K00475	PF03171	1.14.11.9	
anthocyanin	DFR	dihydroflavonol reductase	dihydroflavonol reductase	K13082	PF00106	1.1.1.219	GO:0045552
anthocyanin	ANS	anthocyanidin synthase; leucoanthocyanidin dioxygenase	anthocyanidin synthase; leucoanthocyanidin dioxygenase	K05277	PF03171	1.14.20.4	
anthocyanin	UFGT	UDP-glucose flavonoid glucosyltransferase	UDP-glucose flavonoid glucosyltransferase	K12930	PF00201	2.4.1.x	
```

PhenoSieve then searches annotation tables, pulls the matching gene IDs, maps them to orthogroups if available, extracts the sequences, and reports module-level statistics.

Example output:

```text
anthocyanin_sieve/
├── candidate_genes.tsv
├── candidate_orthogroups.tsv
├── module_presence_absence.tsv
├── module_copy_number.tsv
├── missing_expected_genes.tsv
├── ambiguous_matches.tsv
├── warnings.tsv
├── module_audit_report.md
├── fasta/
│   ├── CHS.faa
│   ├── CHI.faa
│   ├── F3H.faa
│   ├── DFR.faa
│   ├── ANS.faa
│   └── UFGT.faa
└── logs/
    └── phenosieve.log
```

Future versions may add:

```text
supermatrix/
├── anthocyanin_supermatrix.faa
├── anthocyanin_partitions.txt
├── occupancy_matrix.tsv
└── alignment_summary.tsv
```

---

## Input Requirements

### Minimum inputs

PhenoSieve requires three basic inputs.

#### 1. Curated module definition file

Supported or planned formats:

- TSV
- YAML
- JSON

The module file defines expected genes, aliases, keywords, KO IDs, EC numbers, Pfam IDs, InterPro IDs, GO terms, MapMan bins, or other identifiers.

#### 2. FASTA file

Protein FASTA is recommended for early versions.

Example:

```text
proteins.faa
```

Future versions may support:

- CDS FASTA;
- transcript FASTA;
- genome + GFF3 extraction.

#### 3. Functional annotation table

Supported or planned annotation sources include:

- eggNOG-mapper;
- InterProScan;
- KofamScan/KofamKOALA;
- KAAS;
- BLAST/DIAMOND custom tables;
- Mercator4/MapMan;
- Mantis;
- user-defined annotation TSV.

### Recommended inputs

#### 4. OrthoFinder output

Recommended files:

```text
Orthogroups.tsv
Orthogroups.GeneCount.tsv
```

Optional files:

```text
Orthologues/
Gene_Trees/
Comparative_Genomics_Statistics/
```

#### 5. Gene coordinate file

Optional but useful for future genomic-region extraction:

```text
annotation.gff3
annotation.gtf
genes.bed
```

#### 6. ID mapping file

Recommended when FASTA IDs, gene IDs, transcript IDs, protein IDs, and locus IDs differ.

```tsv
gene_id	fasta_id	transcript_id	protein_id	locus_id
Os01g0633500	Os01g0633500.1	Os01t0633500.1	Os01p0633500	LOC_Os01g44280
```

This is especially important for plant genomes, where identifier systems often differ between annotation files, FASTA headers, and external databases.

---

## Standardized Annotation Table

PhenoSieve should accept raw outputs from common annotation tools, but for reproducibility users are encouraged to convert their results into a normalized table:

```text
phenosieve_annotation.tsv
```

### Why normalize?

Different tools use different output formats.

| Tool | Useful fields |
|---|---|
| eggNOG-mapper | gene ID, orthologous group, function, GO, EC, KEGG KO/pathway/module, COG category |
| InterProScan | gene/protein ID, InterPro ID, Pfam/domain IDs, GO, pathway terms |
| KofamScan/KofamKOALA | gene/protein ID, KO ID, score, threshold |
| Mercator4/MapMan | gene/protein ID, MapMan bin, functional category |
| BLAST/DIAMOND | query ID, subject ID, description, e-value, bitscore |
| Mantis | consensus annotation across multiple reference sources |
| Custom table | user-defined annotations |

PhenoSieve should eventually provide converters:

```bash
phenosieve convert-eggnog \
  --input eggnog.emapper.annotations \
  --out phenosieve_annotation.tsv
```

```bash
phenosieve convert-interpro \
  --input interproscan.tsv \
  --out phenosieve_annotation.tsv
```

```bash
phenosieve convert-kofam \
  --input kofam_results.tsv \
  --out phenosieve_annotation.tsv
```

```bash
phenosieve convert-mercator \
  --input mercator4_results.tsv \
  --out phenosieve_annotation.tsv
```

### Minimum annotation table

For v0.1, the absolute minimum is:

```tsv
gene_id	annotation_text
```

Example:

```tsv
gene_id	annotation_text
Gene001	chalcone synthase
Gene002	dihydroflavonol reductase
Gene003	MYB transcription factor
```

### Recommended annotation table

A more useful table should include:

```tsv
gene_id	species	source	gene_symbol	annotation_text	ko	ec	pfam	go
```

Example:

```tsv
gene_id	species	source	gene_symbol	annotation_text	ko	ec	pfam	go
Os01g0633500	Oryza_sativa	eggNOG	CHS	chalcone synthase	K00660	2.3.1.74	PF00195	GO:0009813
Os08g0424500	Oryza_sativa	Kofam	BADH2	betaine aldehyde dehydrogenase	K00130	1.2.1.8	PF00171	GO:0004029
```

### Full recommended annotation table

For more robust matching and scoring:

```tsv
gene_id	species	source	gene_symbol	aliases	annotation_text	ko	ec	pfam	interpro	go	mapman_bin	eggnog_og	best_hit	evalue	bitscore	evidence_level	notes
```

Example:

```tsv
gene_id	species	source	gene_symbol	aliases	annotation_text	ko	ec	pfam	interpro	go	mapman_bin	eggnog_og	best_hit	evalue	bitscore	evidence_level	notes
Os01g0633500	Oryza_sativa	eggNOG	CHS	chalcone synthase; naringenin-chalcone synthase	chalcone synthase	K00660	2.3.1.74	PF00195	IPR011141	GO:0009813	16.8 secondary metabolism	ENOG502QABC	CHS1_ARATH	1e-80	260	high	manual review recommended
Os08g0424500	Oryza_sativa	Kofam	BADH2	betaine aldehyde dehydrogenase; fgr	betaine aldehyde dehydrogenase	K00130	1.2.1.8	PF00171	IPR016162	GO:0004029			BADH2_ORYSJ	2e-120	410	high	fragrance-related anchor gene
```

### Wide versus long annotation format

PhenoSieve should prioritize a user-friendly **wide format** as input:

```tsv
gene_id	species	gene_symbol	annotation_text	ko	ec	pfam	go
Gene001	Rice	CHS	chalcone synthase	K00660	2.3.1.74	PF00195	GO:0009813
Gene002	Rice	DFR	dihydroflavonol reductase	K13082	1.1.1.219	PF00106	GO:0045552
```

Internally, it may convert this into a **long format** for cleaner matching and scoring:

```tsv
gene_id	species	evidence_type	evidence_value	source	score
Gene001	Rice	ko	K00660	KofamScan	300
Gene001	Rice	pfam	PF00195	InterProScan	
Gene001	Rice	keyword	chalcone synthase	eggNOG	
Gene002	Rice	ko	K13082	KofamScan	250
```

Recommended philosophy:

> **Users provide wide format. PhenoSieve internally converts to long format.**

---

## Important ID Rule

The `gene_id` must match the FASTA header, or users must provide an ID mapping file.

Example FASTA:

```fasta
>Os01g0633500
MAVVVG...
```

Then the annotation table should use:

```tsv
gene_id
Os01g0633500
```

This may fail unless an ID map is provided:

```tsv
gene_id
LOC_Os01g44280
Os01g0633500.1
sp|Q84P23|CHS_ORYSJ
gene:Os01g0633500
```

Many real projects fail at this step because FASTA headers, GFF3 IDs, transcript IDs, protein IDs, and database IDs are inconsistent.

Therefore, PhenoSieve should eventually provide ID-checking utilities:

```bash
phenosieve check-ids \
  --annotation phenosieve_annotation.tsv \
  --fasta proteins.faa \
  --out id_check_report.tsv
```

---

## Module Definition Format

A module definition describes the expected gene set.

### Minimal module file

```tsv
module	gene_symbol	keywords
anthocyanin	CHS	chalcone synthase; naringenin-chalcone synthase
anthocyanin	CHI	chalcone isomerase
anthocyanin	DFR	dihydroflavonol reductase
anthocyanin	ANS	anthocyanidin synthase; leucoanthocyanidin dioxygenase
anthocyanin	UFGT	UDP-glucose flavonoid glucosyltransferase
```

### Recommended module file

```tsv
module	gene_symbol	aliases	keywords	ko	ec	pfam	interpro	go	mapman_bin	notes
anthocyanin	CHS	chalcone synthase; naringenin-chalcone synthase	chalcone synthase	K00660	2.3.1.74	PF00195	IPR011141	GO:0009813		early flavonoid biosynthesis
anthocyanin	DFR	dihydroflavonol reductase	dihydroflavonol reductase	K13082	1.1.1.219	PF00106		GO:0045552		late anthocyanin pathway
```

### YAML module example

```yaml
module: anthocyanin
description: Core anthocyanin biosynthesis gene module
expected_genes:
  - gene_symbol: CHS
    aliases:
      - chalcone synthase
      - naringenin-chalcone synthase
    keywords:
      - chalcone synthase
    ko:
      - K00660
    pfam:
      - PF00195
    ec:
      - 2.3.1.74
  - gene_symbol: DFR
    aliases:
      - dihydroflavonol reductase
    keywords:
      - dihydroflavonol reductase
    ko:
      - K13082
    pfam:
      - PF00106
    ec:
      - 1.1.1.219
```

---

## Planned Command-Line Usage

Basic mode:

```bash
phenosieve run \
  --module modules/anthocyanin.tsv \
  --annotation phenosieve_annotation.tsv \
  --fasta proteins.faa \
  --out anthocyanin_sieve/
```

With OrthoFinder:

```bash
phenosieve run \
  --module modules/anthocyanin.tsv \
  --annotation phenosieve_annotation.tsv \
  --fasta proteins.faa \
  --orthogroups Orthogroups.tsv \
  --gene-counts Orthogroups.GeneCount.tsv \
  --out anthocyanin_sieve/
```

With ID map:

```bash
phenosieve run \
  --module modules/anthocyanin.tsv \
  --annotation phenosieve_annotation.tsv \
  --fasta proteins.faa \
  --id-map id_map.tsv \
  --out anthocyanin_sieve/
```

Future supermatrix mode:

```bash
phenosieve supermatrix \
  --sieve-output anthocyanin_sieve/ \
  --aligner mafft \
  --out anthocyanin_supermatrix/
```

---

## Output Files

| Output | Description |
|---|---|
| `candidate_genes.tsv` | Main candidate gene table |
| `candidate_orthogroups.tsv` | Candidate genes grouped by orthogroup |
| `module_presence_absence.tsv` | Presence/absence matrix by gene/module/species |
| `module_copy_number.tsv` | Copy-number matrix |
| `missing_expected_genes.tsv` | Expected genes not detected |
| `ambiguous_matches.tsv` | Genes with uncertain or multi-category matches |
| `warnings.tsv` | Potential issues requiring manual inspection |
| `module_audit_report.md` | Human-readable report |
| `fasta/*.faa` | Extracted protein FASTA files per gene/module |
| `logs/phenosieve.log` | Run log |

---

## BUSCO-like Statistics

PhenoSieve will use a BUSCO-inspired vocabulary but apply it to user-defined modules rather than universal single-copy orthologs.

| Category | Meaning |
|---|---|
| `Present` | Expected gene/module detected |
| `Single-copy` | One candidate detected in a species |
| `Duplicated` | More than one candidate detected in a species |
| `Missing` | No candidate detected |
| `Ambiguous` | Candidate detected, but evidence is weak or conflicting |
| `Fragmented` | Candidate sequence appears incomplete, if length/domain checks are enabled |
| `Expanded` | Gene family appears unusually expanded |
| `Unclassified` | Candidate found but not confidently assigned to a specific expected gene |

Example summary:

```text
Module: anthocyanin
Species: Oryza_sativa

Expected genes: 6
Present: 5
Single-copy: 3
Duplicated: 2
Missing: 1
Ambiguous: 1
Completeness: 83.3%
```

Important note:

> `Missing` means "not detected under the current evidence rules," not necessarily biologically absent.

---

## Matching Strategy

PhenoSieve should support several matching evidence types.

| Evidence type | Example | Strength |
|---|---|---|
| KO match | `K00660` | Strong |
| EC match | `2.3.1.74` | Strong |
| Pfam match | `PF00195` | Strong/moderate |
| InterPro match | `IPR011141` | Strong/moderate |
| GO match | `GO:0009813` | Moderate |
| MapMan bin match | `16.8 secondary metabolism` | Moderate |
| Gene symbol match | `CHS` | Moderate, but risky |
| Keyword match | `chalcone synthase` | Useful, but should be audited |
| BLAST/DIAMOND best hit | `CHS1_ARATH` | Useful, depends on quality |

Early versions should be conservative. When evidence conflicts, PhenoSieve should report ambiguity rather than forcing assignment.

---

## Future Supermatrix Helper

A future PhenoSieve mode should support pathway/module-based phylogenomics.

Instead of using all orthogroups or universal BUSCO markers, users could build a tree from standardized curated modules.

Example:

```text
anthocyanin genes only
cell-wall remodeling genes only
aroma-associated genes only
lignin biosynthesis genes only
salt-response module only
```

Planned workflow:

```text
Per-gene FASTA output
        ↓
Align each gene separately
        ↓
Trim alignments
        ↓
Check species occupancy
        ↓
Concatenate into supermatrix
        ↓
Export partition file
        ↓
Run downstream tree inference
```

Planned outputs:

```text
supermatrix/
├── module_supermatrix.faa
├── module_supermatrix.fna
├── partitions.txt
├── occupancy_matrix.tsv
├── alignment_summary.tsv
├── excluded_genes.tsv
└── warnings.md
```

External tools may include:

- MAFFT;
- MUSCLE;
- trimAl;
- ClipKIT;
- IQ-TREE;
- RAxML-NG;
- FastTree.

PhenoSieve does not need to replace these tools. It can prepare standardized inputs and optionally call them later.

---

## Planned Repository Structure

```text
PhenoSieve/
├── README.md
├── pyproject.toml
├── LICENSE
├── phenosieve/
│   ├── __init__.py
│   ├── cli.py
│   ├── parsers.py
│   ├── normalize.py
│   ├── modules.py
│   ├── matcher.py
│   ├── fasta.py
│   ├── orthogroups.py
│   ├── stats.py
│   ├── report.py
│   └── supermatrix.py
├── modules/
│   ├── anthocyanin.tsv
│   ├── carotenoid.tsv
│   ├── lignin.tsv
│   ├── cellulose_cell_wall.tsv
│   └── aroma_rice.tsv
├── examples/
│   ├── anthocyanin_demo/
│   └── rice_aroma_demo/
├── tests/
│   ├── test_normalize.py
│   ├── test_matcher.py
│   ├── test_fasta.py
│   └── test_stats.py
└── docs/
    ├── input_formats.md
    ├── module_format.md
    ├── annotation_conversion.md
    ├── roadmap.md
    └── related_tools.md
```

---

## Roadmap

### v0.1 — Curated module sequence extraction

- Read module TSV.
- Read normalized annotation TSV.
- Match expected genes to candidate gene IDs.
- Extract protein FASTA.
- Produce candidate gene table.
- Produce basic audit report.

### v0.2 — BUSCO-like module statistics

- Presence/absence matrix.
- Copy-number matrix.
- Missing gene table.
- Ambiguous match table.
- Basic scoring system.
- ID consistency checker.

### v0.3 — Annotation converters

- eggNOG-mapper converter.
- InterProScan converter.
- KofamScan converter.
- Mercator4/MapMan converter.
- BLAST/DIAMOND converter.

### v0.4 — OrthoFinder-aware mode

- Read `Orthogroups.tsv`.
- Read `Orthogroups.GeneCount.tsv`.
- Expand candidates by orthogroup.
- Flag duplicated/expanded gene families.
- Export orthogroup-aware FASTA files.

### v0.5 — Built-in plant module library

Starter modules may include:

- anthocyanin;
- carotenoid;
- lignin;
- cellulose/cell wall;
- cuticle/wax;
- ABA signaling;
- salt stress;
- rice aroma;
- CAM photosynthesis;
- nitrogen assimilation.

### v0.6 — Supermatrix helper

- One FASTA per expected gene.
- Alignment-ready output.
- Optional MAFFT wrapper.
- Occupancy matrix.
- Concatenation helper.
- Partition file export.

### v1.0 — Reproducible comparative gene-module phylogenomics

- Stable CLI.
- Stable input formats.
- Documented examples.
- Unit tests.
- Citation and manuscript-ready documentation.

---

## Design Philosophy

PhenoSieve follows five principles.

### 1. Curation first

PhenoSieve depends on curated gene/module definitions. It does not pretend to infer biology from phenotype words automatically.

### 2. Annotation-aware but not annotation-dependent

It can use KEGG, Pfam, GO, EC, MapMan, eggNOG, InterPro, Mantis, BLAST, DIAMOND, or custom keywords.

### 3. Orthogroup-aware when possible

OrthoFinder output can help distinguish single-copy genes, duplicated candidates, and gene-family expansions.

### 4. Audit-oriented

Missing genes, duplicated genes, ambiguous matches, and weak evidence should be reported clearly.

### 5. Sequence-first

The main product is not only a table. PhenoSieve should extract usable sequence files for downstream comparative genomics, alignment, and phylogenetics.

---

## Database and Licensing Notes

Some external databases have their own licensing and access conditions.

Users are responsible for following the terms of each database or tool, especially when using:

- KEGG;
- KEGG REST;
- KOfam;
- PlantCyc / PMN;
- MetaCyc;
- InterPro;
- Pfam;
- eggNOG;
- MapMan / Mercator.

PhenoSieve should not redistribute restricted database content unless permitted. Instead, early versions should allow users to provide their own annotation outputs or locally prepared module definition files.

For KEGG-derived modules, users should verify whether their intended usage is compatible with KEGG licensing and access conditions.

---

## Related Tools and Resources

### Completeness and orthology

- BUSCO
- OrthoFinder
- BuscoPhylo

### Functional annotation

- eggNOG-mapper
- InterProScan
- KofamKOALA / KofamScan
- KAAS
- BlastKOALA / GhostKOALA
- Mercator4 / MapMan4
- Mantis
- BLAST / DIAMOND

### Plant metabolism and pathway resources

- PlantCyc
- Plant Metabolic Network
- MapMan
- Mercator4
- KEGG PATHWAY
- KEGG MODULE
- MetaCyc

### KEGG/pathway extraction and enrichment neighbors

- KEGG_Extractor
- GPATHEX
- keggtools
- KEGGREST
- clusterProfiler

### Microbial metabolism profiling neighbors

- DRAM
- METABOLIC
- GapMind

---

## References

Aramaki, T., Blanc-Mathieu, R., Endo, H., Ohkubo, K., Kanehisa, M., Goto, S., & Ogata, H. (2020). KofamKOALA: KEGG Ortholog assignment based on profile HMM and adaptive score threshold. *Bioinformatics, 36*(7), 2251–2252. https://doi.org/10.1093/bioinformatics/btz859

Emms, D. M., & Kelly, S. (2019). OrthoFinder: Phylogenetic orthology inference for comparative genomics. *Genome Biology, 20*, 238. https://doi.org/10.1186/s13059-019-1832-y

Hawkins, C., Xue, B., Yasmin, F., Wyatt, G., Zerbe, P., & Rhee, S. Y. (2025). Plant Metabolic Network 16: Expansion of underrepresented plant groups and experimentally supported enzyme data. *Nucleic Acids Research, 53*(D1), D1606–D1613. https://doi.org/10.1093/nar/gkae991

Huerta-Cepas, J., Forslund, K., Coelho, L. P., Szklarczyk, D., Jensen, L. J., von Mering, C., & Bork, P. (2017). Fast genome-wide functional annotation through orthology assignment by eggNOG-mapper. *Molecular Biology and Evolution, 34*(8), 2115–2122. https://doi.org/10.1093/molbev/msx148

Jones, P., Binns, D., Chang, H.-Y., Fraser, M., Li, W., McAnulla, C., McWilliam, H., Maslen, J., Mitchell, A., Nuka, G., Pesseat, S., Quinn, A. F., Sangrador-Vegas, A., Scheremetjew, M., Yong, S.-Y., Lopez, R., & Hunter, S. (2014). InterProScan 5: Genome-scale protein function classification. *Bioinformatics, 30*(9), 1236–1240. https://doi.org/10.1093/bioinformatics/btu031

Kanehisa, M., Sato, Y., & Morishima, K. (2016). BlastKOALA and GhostKOALA: KEGG tools for functional characterization of genome and metagenome sequences. *Journal of Molecular Biology, 428*(4), 726–731. https://doi.org/10.1016/j.jmb.2015.11.006

Kanehisa, M., Sato, Y., Kawashima, M., Furumichi, M., & Tanabe, M. (2016). KEGG as a reference resource for gene and protein annotation. *Nucleic Acids Research, 44*(D1), D457–D462. https://doi.org/10.1093/nar/gkv1070

Manni, M., Berkeley, M. R., Seppey, M., Simão, F. A., & Zdobnov, E. M. (2021). BUSCO update: Novel and streamlined workflows along with broader and deeper phylogenetic coverage for scoring of eukaryotic, prokaryotic, and viral genomes. *Molecular Biology and Evolution, 38*(10), 4647–4654. https://doi.org/10.1093/molbev/msab199

Moriya, Y., Itoh, M., Okuda, S., Yoshizawa, A. C., & Kanehisa, M. (2007). KAAS: An automatic genome annotation and pathway reconstruction server. *Nucleic Acids Research, 35*(Web Server issue), W182–W185. https://doi.org/10.1093/nar/gkm321

Queirós, P., Delogu, F., Hickl, O., May, P., & Wilmes, P. (2021). Mantis: Flexible and consensus-driven genome annotation. *GigaScience, 10*(6), giab042. https://doi.org/10.1093/gigascience/giab042

Sahbou, A.-E., Iraqi, D., Mentag, R., & Khayi, S. (2022). BuscoPhylo: A webserver for BUSCO-based phylogenomic analysis for non-specialists. *Scientific Reports, 12*, 17352. https://doi.org/10.1038/s41598-022-22461-0

Schwacke, R., Ponce-Soto, G. Y., Krause, K., Bolger, A. M., Arsova, B., Hallab, A., Gruden, K., Stitt, M., Bolger, M. E., & Usadel, B. (2019). MapMan4: A refined protein classification and annotation framework applicable to multi-omics data analysis. *Molecular Plant, 12*(6), 879–892. https://doi.org/10.1016/j.molp.2019.01.003

Shaffer, M., Borton, M. A., McGivern, B. B., Zayed, A. A., La Rosa, S. L., Solden, L. M., Liu, P., Narrowe, A. B., Rodríguez-Ramos, J., Bolduc, B., Gazitúa, M. C., Daly, R. A., Smith, G. J., Vik, D. R., Pope, P. B., Sullivan, M. B., Roux, S., & Wrighton, K. C. (2020). DRAM for distilling microbial metabolism to automate the curation of microbiome function. *Nucleic Acids Research, 48*(16), 8883–8900. https://doi.org/10.1093/nar/gkaa621

Simão, F. A., Waterhouse, R. M., Ioannidis, P., Kriventseva, E. V., & Zdobnov, E. M. (2015). BUSCO: Assessing genome assembly and annotation completeness with single-copy orthologs. *Bioinformatics, 31*(19), 3210–3212. https://doi.org/10.1093/bioinformatics/btv351

Zhang, C., Chen, Z., Zhang, M., & Jia, S. (2023). KEGG_Extractor: An effective extraction tool for KEGG Orthologs. *Genes, 14*(2), 386. https://doi.org/10.3390/genes14020386

Zhou, Z., Tran, P. Q., Breister, A. M., Liu, Y., Kieft, K., Cowley, E. S., Karaoz, U., & Anantharaman, K. (2022). METABOLIC: High-throughput profiling of microbial genomes for functional traits, metabolism, biogeochemistry, and community-scale functional networks. *Microbiome, 10*, 33. https://doi.org/10.1186/s40168-021-01213-8

---

## Notes on Closest Neighbors

- **KEGG_Extractor** is probably the closest sequence-extraction neighbor because it extracts/classifies amino acid and nucleotide sequences from KEGG annotation results. PhenoSieve should acknowledge it clearly.
- **GPATHEX** is a recent KEGG pathway/taxonomic information extractor available on PyPI. It appears related to KEGG data extraction, but it is not identical to PhenoSieve's planned module-based comparative genomics workflow.
- **BuscoPhylo** is highly relevant to the future supermatrix helper, but its marker system is BUSCO-based rather than custom curated pathway/module-based.
- **DRAM, METABOLIC, and GapMind** are important conceptual neighbors for microbial metabolism profiling, but PhenoSieve is planned for general comparative gene-module extraction with a strong plant/non-model organism emphasis.

---

## Suggested Citation Statement for Early GitHub Releases

Until a formal software paper exists, users may cite the GitHub repository:

```text
PhenoSieve: curated gene-set sequence calling for comparative genomics.
GitHub repository: [repository URL to be added]
```

---

## Development Philosophy

PhenoSieve should be small before it becomes clever.

Early versions should do a few things well:

1. read clean input files;
2. match curated gene/module definitions to annotation tables;
3. extract FASTA sequences reliably;
4. report missing, duplicated, and ambiguous cases honestly;
5. avoid overclaiming biological interpretation.

The long-term vision is not to replace expert curation, but to make expert curation computationally reusable.

---

## Author

This project is curated by **Adhityo Wicaksono**.
Plant molecular biologist and bioinformatician.

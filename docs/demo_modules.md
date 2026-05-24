# Demo modules

PhenoSieve v0.1 includes six toy/demo modules:

1. Anthocyanin/flavonoid demo
2. Carotenoid core
3. Lignin core
4. Cellulose/cell-wall core
5. ABA signaling core
6. Nitrogen assimilation core

## Important note

These modules are starter examples for software testing and demonstration.

They are **not final biological reference libraries**.

For real analysis, users should curate module files from appropriate sources such as:

- KEGG/Kofam;
- InterProScan/Pfam;
- GO;
- Mercator4/MapMan;
- PlantCyc/PMN;
- literature-curated gene lists;
- expert manual review.

## Why multiple modules?

Using several module types helps test whether PhenoSieve can handle:

- enzyme-centered pathways;
- transcription-factor-rich modules;
- cell-wall modules;
- signaling modules;
- nutrient-assimilation modules.

This prepares the tool for future database-derived and user-curated biological modules.

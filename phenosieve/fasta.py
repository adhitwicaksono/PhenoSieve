from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass
class FastaRecord:
    id: str
    description: str
    sequence: str


def read_fasta(path: str | Path) -> Dict[str, FastaRecord]:
    """Read a FASTA file.

    Uses the first whitespace-delimited token after '>' as the record ID.
    """
    path = Path(path)
    records: Dict[str, FastaRecord] = {}
    current_id = None
    current_desc = ""
    chunks: List[str] = []

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith(">"):
                if current_id is not None:
                    records[current_id] = FastaRecord(current_id, current_desc, "".join(chunks))
                current_desc = line[1:].strip()
                current_id = current_desc.split()[0]
                chunks = []
            else:
                chunks.append(line.strip())

    if current_id is not None:
        records[current_id] = FastaRecord(current_id, current_desc, "".join(chunks))

    return records


def write_fasta(path: str | Path, records: Iterable[FastaRecord], width: int = 80) -> None:
    """Write FASTA records."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for rec in records:
            desc = rec.description or rec.id
            if not desc.startswith(rec.id):
                desc = f"{rec.id} {desc}"
            handle.write(f">{desc}\n")
            seq = rec.sequence
            for i in range(0, len(seq), width):
                handle.write(seq[i:i + width] + "\n")


def subset_records(records: Dict[str, FastaRecord], ids: Iterable[str]) -> List[FastaRecord]:
    """Return records matching IDs, preserving the requested order where possible."""
    selected = []
    for gene_id in ids:
        if gene_id in records:
            selected.append(records[gene_id])
    return selected

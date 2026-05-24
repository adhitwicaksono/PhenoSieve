from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Iterable, Any


def read_tsv(path: str | Path) -> List[Dict[str, str]]:
    """Read a TSV file into a list of dictionaries.

    Blank cells are normalized to empty strings.
    """
    path = Path(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise ValueError(f"No header found in TSV file: {path}")
        rows = []
        for row in reader:
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
    return rows


def write_tsv(path: str | Path, rows: Iterable[Dict[str, Any]], fieldnames: List[str]) -> None:
    """Write dictionaries as TSV."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def split_multi(value: str) -> List[str]:
    """Split semicolon/comma/pipe-delimited annotation cells into normalized tokens."""
    if value is None:
        return []
    value = str(value).strip()
    if not value:
        return []
    # Many annotation tools use mixed delimiters. We handle common cases gently.
    for sep in ["|", ","]:
        value = value.replace(sep, ";")
    return [part.strip() for part in value.split(";") if part.strip()]


def require_columns(rows: List[Dict[str, str]], required: List[str], file_label: str) -> None:
    """Check whether rows contain required columns."""
    if not rows:
        raise ValueError(f"{file_label} is empty.")
    observed = set(rows[0].keys())
    missing = [col for col in required if col not in observed]
    if missing:
        raise ValueError(f"{file_label} missing required columns: {', '.join(missing)}")

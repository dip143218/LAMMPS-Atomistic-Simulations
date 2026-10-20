"""Run with OVITO's Python interpreter: ovitos analyze_phase_fractions_ovito.py"""
from __future__ import annotations
import csv
from pathlib import Path

try:
    from ovito.io import import_file
    from ovito.modifiers import PolyhedralTemplateMatchingModifier
except Exception:
    raise SystemExit(
        "OVITO Python/ovitos is required for automatic PTM. "
        "In OVITO Basic, apply PTM manually with RMSD cutoff 0.12."
    )

ROOT = Path(__file__).resolve().parent
TEMPERATURES = (1073, 1273, 1473, 1673, 1873, 2073, 2273)
LABELS = {0: "Other", 1: "FCC", 2: "HCP", 3: "BCC", 4: "ICO"}
rows: list[dict[str, float | int]] = []

for temperature in TEMPERATURES:
    path = ROOT / f"FCC_quenched_0K_from_{temperature}K.data"
    if not path.exists():
        raise SystemExit(f"Missing file: {path.name}")
    pipeline = import_file(str(path), atom_style="atomic")
    pipeline.modifiers.append(PolyhedralTemplateMatchingModifier(rmsd_cutoff=0.12))
    data = pipeline.compute()
    structure_types = data.particles["Structure Type"]
    total = len(structure_types)
    counts = {key: 0 for key in LABELS}
    for value in structure_types:
        key = int(value)
        counts[key if key in counts else 0] += 1
    row: dict[str, float | int] = {"temperature_K": temperature, "atoms": total}
    for key, label in LABELS.items():
        row[f"{label}_fraction"] = counts[key] / total
    row["crystalline_fraction"] = (counts[1] + counts[2] + counts[3]) / total
    rows.append(row)

output = ROOT / "PTM_phase_fractions.csv"
fields = [
    "temperature_K", "atoms", "Other_fraction", "FCC_fraction", "HCP_fraction",
    "BCC_fraction", "ICO_fraction", "crystalline_fraction",
]
with output.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print(f"Saved {output.name}")

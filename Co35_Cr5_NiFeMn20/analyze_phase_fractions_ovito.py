"""Run with OVITO's Python interpreter: ovitos analyze_phase_fractions_ovito.py"""
from __future__ import annotations

import csv
from pathlib import Path

from ovito.io import import_file
from ovito.modifiers import PolyhedralTemplateMatchingModifier

ROOT = Path(__file__).resolve().parent
FILES = sorted(ROOT.glob("FCC_quenched_0K_from_*K.data"))
if not FILES:
    raise SystemExit("No FCC_quenched_0K_from_*K.data files found. Run the batch simulation first.")

# Standard PTM structure-type IDs in OVITO:
# 0 Other, 1 FCC, 2 HCP, 3 BCC, 4 ICO, 5 SC, 6 cubic diamond, 7 hex diamond, 8 graphene.
LABELS = {0: "Other", 1: "FCC", 2: "HCP", 3: "BCC", 4: "ICO"}
rows = []

for path in FILES:
    pipeline = import_file(str(path), atom_style="atomic")
    pipeline.modifiers.append(
        PolyhedralTemplateMatchingModifier(
            rmsd_cutoff=0.12,
            output_interatomic_distance=True,
        )
    )
    data = pipeline.compute()
    structure_types = data.particles["Structure Type"]
    total = len(structure_types)
    counts = {key: 0 for key in LABELS}
    for value in structure_types:
        value = int(value)
        if value in counts:
            counts[value] += 1
        else:
            counts[0] += 1

    temp = int(path.stem.split("_")[-1].replace("K", ""))
    row = {"source_temperature_K": temp, "atoms": total}
    for key, label in LABELS.items():
        row[f"{label}_fraction"] = counts[key] / total
    row["crystalline_fraction"] = (counts[1] + counts[2] + counts[3]) / total
    rows.append(row)

rows.sort(key=lambda row: row["source_temperature_K"])
out = ROOT / "PTM_phase_fractions.csv"
fields = [
    "source_temperature_K", "atoms", "FCC_fraction", "HCP_fraction",
    "BCC_fraction", "ICO_fraction", "Other_fraction", "crystalline_fraction"
]
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {out.name}")
for row in rows:
    print(
        f"{row['source_temperature_K']} K: "
        f"FCC={row['FCC_fraction']:.3f}, HCP={row['HCP_fraction']:.3f}, "
        f"BCC={row['BCC_fraction']:.3f}, Other={row['Other_fraction']:.3f}"
    )

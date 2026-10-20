from __future__ import annotations
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = 8.314462618

C = {"Co": 0.25, "Cr": 0.25, "Fe": 0.0, "Mn": 0.25, "Ni": 0.25}
RADIUS = {"Co": 135.0, "Cr": 140.0, "Fe": 140.0, "Mn": 140.0, "Ni": 135.0}
TM = {"Co": 1768.0, "Cr": 2180.0, "Fe": 1811.0, "Mn": 1519.0, "Ni": 1728.0}
DENS = {"Co": 8.900, "Cr": 7.190, "Fe": 7.874, "Mn": 7.210, "Ni": 8.908}
VEC = {"Co": 9.0, "Cr": 6.0, "Fe": 8.0, "Mn": 7.0, "Ni": 10.0}

def weighted(values: dict[str, float]) -> float:
    return sum(C[element] * values[element] for element in C)

positive_fractions = [fraction for fraction in C.values() if fraction > 0.0]
s_over_r = -sum(fraction * math.log(fraction) for fraction in positive_fractions)
s_mix = s_over_r * R
mean_radius = weighted(RADIUS)
delta = 100.0 * math.sqrt(
    sum(C[element] * (1.0 - RADIUS[element] / mean_radius) ** 2 for element in C)
)
lambda_value = s_over_r / (delta ** 2)
mean_tm = weighted(TM)
mean_density = weighted(DENS)
vec = weighted(VEC)

rows = [
    ("composition", "Co25Cr25Fe0Mn25Ni25", "label", "direct input"),
    ("active_element_count", 4, "count", "Fe fraction is zero"),
    ("Sconf_over_R", s_over_r, "dimensionless", "-sum(ci ln ci), excluding zero fractions"),
    ("Sconf", s_mix, "J/mol/K", "configurational entropy"),
    ("mean_atomic_radius", mean_radius, "pm", "composition-weighted property"),
    ("atomic_size_difference_delta", delta, "%", "direct formula"),
    ("Lambda", lambda_value, "dimensionless", "Sconf/R divided by delta squared"),
    ("mean_melting_point", mean_tm, "K", "weighted elemental descriptor; not simulated melting"),
    ("mean_elemental_density", mean_density, "g/cm3", "weighted elemental descriptor; compare with relaxed LAMMPS density"),
    ("VEC", vec, "dimensionless", "composition-weighted property"),
]

output = ROOT / "formula_features_Co25Cr25Fe0Mn25Ni25.csv"
with output.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["feature", "value", "unit", "source"])
    writer.writerows(rows)

print("=== Co25Cr25Fe0Mn25Ni25 formula features ===")
for feature, value, unit, _ in rows:
    print(f"{feature:34s}: {value} {unit}")
print(f"Saved {output.name}")

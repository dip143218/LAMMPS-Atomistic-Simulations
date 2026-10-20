from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = 8.314462618
COMPOSITION = {"Co": 0.20, "Cr": 0.20, "Fe": 0.05, "Mn": 0.35, "Ni": 0.20}

# Property constants used for direct composition-weighted calculations.
# These are not outputs of LAMMPS. Replace them if the web app uses a different table.
ATOMIC_RADIUS_PM = {"Co": 135.0, "Cr": 140.0, "Fe": 140.0, "Mn": 140.0, "Ni": 135.0}
MELTING_POINT_K = {"Co": 1768.0, "Cr": 2180.0, "Fe": 1811.0, "Mn": 1519.0, "Ni": 1728.0}
ELEMENT_DENSITY_G_CM3 = {"Co": 8.900, "Cr": 7.190, "Fe": 7.874, "Mn": 7.210, "Ni": 8.908}
VEC = {"Co": 9.0, "Cr": 6.0, "Fe": 8.0, "Mn": 7.0, "Ni": 10.0}


def weighted(values: dict[str, float]) -> float:
    return sum(COMPOSITION[e] * values[e] for e in COMPOSITION)


def main() -> None:
    s_over_r = -sum(x * math.log(x) for x in COMPOSITION.values())
    s_mix = s_over_r * R
    rbar = weighted(ATOMIC_RADIUS_PM)
    delta = 100.0 * math.sqrt(sum(COMPOSITION[e] * (1.0 - ATOMIC_RADIUS_PM[e] / rbar) ** 2 for e in COMPOSITION))
    mean_tm = weighted(MELTING_POINT_K)
    mean_density = weighted(ELEMENT_DENSITY_G_CM3)
    mean_vec = weighted(VEC)
    lambda_value = s_over_r / (delta ** 2)

    rows = [
        ("composition", "Co20Cr20Fe5Mn35Ni20", "label", "direct input"),
        ("Sconf_over_R", s_over_r, "dimensionless", "direct formula"),
        ("Sconf", s_mix, "J/mol/K", "direct formula"),
        ("mean_atomic_radius", rbar, "pm", "weighted property formula"),
        ("atomic_size_difference_delta", delta, "%", "direct formula"),
        ("Lambda", lambda_value, "dimensionless", "direct formula"),
        ("mean_melting_point", mean_tm, "K", "weighted property formula; not LAMMPS"),
        ("mean_elemental_density", mean_density, "g/cm3", "weighted property formula; not relaxed LAMMPS density"),
        ("VEC", mean_vec, "dimensionless", "weighted property formula"),
    ]

    out = ROOT / "formula_features_Mn35Fe5.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["feature", "value", "unit", "source"])
        writer.writerows(rows)

    print("=== Co20Cr20Fe5Mn35Ni20 direct formula features ===")
    for feature, value, unit, source in rows[1:]:
        if isinstance(value, float):
            print(f"{feature:32s}: {value:.12f} {unit}  [{source}]")
        else:
            print(f"{feature:32s}: {value} {unit}  [{source}]")
    print(f"Saved: {out.name}")
    print("Note: mean melting point and weighted elemental density are formula values, not simulation outputs.")
    print("Omega requires a selected DeltaHmix definition; compare only after choosing app, elemental-reference, or FCC-reference DeltaHmix.")


if __name__ == "__main__":
    main()

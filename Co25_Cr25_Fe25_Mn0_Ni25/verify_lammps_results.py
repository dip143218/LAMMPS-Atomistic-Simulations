from __future__ import annotations
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = 8.314462618
EV_TO_KJMOL = 96.4853321233
C = {"Co": 0.25, "Cr": 0.25, "Fe": 0.25, "Mn": 0.0, "Ni": 0.25}

# Same-potential 0 K pure-element references established in the earlier
# Co-Cr-Fe-Mn-Ni verification. Mn contributes zero weight in this alloy.
NATIVE = {
    "Co": -4.409213994265,
    "Cr": -4.100000003071,
    "Fe": -4.290209683564,
    "Mn": -2.898845002119,
    "Ni": -4.450000000004,
}
FCC_REFERENCE = {
    "Co": -4.405592724875,
    "Cr": -4.013013100025,
    "Fe": -4.242099209160,
    "Mn": -2.909004052582,
    "Ni": -4.450000000004,
}

def read_csv(name: str) -> list[dict[str, str]]:
    path = ROOT / name
    if not path.exists():
        raise SystemExit(f"Required file not found: {name}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def weighted_reference(values: dict[str, float]) -> float:
    return sum(C[element] * values[element] for element in C)

main_rows = read_csv("FCC_main_summary.csv")
phase_rows = read_csv("phase_0K_energies.csv")
quench_rows = read_csv("FCC_quench_0K_summary.csv")
relaxed = next(row for row in main_rows if row["state"] == "FCC_0K_relaxed")
alloy_energy = float(relaxed["energy_eV_per_atom"])

native_ref = weighted_reference(NATIVE)
fcc_ref = weighted_reference(FCC_REFERENCE)
dh_native = (alloy_energy - native_ref) * EV_TO_KJMOL
dh_fcc = (alloy_energy - fcc_ref) * EV_TO_KJMOL

phase_ranking = sorted(
    [(row["starting_phase"].upper(), float(row["energy_eV_per_atom"])) for row in phase_rows],
    key=lambda item: item[1],
)
quench_values = [
    (int(float(row["source_temperature_K"])), float(row["energy_eV_per_atom"]))
    for row in quench_rows
]
best_quench = min(quench_values, key=lambda item: item[1])
positive_fractions = [fraction for fraction in C.values() if fraction > 0.0]
s_over_r = -sum(fraction * math.log(fraction) for fraction in positive_fractions)

output = ROOT / "LAMMPS_verification_summary.csv"
with output.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["metric", "value", "unit"])
    writer.writerow(["Sconf_over_R", f"{s_over_r:.12f}", "dimensionless"])
    writer.writerow(["Sconf", f"{s_over_r * R:.12f}", "J/mol/K"])
    writer.writerow(["alloy_energy_FCC_relaxed", f"{alloy_energy:.12f}", "eV/atom"])
    writer.writerow(["relaxed_FCC_density", relaxed["density_g_cm3"], "g/cm3"])
    writer.writerow(["DeltaHmix_elemental_reference", f"{dh_native:.12f}", "kJ/mol"])
    writer.writerow(["DeltaHmix_FCC_reference", f"{dh_fcc:.12f}", "kJ/mol"])
    writer.writerow(["lowest_ideal_phase", phase_ranking[0][0], "label"])
    writer.writerow([
        "phase_gap_to_second",
        f"{(phase_ranking[1][1] - phase_ranking[0][1]) * 1000.0:.12f}",
        "meV/atom",
    ])
    writer.writerow(["lowest_quench_source_temperature", best_quench[0], "K"])
    writer.writerow(["lowest_quenched_energy", f"{best_quench[1]:.12f}", "eV/atom"])

print(f"DeltaHmix native refs = {dh_native:.6f} kJ/mol")
print(f"DeltaHmix FCC refs    = {dh_fcc:.6f} kJ/mol")
print(f"Lowest phase          = {phase_ranking[0][0]}")
print(f"Saved {output.name}")

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EV_ATOM_TO_KJ_MOL = 96.4853321233

COMPOSITION = {"Co": 0.20, "Cr": 0.20, "Fe": 0.35, "Mn": 0.20, "Ni": 0.05}

# Same pure-element energies used in the previous MEAM verification.
PURE_REFERENCE = {
    "Co": -4.409213994265,
    "Cr": -4.100000003071,
    "Fe": -4.290209683564,
    "Mn": -2.898845002119,
    "Ni": -4.450000000004,
}
FCC_CONSTRAINED_REFERENCE = {
    "Co": -4.405592724875,
    "Cr": -4.013013100025,
    "Fe": -4.242099209160,
    "Mn": -2.909004052582,
    "Ni": -4.450000000004,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path.name}")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def mixing_entropy_dimensionless() -> float:
    return -sum(x * math.log(x) for x in COMPOSITION.values() if x > 0)


def weighted_reference(energies: dict[str, float]) -> float:
    return sum(COMPOSITION[element] * energies[element] for element in COMPOSITION)


def main() -> None:
    main_rows = read_csv(ROOT / "FCC_main_summary.csv")
    phase_rows = read_csv(ROOT / "phase_0K_energies.csv")
    quench_rows = read_csv(ROOT / "FCC_quench_0K_summary.csv")

    relaxed = next((row for row in main_rows if row["state"] == "FCC_0K_relaxed"), None)
    if relaxed is None:
        raise ValueError("FCC_0K_relaxed row not found in FCC_main_summary.csv")
    alloy_energy = float(relaxed["energy_eV_per_atom"])

    phase_energy = {
        row["starting_phase"].strip().upper(): float(row["energy_eV_per_atom"])
        for row in phase_rows
    }
    ordered = sorted(phase_energy.items(), key=lambda item: item[1])
    lowest_phase, lowest_energy = ordered[0]
    second_phase, second_energy = ordered[1]
    gap_mev = (second_energy - lowest_energy) * 1000.0

    quenched = [
        (int(float(row["source_temperature_K"])), float(row["energy_eV_per_atom"]))
        for row in quench_rows
    ]
    best_quench_T, best_quench_energy = min(quenched, key=lambda item: item[1])

    eref_elemental = weighted_reference(PURE_REFERENCE)
    dh_elemental = (alloy_energy - eref_elemental) * EV_ATOM_TO_KJ_MOL
    eref_fcc = weighted_reference(FCC_CONSTRAINED_REFERENCE)
    dh_fcc = (alloy_energy - eref_fcc) * EV_ATOM_TO_KJ_MOL

    sconf_r = mixing_entropy_dimensionless()

    print("\n=== Co20Cr20Fe35Mn20Ni5 LAMMPS verification ===")
    print(f"Composition sum             : {sum(COMPOSITION.values()):.3f}")
    print(f"Configurational entropy/R   : {sconf_r:.6f}")
    print(f"Configurational entropy     : {sconf_r * 8.314462618:.6f} J mol^-1 K^-1")
    print(f"Relaxed FCC alloy energy    : {alloy_energy:.12f} eV/atom")
    print(f"DeltaHmix, elemental refs   : {dh_elemental:.6f} kJ/mol")
    print(f"DeltaHmix, FCC refs         : {dh_fcc:.6f} kJ/mol")
    print()
    print("Independent 0 K phase-energy ranking:")
    for phase, energy in ordered:
        print(f"  {phase:3s}: {energy:.12f} eV/atom")
    print(f"Lowest starting lattice     : {lowest_phase}")
    print(f"Gap to second-lowest        : {gap_mev:.6f} meV/atom ({second_phase})")
    print(f"Lowest quenched energy      : {best_quench_energy:.12f} eV/atom from {best_quench_T} K")

    print("\nInterpretation:")
    if gap_mev >= 20.0:
        print("A clear 0 K energetic preference is present among the three ideal lattices.")
    elif gap_mev >= 5.0:
        print("The phase-energy preference is modest; finite-temperature entropy may change stability.")
    else:
        print("The leading phases are nearly degenerate; multiphase/metastable behavior is plausible.")
    print("This ranking alone cannot prove single-phase formation.")
    print("Use PTM phase fractions from analyze_phase_fractions_ovito.py on the quenched structures.")
    print("The web-app probability (for example 89.87%) cannot be reproduced directly by LAMMPS;")
    print("LAMMPS provides independent energetic and structural evidence for or against that prediction.")

    output = ROOT / "LAMMPS_verification_summary.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value", "unit"])
        writer.writerow(["Sconf_over_R", f"{sconf_r:.12f}", "dimensionless"])
        writer.writerow(["Sconf", f"{sconf_r * 8.314462618:.12f}", "J/mol/K"])
        writer.writerow(["alloy_energy_FCC_relaxed", f"{alloy_energy:.12f}", "eV/atom"])
        writer.writerow(["DeltaHmix_elemental_reference", f"{dh_elemental:.12f}", "kJ/mol"])
        writer.writerow(["DeltaHmix_FCC_reference", f"{dh_fcc:.12f}", "kJ/mol"])
        writer.writerow(["lowest_ideal_phase", lowest_phase, "label"])
        writer.writerow(["phase_gap_to_second", f"{gap_mev:.12f}", "meV/atom"])
        writer.writerow(["lowest_quench_source_temperature", best_quench_T, "K"])
        writer.writerow(["lowest_quenched_energy", f"{best_quench_energy:.12f}", "eV/atom"])
    print(f"\nSaved: {output.name}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, KeyError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

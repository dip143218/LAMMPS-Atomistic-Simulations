from __future__ import annotations
import hashlib
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
checks: list[tuple[bool, str]] = []

def add(condition: bool, message: str) -> None:
    checks.append((condition, message))
    print(("PASS: " if condition else "FAIL: ") + message)

def text(name: str) -> str:
    path = ROOT / name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")

def sha256(name: str) -> str:
    digest = hashlib.sha256()
    with (ROOT / name).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

main_name = "run_FCC_Choi_5760_Co0Cr25Fe25Mn25Ni25.in"
phase_name = "phase_energy_5760_Co0Cr25Fe25Mn25Ni25.in"
main = text(main_name)
phase = text(phase_name)
batch = text("RUN_ALL_6CORE_Co0Cr25Fe25Mn25Ni25.bat")

add((ROOT / "library.meam").exists(), "library.meam exists")
add((ROOT / "CoNiCrFeMn.meam").exists(), "CoNiCrFeMn.meam exists")
if (ROOT / "library.meam").exists():
    add(sha256("library.meam") == "3948e51e15f706e29bd8fee24944a9043be418b611ad8748e7efcc2d8df6f1cb", "library.meam checksum matches the supplied Choi file")
if (ROOT / "CoNiCrFeMn.meam").exists():
    add(sha256("CoNiCrFeMn.meam") == "11d8c6a2ca849ead980585c8acca1b56088b8d88ee006c6127d09f57b20d5aea", "CoNiCrFeMn.meam checksum matches the supplied file")

mapping = "pair_coeff * * library.meam Co Ni Cr Fe Mn CoNiCrFeMn.meam Co Cr Fe Mn Ni"
add(mapping in main, "main MEAM mapping is unchanged")
add(mapping in phase, "phase-screen MEAM mapping is unchanged")
add("set type 1 type/subset 2 1440" in main, "Cr atom count is 1440")
add("set type 1 type/subset 3 1440" in main, "Fe atom count is 1440")
add("set type 1 type/subset 4 1440" in main, "Mn atom count is 1440")
add("set type 1 type/subset 5 1440" in main, "Ni atom count is 1440")
add("set type 1 type/subset 2 1440" in main and "set type 1 type/subset 5 1440" in main, "all 5760 original Co atoms are converted to Cr/Fe/Mn/Ni")
add("Co=0, Cr=1440, Fe=1440, Mn=1440, Ni=1440" in main, "composition comment confirms 5760 total atoms")

present_fixes = ["SW23", "SW24", "SW25", "SW34", "SW35", "SW45"]
add(all(f"fix {name} all atom/swap 6 1" in main for name in present_fixes), "six present-element pair-swap fixes use equal sampling")
add(all(name not in main for name in ["SW12", "SW13", "SW14", "SW15"]), "no invalid Co-involving swap fixes")
add("run 10002" in main, "CMC block gives 1667 attempts per pair and 10002 total attempts")
add("variable Tlist index 1073 1273 1473 1673 1873 2073 2273" in main, "seven-temperature ladder is unchanged")
add("run 50000" in main, "50 ps per ladder temperature is unchanged")
add('if "${PHASE} == HCP" then "region ebox block 0 12 0 12 0 10 units lattice"' in phase, "HCP screen creates 5760 atoms")
add('if "${PHASE} == BCC" then "region ebox block 0 12 0 12 0 20 units lattice"' in phase, "BCC screen creates 5760 atoms")
add("-np 6" in batch, "batch uses 6 MPI processes")
add("RUN_MELTING" not in batch and "auto_melting" not in batch and "coexistence" not in batch, "no melting workflow is included")

for script in [
    "calculate_formula_features.py", "verify_lammps_results.py",
    "build_app_feature_report.py", "analyze_phase_fractions_ovito.py",
]:
    try:
        py_compile.compile(str(ROOT / script), doraise=True)
        add(True, f"Python syntax: {script}")
    except Exception as exc:
        add(False, f"Python syntax: {script}: {exc}")

passed = all(condition for condition, _ in checks)
report = ROOT / "RECHECK_REPORT.txt"
report.write_text(
    "Co0Cr25Fe25Mn25Ni25 package static recheck\n\n"
    + "\n".join(("PASS: " if ok else "FAIL: ") + msg for ok, msg in checks)
    + f"\n\nOVERALL: {'PASS' if passed else 'FAIL'}\n",
    encoding="utf-8",
)
print(f"OVERALL: {'PASS' if passed else 'FAIL'}")
print(f"Saved: {report.name}")
raise SystemExit(0 if passed else 1)

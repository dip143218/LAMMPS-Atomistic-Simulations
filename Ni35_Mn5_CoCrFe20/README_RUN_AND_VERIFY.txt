COMPOSITION
Co 20 at percent = 1152 atoms
Cr 20 at percent = 1152 atoms
Fe 20 at percent = 1152 atoms
Mn  5 at percent =  288 atoms
Ni 35 at percent = 2016 atoms
Total            = 5760 atoms

ATOM TYPE MAPPING
Type 1 = Co
Type 2 = Cr
Type 3 = Fe
Type 4 = Mn
Type 5 = Ni

MEAM COEFFICIENT
The pair coefficient is exactly unchanged:
pair_coeff * * library.meam Co Ni Cr Fe Mn CoNiCrFeMn.meam Co Cr Fe Mn Ni

FILES IN THIS PACKAGE
1. library.meam
2. CoNiCrFeMn.meam
3. run_FCC_Choi_5760_Ni35_Mn5.in
4. phase_energy_5760_Ni35_Mn5.in
5. quench_one_temperature.in
6. RUN_ALL_6CORE_Ni35_Mn5.bat
7. verify_lammps_results.py
8. analyze_phase_fractions_ovito.py
9. RECHECK_REPORT.txt

WINDOWS CMD RUN
Open CMD in this folder and run:
call RUN_ALL_6CORE_Ni35_Mn5.bat

The batch file uses six MPI processes and automatically performs:
1. FCC 0 K relaxation
2. 1073 K CMC with the same ten pair swap fixes and 10000 steps
3. Temperature ladder at 1073, 1273, 1473, 1673, 1873, 2073 and 2273 K
4. 50000 steps at each ladder temperature
5. Seven rapid 0 K minimizations
6. Independent FCC, HCP and BCC 0 K energy screens

EXPECTED MAIN OUTPUTS
FCC_main_summary.csv
FCC_ladder_summary.csv
CMC_swap_statistics.csv
FCC_quench_0K_summary.csv
phase_0K_energies.csv
FCC_hot_1073K.data through FCC_hot_2273K.data
FCC_quenched_0K_from_1073K.data through FCC_quenched_0K_from_2273K.data
Energy_FCC_relaxed_0K_5760_Ni35Mn5.data
Energy_HCP_relaxed_0K_5760_Ni35Mn5.data
Energy_BCC_relaxed_0K_5760_Ni35Mn5.data

POSTPROCESSING
Run:
python verify_lammps_results.py

For automated PTM with OVITO Python, run:
ovitos analyze_phase_fractions_ovito.py

For direct comparison with your previous composition, use the same PTM RMSD cutoff for both datasets. This script retains the previous package value of 0.15.

IMPORTANT ABOUT THE SLASH CHARACTER
Do not remove the slash from LAMMPS command names such as type/subset, atom/swap, box/relax, ave/time, pe/atom, pe/atoms and enthalpy/atoms. The slash is part of the official LAMMPS command or expression and is required. No slash is used as a file path separator inside the LAMMPS input files.

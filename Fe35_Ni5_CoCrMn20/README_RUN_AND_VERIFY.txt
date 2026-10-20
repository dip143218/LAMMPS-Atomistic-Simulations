COMPOSITION
Co 20 at% = 1152 atoms
Cr 20 at% = 1152 atoms
Fe 35 at% = 2016 atoms
Mn 20 at% = 1152 atoms
Ni  5 at% =  288 atoms
Total       = 5760 atoms

PAIR COEFFICIENT
The MEAM mapping is unchanged:
pair_coeff * * library.meam Co Ni Cr Fe Mn CoNiCrFeMn.meam Co Cr Fe Mn Ni
LAMMPS types are: 1 Co, 2 Cr, 3 Fe, 4 Mn, 5 Ni.

FILES REQUIRED IN THE SAME FOLDER
1. library.meam
2. CoNiCrFeMn.meam
3. run_FCC_Choi_5760_Fe35_Ni5.in
4. phase_energy_5760_Fe35_Ni5.in
5. quench_one_temperature.in
6. RUN_ALL_6CORE_Fe35_Ni5.bat

RUN
Double-click RUN_ALL_6CORE_Fe35_Ni5.bat.
If the executable is lmp_mpi, edit set LMP=lmp to set LMP=lmp_mpi.

WORKFLOW (same as the previous Choi-based package)
1. Create 5760-atom random FCC alloy.
2. Relax at 0 K and zero pressure.
3. Directly assign 1073 K velocities.
4. Run NPT plus ten pair-swap fixes for 10000 total attempted swaps.
5. Run 1073 to 2273 K in 200 K steps, 50 ps per temperature.
6. Rapidly minimize every equilibrated hot structure to 0 K.
7. Independently relax ideal FCC, HCP and BCC starting lattices at 0 K.

POSTPROCESSING
A. Run: python verify_lammps_results.py
This calculates composition-specific configurational entropy, two MEAM DeltaHmix definitions,
phase-energy ranking, phase-energy gap, and the lowest quenched energy.

B. Run with OVITO: ovitos analyze_phase_fractions_ovito.py
This performs PTM on every quenched data file and writes PTM_phase_fractions.csv.

HOW TO JUDGE SINGLE OR MULTIPHASE
- A single-phase claim needs one dominant PTM structure fraction over relevant temperatures,
  not merely the lowest separate FCC/HCP/BCC energy.
- Significant simultaneous FCC/HCP/BCC fractions indicate mixed local structures.
- A large 'Other' fraction may indicate disorder, defects, or an unsuitable PTM RMSD cutoff.
- Repeat with several random seeds before a strong conclusion.

IMPORTANT LIMITATION
The web/ML value 89.87% is a classifier probability, not a physical observable in LAMMPS.
LAMMPS cannot output the same probability unless the exact ML model is supplied and evaluated.
The simulation can independently support or contradict the prediction using:
DeltaHmix, 0 K phase-energy differences, temperature-dependent volume/energy, and PTM phase fractions.

For the new composition, ideal configurational entropy/R is 1.482887, not ln(5)=1.609438.
Therefore, do not reuse all equiatomic web-app feature values without recalculating them.

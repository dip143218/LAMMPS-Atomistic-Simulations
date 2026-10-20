Co25Cr25Fe25Mn0Ni25 (5760 atoms) -- Choi Co-Cr-Fe-Mn-Ni MEAM

Exact atom counts:
Co 25% = 1440
Cr 25% = 1440
Fe 25% = 1440
Mn  0% = 0
Ni 25% = 1440
Total    = 5760

One-command 6-core run:
  call RUN_ALL_6CORE_Co25Cr25Fe25Mn0Ni25.bat

The workflow performs:
1. FCC 0 K relaxation
2. 1073 K CMC/MD using only the six present-element pairs
3. 1073-2273 K ladder, 50 ps at each temperature
4. Seven direct 0 K quenches/minimizations
5. FCC/HCP/BCC 0 K screens
6. Formula descriptors, two MEAM DeltaHmix definitions, density and phase ranking
7. Optional PTM if ovitos is available

Important CMC note:
Mn has zero atoms, so Mn-involving atom/swap fixes cannot be used meaningfully.
The six Co/Cr/Fe/Ni pairs are sampled equally: 1667 attempts per pair,
10002 total attempts. All other workflow settings remain the same.

Primary outputs:
FCC_main_summary.csv
FCC_ladder_summary.csv
CMC_swap_statistics.csv
FCC_quench_0K_summary.csv
phase_0K_energies.csv
formula_features_Co25Cr25Fe25Mn0Ni25.csv
LAMMPS_verification_summary.csv
app_feature_simulation_report.csv
PTM_phase_fractions.csv (only if ovitos is installed)

No melting-point code is included.
The web-app ML probability cannot be reproduced by LAMMPS; it is marked N/A.
MeanMeltingPoint in the report is a weighted elemental descriptor, not a simulated melting point.

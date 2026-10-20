Co35Cr5Fe20Mn20Ni20 - 5760 atom LAMMPS package

Composition and LAMMPS types
  type 1 Co: 2016 atoms (35 percent, left after subset conversion)
  type 2 Cr:  288 atoms (5 percent)
  type 3 Fe: 1152 atoms (20 percent)
  type 4 Mn: 1152 atoms (20 percent)
  type 5 Ni: 1152 atoms (20 percent)
  total: 5760 atoms

Run all stages with 6 MPI ranks
  call RUN_ALL_6CORE_Co35_Cr5.bat

Live progress in a second CMD
  powershell -NoProfile -Command "Get-Content '.\log_FCC_Choi_5760_Co35Cr5.txt' -Tail 30 -Wait"

Check processes
  tasklist | findstr /I "lmp mpiexec"

After completion
  python verify_lammps_results.py
  ovitos analyze_phase_fractions_ovito.py

Correct atom counts for phase screens
  FCC: 12 x 12 x 10 x 4 = 5760
  HCP: 12 x 12 x 10 x 4 = 5760
  BCC: 12 x 12 x 20 x 2 = 5760

The MEAM pair_coeff is unchanged. Slash characters in LAMMPS styles such as type/subset, atom/swap, box/relax, ave/time and pe/atom are required LAMMPS syntax, not file paths.

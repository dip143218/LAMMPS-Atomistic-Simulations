Ni35-Mn5 HCP-only correction

Composition: Co20 Cr20 Fe20 Mn5 Ni35
Total atoms: 5760
HCP box: 12 x 12 x 10 lattice-space blocks
MEAM pair_coeff: unchanged

Put these files in the existing completed simulation folder:
- run_HCP_energy_5760_Ni35_Mn5_FIXED.in
- RUN_HCP_ONLY_6CORE_Ni35_Mn5.bat

The folder must already contain:
- library.meam
- CoNiCrFeMn.meam
- phase_0K_energies.csv (optional; the batch updates its HCP row if present)

Run in CMD:
call RUN_HCP_ONLY_6CORE_Ni35_Mn5.bat

Expected confirmation:
Created 5760 atoms
HCP CORRECTION COMPLETED SUCCESSFULLY.

Do not rerun the main FCC/CMC/temperature-ladder or the seven quench simulations.

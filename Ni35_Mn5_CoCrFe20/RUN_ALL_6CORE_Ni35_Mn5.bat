@echo off
setlocal
cd /d "%~dp0"
set LMP=lmp
set MPI=mpiexec

echo [1/3] FCC CMC and temperature ladder
%MPI% -np 6 %LMP% -in run_FCC_Choi_5760_Ni35_Mn5.in > log_FCC_Choi_5760_Ni35Mn5.txt
if errorlevel 1 goto :fail

echo [2/3] Rapid 0 K minimization of each equilibrated temperature
echo source_temperature_K,energy_eV_per_atom,enthalpy_eV_per_atom,volume_A3_per_atom,density_g_cm3>FCC_quench_0K_summary.csv
for %%T in (1073 1273 1473 1673 1873 2073 2273) do (
  echo Quenching %%T K
  %MPI% -np 6 %LMP% -var TK %%T -in quench_one_temperature.in > log_quench_%%T.txt
  if errorlevel 1 goto :fail
)

echo [3/3] Independent FCC, HCP and BCC 0 K energy screens
echo starting_phase,energy_eV_per_atom,enthalpy_eV_per_atom,volume_A3_per_atom,density_g_cm3>phase_0K_energies.csv
for %%P in (FCC HCP BCC) do (
  echo Energy screen %%P
  %MPI% -np 6 %LMP% -var PHASE %%P -in phase_energy_5760_Ni35_Mn5.in > log_energy_%%P.txt
  if errorlevel 1 goto :fail
)

echo ALL SIMULATIONS COMPLETED.
echo Next: run python verify_lammps_results.py
echo For phase fractions, run: ovitos analyze_phase_fractions_ovito.py
pause
exit /b 0

:fail
echo RUN STOPPED. CHECK THE NEWEST LOG FILE.
pause
exit /b 1

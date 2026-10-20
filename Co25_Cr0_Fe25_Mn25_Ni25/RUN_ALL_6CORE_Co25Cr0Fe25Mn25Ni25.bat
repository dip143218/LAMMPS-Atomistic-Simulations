@echo off
setlocal
cd /d "%~dp0"
set LMP=lmp
set MPI=mpiexec

where %MPI% >nul 2>nul || (echo ERROR: mpiexec not found & pause & exit /b 1)
where %LMP% >nul 2>nul || (echo ERROR: lmp not found & pause & exit /b 1)
where python >nul 2>nul || (echo ERROR: python not found & pause & exit /b 1)

echo ============================================================
echo Co25Cr0Fe25Mn25Ni25 main workflow - 6 cores
echo Same Choi-based workflow; melting calculation is NOT included.
echo ============================================================

echo [0/5] Static package recheck
python self_check_package.py
if errorlevel 1 goto :fail

echo [1/5] FCC relaxation, 1073 K CMC, temperature ladder
%MPI% -np 6 %LMP% -in run_FCC_Choi_5760_Co25Cr0Fe25Mn25Ni25.in > log_FCC_Choi_Co25Cr0Fe25Mn25Ni25.txt 2>&1
if errorlevel 1 goto :fail

echo [2/5] Seven rapid 0 K minimizations
echo source_temperature_K,energy_eV_per_atom,enthalpy_eV_per_atom,volume_A3_per_atom,density_g_cm3>FCC_quench_0K_summary.csv
for %%T in (1073 1273 1473 1673 1873 2073 2273) do (
  echo Quenching %%T K
  %MPI% -np 6 %LMP% -var TK %%T -in quench_one_temperature.in > log_quench_%%T.txt 2>&1
  if errorlevel 1 goto :fail
)

echo [3/5] Independent FCC, HCP and BCC 0 K energy screens
echo starting_phase,energy_eV_per_atom,enthalpy_eV_per_atom,volume_A3_per_atom,density_g_cm3>phase_0K_energies.csv
for %%P in (FCC HCP BCC) do (
  echo Energy screen %%P
  %MPI% -np 6 %LMP% -var PHASE %%P -in phase_energy_5760_Co25Cr0Fe25Mn25Ni25.in > log_energy_%%P.txt 2>&1
  if errorlevel 1 goto :fail
)

echo [4/5] Formula descriptors and MEAM verification
python calculate_formula_features.py
if errorlevel 1 goto :fail
python verify_lammps_results.py
if errorlevel 1 goto :fail
python build_app_feature_report.py
if errorlevel 1 goto :fail

echo [5/5] Optional automatic OVITO PTM
where ovitos >nul 2>nul
if errorlevel 1 (
  echo ovitos not found. Use OVITO Basic manually with PTM RMSD cutoff 0.12.
) else (
  ovitos analyze_phase_fractions_ovito.py
  if errorlevel 1 goto :fail
)

echo.
echo ALL SIMULATIONS AND CALCULATIONS COMPLETED.
echo Main comparison report: app_feature_simulation_report.csv
echo No melting-point calculation was run, as requested.
pause
exit /b 0

:fail
echo.
echo WORKFLOW STOPPED. Check the newest log file.
pause
exit /b 1

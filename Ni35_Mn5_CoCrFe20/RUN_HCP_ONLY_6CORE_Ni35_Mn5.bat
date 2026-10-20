@echo off
setlocal
cd /d "%~dp0"
set LMP=lmp
set MPI=mpiexec

if not exist run_HCP_energy_5760_Ni35_Mn5_FIXED.in goto :missing_input
if not exist library.meam goto :missing_potential
if not exist CoNiCrFeMn.meam goto :missing_potential

echo Running corrected HCP-only 0 K energy screen with 6 MPI processes...
%MPI% -np 6 %LMP% -in run_HCP_energy_5760_Ni35_Mn5_FIXED.in > log_energy_HCP_corrected.txt 2>&1
if errorlevel 1 goto :fail

findstr /I /C:"Created 5760 atoms" log_energy_HCP_corrected.txt >nul
if errorlevel 1 goto :atom_fail

rem Replace only the old HCP row in phase_0K_energies.csv; keep existing FCC and BCC rows.
powershell -NoProfile -Command "$p='phase_0K_energies.csv'; $h='starting_phase,energy_eV_per_atom,enthalpy_eV_per_atom,volume_A3_per_atom,density_g_cm3'; $rows=@(); if(Test-Path $p){$rows=Get-Content $p ^| Select-Object -Skip 1 ^| Where-Object {$_ -notmatch '^HCP,'}}; $new=Get-Content 'HCP_0K_corrected_Ni35Mn5.csv' ^| Select-Object -Skip 1; Set-Content -Path $p -Value $h; if($rows){Add-Content -Path $p -Value $rows}; Add-Content -Path $p -Value $new"
if errorlevel 1 goto :csv_fail

echo.
echo HCP CORRECTION COMPLETED SUCCESSFULLY.
echo Confirmed: Created 5760 atoms.
echo Corrected outputs:
echo   Energy_HCP_relaxed_0K_5760_Ni35Mn5.data
echo   HCP_0K_corrected_Ni35Mn5.csv
echo   phase_0K_energies.csv  ^(HCP row replaced; FCC and BCC kept^)
echo   log_energy_HCP_corrected.txt
echo.
echo Quick check:
findstr /I /C:"Created 5760 atoms" /C:"CORRECTED 5760-ATOM" log_energy_HCP_corrected.txt
pause
exit /b 0

:missing_input
echo ERROR: run_HCP_energy_5760_Ni35_Mn5_FIXED.in is missing.
pause
exit /b 1

:missing_potential
echo ERROR: library.meam or CoNiCrFeMn.meam is missing from this folder.
pause
exit /b 1

:atom_fail
echo ERROR: The log does not confirm 5760 atoms. Check log_energy_HCP_corrected.txt.
pause
exit /b 1

:csv_fail
echo ERROR: HCP completed, but phase_0K_energies.csv could not be updated.
echo HCP_0K_corrected_Ni35Mn5.csv still contains the valid corrected result.
pause
exit /b 1

:fail
echo ERROR: HCP run failed. Check log_energy_HCP_corrected.txt.
pause
exit /b 1

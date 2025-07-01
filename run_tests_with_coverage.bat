@echo off
REM Ejecuta los tests con cobertura en Windows

echo ============================
echo Ejecutando pruebas con cobertura...
echo ============================

REM Ejecutar los tests y guardar la cobertura
coverage run tests\run_all_tests.py

REM Mostrar el resumen en consola
coverage report -m

REM Generar el reporte visual en HTML
coverage html

REM Abrir el reporte en navegador
start htmlcov\index.html

echo.
echo ✅ Pruebas completadas. Revisa el informe en htmlcov\index.html
pause
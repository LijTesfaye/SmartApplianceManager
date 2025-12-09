
@echo off
REM ============================================================
REM  SmartApplianceManager UML Generator
REM  Generates class and package diagrams from Pyreverse
REM ============================================================

echo [INFO] Activating Conda environment: smart_env...
CALL conda activate smart_env

echo [INFO] Removing old UML diagrams...
del classes_DevSystemCore.* >nul 2>&1
del packages_DevSystemCore.* >nul 2>&1

echo [INFO] Generating UML diagrams in SVG format...
pyreverse -o svg -p DevSystemCore development_system/controller development_system/model development_system/generator

IF EXIST classes_DevSystemCore.svg (
    echo [SUCCESS] Class diagram generated: classes_DevSystemCore.svg
) ELSE (
    echo [ERROR] Failed to generate class diagram.
)

IF EXIST packages_DevSystemCore.svg (
    echo [SUCCESS] Package diagram generated: packages_DevSystemCore.svg
) ELSE (
    echo [ERROR] Failed to generate package diagram.
)

echo [INFO] Opening output folder...
explorer .

echo [DONE] UML generation completed.
pause

@echo off
REM Script para executar o Sistema de Gestão de Obras
REM CMD/Prompt de Comando

echo ==================================================
echo     Sistema de Gestão de Obras - Inicializando
echo ==================================================
echo.

REM Ativa o ambiente virtual se existir
if exist .venv\Scripts\activate.bat (
    echo [OK] Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
) else (
    echo [!] Ambiente virtual não encontrado
)

echo [OK] Executando sistema...
echo.

python main.py

echo.
echo ==================================================
echo         Sistema encerrado
echo ==================================================
pause

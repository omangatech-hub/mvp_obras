# Script para executar o Sistema de Gestão de Obras
# PowerShell

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "    Sistema de Gestão de Obras - Inicializando   " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Ativa o ambiente virtual se existir
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "✓ Ativando ambiente virtual..." -ForegroundColor Green
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠ Ambiente virtual não encontrado" -ForegroundColor Yellow
}

Write-Host "✓ Executando sistema..." -ForegroundColor Green
Write-Host ""

python main.py

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        Sistema encerrado                         " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

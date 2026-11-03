<#
.SYNOPSIS
    Script de inicialização do Sistema de Gestão Escolar (Backend e Frontend).

.DESCRIPTION
    Este script localiza o ambiente virtual (venv), inicia o servidor Django
    (responsável pelo Backend e pela entrega do Frontend - templates e arquivos estáticos)
    e abre automaticamente a aplicação no navegador.
#>

param(
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

# Garante a execução a partir do diretório raiz do projeto
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Iniciando Sistema de Gestao Escolar    " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Localização do executável Python
$VenvPython = Join-Path $ProjectRoot "venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    $PythonCmd = $VenvPython
    Write-Host "[OK] Ambiente virtual detectado: .\venv" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Ambiente virtual (venv) nao encontrado no local padrao. Tentando comando global 'python'..." -ForegroundColor Yellow
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $PythonCmd = "python"
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        $PythonCmd = "py"
    } else {
        Write-Error "Python nao foi encontrado no sistema ou na pasta venv."
        exit 1
    }
}

$ManagePy = Join-Path $ProjectRoot "backend\manage.py"
if (-not (Test-Path $ManagePy)) {
    Write-Error "manage.py nao foi encontrado em backend\manage.py."
    exit 1
}

# 2. Informações de execução
Write-Host "[INFO] Backend: Django API e Regras de Negocio" -ForegroundColor Gray
Write-Host "[INFO] Frontend: Templates e Arquivos Estaticos (servidos pelo Django)" -ForegroundColor Gray
Write-Host "[INFO] Servidor sera iniciado em: http://127.0.0.1:8000/" -ForegroundColor Gray

# 3. Abertura opcional do navegador
if (-not $NoBrowser) {
    Write-Host "[INFO] Abrindo navegador em http://127.0.0.1:8000/ ..." -ForegroundColor Gray
    Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile", "-Command", "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000/'"
}

Write-Host "`nServidor rodando! Pressione CTRL+C no terminal para encerrar.`n" -ForegroundColor Yellow

# 4. Iniciar servidor
& $PythonCmd $ManagePy runserver 127.0.0.1:8000


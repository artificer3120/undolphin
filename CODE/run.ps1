# ---
# operator: artificer
# agent: alchemist.Haldir
# session: 92d0faba-45d4-473e-93a4-e05ae658cd4b
# created: 2026-07-20
# origin: BUILD unDolphin -- launch script. Starts the local Flask app on 127.0.0.1:8790.
#         Needs VAULT_KEY + VAULT_URL in the environment (the Runware key pulls from the vault at boot).
# location: _DECK 8\LAB 70 - unDolphin\CODE\run.ps1
# release_status: draft
# version: 0.1.0
# ---
Set-Location $PSScriptRoot
if (-not $env:VAULT_KEY) { Write-Host "VAULT_KEY unset -- openVault locked. Generation will fail until you authenticate." -ForegroundColor Yellow }
Write-Host "unDolphin -> http://127.0.0.1:8790" -ForegroundColor Cyan
python app.py

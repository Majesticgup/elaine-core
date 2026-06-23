[CmdletBinding()]
param(
    [string]$Purpose = "future-controlled-setup",
    [string]$ReceiptPath = "receipts/guided-secret-entry-receipt.json",
    [switch]$NoReceipt
)

$ErrorActionPreference = "Stop"

function Read-ElaineChoice {
    param(
        [string]$Prompt,
        [string[]]$Allowed,
        [string]$Default
    )

    while ($true) {
        $value = Read-Host "$Prompt [$Default]"
        if ([string]::IsNullOrWhiteSpace($value)) {
            $value = $Default
        }
        $normalized = $value.Trim().ToLowerInvariant()
        if ($Allowed -contains $normalized) {
            return $normalized
        }
        Write-Host "Use one of: $($Allowed -join ', ')"
    }
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$packageRoot = Split-Path -Parent $scriptRoot

Write-Host "Elaine guided secret-entry helper"
Write-Host "Elaine Core v0.1 does not require secrets for the proof lab or Runtime Core checks."
Write-Host "This helper never prints, logs, commits, or persists the raw value."
Write-Host ""

$entryMode = Read-ElaineChoice `
    -Prompt "Do you use a password manager, prefer manual entry, or want to skip" `
    -Allowed @("password_manager", "manual", "skip") `
    -Default "skip"

$setupTarget = Read-ElaineChoice `
    -Prompt "Setup target" `
    -Allowed @("github_ssh", "github_token", "provider_api_key", "local_password", "other", "none") `
    -Default "none"

$persistence = Read-ElaineChoice `
    -Prompt "Persistence preference" `
    -Allowed @("session_only", "password_manager", "manual_owner_storage", "none") `
    -Default "none"

$secretReceived = $false
if ($entryMode -ne "skip") {
    Write-Host ""
    Write-Host "Paste or type the value only into this hidden local prompt."
    Write-Host "Do not paste it into chat, docs, GitHub issues, screenshots, or receipts."
    $secret = Read-Host "Secret value (hidden input)" -AsSecureString
    try {
        $secretReceived = $secret.Length -gt 0
    }
    finally {
        if ($null -ne $secret) {
            $secret.Dispose()
        }
    }
}

$receipt = [ordered]@{
    receipt_id = "guided-secret-entry-receipt"
    schema_version = "0.1.0"
    generated_utc = (Get-Date).ToUniversalTime().ToString("o")
    producer = [ordered]@{
        id = "Start-ElaineGuidedSecretPrompt.ps1"
        type = "local_prompt_helper"
    }
    status = "pass"
    purpose = $Purpose
    package = "elaine-core-v0.1"
    entry_mode = $entryMode
    setup_target = $setupTarget
    persistence_preference = $persistence
    secret_received_locally = $secretReceived
    raw_secret_printed = $false
    raw_secret_persisted = $false
    provider_call_used = $false
    hosted_retrieval_used = $false
    git_action_used = $false
    account_setting_changed = $false
    claim_boundary = "local redacted prompt receipt only; not authentication proof, not security validation, not production readiness"
}

if (-not $NoReceipt) {
    $resolvedReceipt = $ReceiptPath
    if (-not [System.IO.Path]::IsPathRooted($resolvedReceipt)) {
        $resolvedReceipt = Join-Path $packageRoot $resolvedReceipt
    }
    $receiptDir = Split-Path -Parent $resolvedReceipt
    New-Item -ItemType Directory -Force -Path $receiptDir | Out-Null
    $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $resolvedReceipt -Encoding UTF8
    Write-Host "Redacted receipt written: $resolvedReceipt"
}

Write-Host "Done. Raw secret value was not printed or persisted."

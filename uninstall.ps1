# GitHub Project Radar - Antigravity 全域技能解除安裝腳本 (PowerShell)
# 作用：從 Antigravity 全域技能目錄 (~/.gemini\config\skills\) 移除本技能

$ErrorActionPreference = "Stop"

$GlobalSkillsDir = Join-Path $HOME ".gemini\config\skills"
$TargetDir = Join-Path $GlobalSkillsDir "github-project-radar"

Write-Host "🗑️  正在從 Antigravity 全域技能目錄移除 GitHub Project Radar..." -ForegroundColor Yellow

if (Test-Path $TargetDir) {
    Remove-Item -Path $TargetDir -Recurse -Force
    Write-Host "✅ 已成功移除全域技能: $TargetDir" -ForegroundColor Green
} else {
    Write-Host "ℹ️  未發現已安裝的全域技能 ($TargetDir)，無需移除。" -ForegroundColor Gray
}

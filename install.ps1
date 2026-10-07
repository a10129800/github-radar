# GitHub Project Radar - Antigravity 全域技能安裝腳本 (PowerShell)
# 作用：將本技能連結或複製至 Antigravity 全域技能目錄 (~/.gemini/config/skills/)

$ErrorActionPreference = "Stop"

$SourceDir = $PSScriptRoot
$GlobalSkillsDir = Join-Path $HOME ".gemini\config\skills"
$TargetDir = Join-Path $GlobalSkillsDir "github-project-radar"

Write-Host "🚀 正在將 GitHub Project Radar 安裝至 Antigravity 全域技能目錄..." -ForegroundColor Cyan
Write-Host "來源目錄: $SourceDir"
Write-Host "目標目錄: $TargetDir"

if (-not (Test-Path $GlobalSkillsDir)) {
    New-Item -ItemType Directory -Path $GlobalSkillsDir -Force | Out-Null
}

# 若目標已存在，先備份或移除
if (Test-Path $TargetDir) {
    Write-Host "偵測到已存在的安裝，正在更新覆蓋..." -ForegroundColor Yellow
    Remove-Item -Path $TargetDir -Recurse -Force
}

# 建立目錄並複製檔案
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
Copy-Item -Path (Join-Path $SourceDir "SKILL.md") -Destination $TargetDir -Force
if (Test-Path (Join-Path $SourceDir "AGENTS.md")) {
    Copy-Item -Path (Join-Path $SourceDir "AGENTS.md") -Destination $TargetDir -Force
}
if (Test-Path (Join-Path $SourceDir ".env.example")) {
    Copy-Item -Path (Join-Path $SourceDir ".env.example") -Destination $TargetDir -Force
}
Copy-Item -Path (Join-Path $SourceDir "scripts") -Destination $TargetDir -Recurse -Force
Copy-Item -Path (Join-Path $SourceDir "references") -Destination $TargetDir -Recurse -Force

Write-Host "✅ 安裝完成！現在您可以在任何專案或對話中直接使用 github-project-radar 技能。" -ForegroundColor Green
Write-Host "測試指令: python `"$TargetDir\scripts\search_github.py`" --mode trending --limit 3" -ForegroundColor Gray

# GitHub Project Radar - Antigravity 全域技能安裝腳本 (PowerShell)
# 作用：將本技能連結或複製至 Antigravity 全域技能目錄 (~/.gemini/config/skills/)

$ErrorActionPreference = "Stop"

$SourceDir = $PSScriptRoot
$GlobalSkillsDir = Join-Path $HOME ".gemini\config\skills"
$TargetDir = Join-Path $GlobalSkillsDir "github-project-radar"

Write-Host "🚀 正在將 GitHub Project Radar 安裝至 Antigravity 全域技能目錄..." -ForegroundColor Cyan
Write-Host "來源目錄: $SourceDir"
Write-Host "目標目錄: $TargetDir"

# 建立目標目錄並複製技能檔案
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
@("SKILL.md", "AGENTS.md", ".env.example") | ForEach-Object {
    $src = Join-Path $SourceDir $_
    if (Test-Path $src) { Copy-Item -Path $src -Destination $TargetDir -Force }
}
Copy-Item -Path (Join-Path $SourceDir "scripts") -Destination $TargetDir -Recurse -Force
Copy-Item -Path (Join-Path $SourceDir "references") -Destination $TargetDir -Recurse -Force

Write-Host "✅ 安裝完成！現在您可以在任何專案或對話中直接使用 github-project-radar 技能。" -ForegroundColor Green
Write-Host "測試指令: python `"$TargetDir\scripts\search_github.py`" --mode trending --limit 3" -ForegroundColor Gray

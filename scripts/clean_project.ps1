# PowerShell Project Cleaner Helper
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$rootDir = Split-Path -Parent $PSScriptRoot

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   🧹 GitHub Project Radar - 專案多餘檔案一鍵清理" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$targets = @(
    "video_storyboard_script.html",
    "video_storyboard_script.md",
    "ponytail-4.12.0"
)

$cleanedCount = 0
foreach ($item in $targets) {
    $fullPath = Join-Path $rootDir $item
    if (Test-Path $fullPath) {
        try {
            Remove-Item -LiteralPath $fullPath -Recurse -Force -ErrorAction Stop
            Write-Host "  [✅ 已清理] $item" -ForegroundColor Green
            $cleanedCount++
        } catch {
            Write-Host "  [⚠️ 清理失敗] $item : $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "  [ℹ️ 已不存在] $item" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
if ($cleanedCount -gt 0) {
    Write-Host "  🎉 清理完成！共移除了 $cleanedCount 個多餘項目，專案已恢復乾淨俐落。" -ForegroundColor Green
} else {
    Write-Host "  ✨ 專案目錄目前非常整潔，沒有任何需要清理的暫存項目。" -ForegroundColor Green
}
Write-Host "========================================================" -ForegroundColor Cyan

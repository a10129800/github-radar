# PowerShell GitHub Push Helper
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   🚀 GitHub Project Radar - 一鍵推送到 GitHub" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 檢查 Git 是否安裝
try {
    $gitVer = git --version
    Write-Host "偵測到 Git: $gitVer" -ForegroundColor Gray
} catch {
    Write-Host "[❌ 錯誤] 系統未找到 Git 指令，請確認已安裝 Git 並加入 PATH 環境變數！" -ForegroundColor Red
    return
}

# 2. 初始化 Git 倉庫
if (-not (Test-Path ".git")) {
    Write-Host "[*] 正在初始化本地 Git 倉庫..." -ForegroundColor Yellow
    git init
}

# 3. 加入檔案與 Commit
Write-Host "[*] 正在加入檔案..." -ForegroundColor Yellow
git add .

Write-Host "[*] 正在建立 Commit..." -ForegroundColor Yellow
git commit -m "feat: initial release of github-project-radar"

# 4. 確保主分支名稱為 main
git branch -M main

# 5. 詢問遠端倉庫網址
Write-Host ""
Write-Host "請輸入您在 GitHub 建立的倉庫網址：" -ForegroundColor Green
Write-Host "（若您命名為 github-project-radar，可直接按 Enter 使用預設）" -ForegroundColor Gray
$defaultUrl = "https://github.com/a10129800/github-project-radar.git"
Write-Host "預設: $defaultUrl" -ForegroundColor DarkGray

$inputUrl = Read-Host "倉庫網址 [按 Enter 使用預設]"
$repoUrl = if ([string]::IsNullOrWhiteSpace($inputUrl)) { $defaultUrl } else { $inputUrl.Trim() }

# 6. 設定 remote
Write-Host "[*] 設定遠端倉庫網址: $repoUrl" -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin $repoUrl

# 7. 推送代碼
Write-Host "[*] 正在推送到 GitHub main 分支..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Green
    Write-Host "  ✅ 恭喜！專案已成功推送到 GitHub！" -ForegroundColor Green
    Write-Host "  專案網址: $repoUrl" -ForegroundColor Green
    Write-Host "========================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[⚠️ 推送未完成] 可能原因：" -ForegroundColor Yellow
    Write-Host "1. GitHub 上的遠端倉庫名稱與您輸入的網址不相符（請確認網址拼寫）。"
    Write-Host "2. 需要進行 GitHub 身分驗證（請依瀏覽器彈跳視窗登入授權）。"
    Write-Host "3. 若在 GitHub 建立時有勾選 Add README，請先執行: git pull origin main --rebase"
}

# 🚀 GitHub Project Radar (開源專案雷達)

> 為 AI Coding Agent（如 Google Antigravity）打造的高效開源專案雷達技能。支援 GitHub Trending 趨勢追蹤、即時新創項目過濾、限流診斷與四維度工程深度評估。

---

## ✨ 核心特點

- **零外部依賴**：核心腳本純以 Python 3 標準庫實現，開箱即用，免 `pip install`。
- **Windows UTF-8 防護**：內建終端編碼自動防護，避免繁中環境下輸出 Emoji 造成崩潰。
- **高自由度複合檢索 (P1)**：支援 `-q / --query` 自訂進階語句、`--pushed-days` 活躍度過濾、`--min-stars` 與 `--max-stars` 區間挖掘潛力新星。
- **Token 多源智慧尋標**：自動依序檢測 CLI 參數、環境變數、本地 `.env` 及 `~/.github_radar_token`，大幅簡化認證流程。
- **Rate Limit 智慧診斷**：GitHub API 遇到 403 限流時，自動解析重置時間並提供因應指引。
- **Trending 雙層容錯與自動備援**：網頁結構微調時具備 Regex 備援；網頁遭攔截時自動切換為 Search API 近期活躍專案探測。
- **工程級深度探測模式 (P2, `--info`)**：一鍵透視目錄樹結構、自動化健全度檢測（測試/文件/範例/CI/CD/Agent規格）、技術棧設定檔與核心依賴萃取，以及 README 摘錄。
- **全方位評估工作流**：規範四階段評估標準（痛點、架構、快速試用、成熟度與授權），輸出高品質結構化報告。

---

## 📂 目錄結構

```text
github-project-radar/
├── index.html               # 官方單頁網站 (整合新手指南、開發筆記與互動指令器)
├── SKILL.md                 # Antigravity 技能主說明與工作流引導
├── AGENTS.md                # 通用跨 Agent 規則規範 (Claude/Cursor/Windsurf 相容)
├── USER_GUIDE.md            # 小白超新手使用指南 (說人話免代碼說明書)
├── DEVELOPER_NOTES.md       # 業界開發筆記 (架構演進、設計哲學與踩坑復盤)
├── README.md                # 專案說明文件
├── LICENSE                  # MIT 開源授權條款
├── .env.example             # GitHub Token 配置範本
├── .gitignore               # 敏感憑證與快取忽略規則
├── install.ps1              # Windows PowerShell 全域安裝腳本
├── uninstall.ps1            # Windows PowerShell 全域解除安裝腳本
├── 一鍵推送到GitHub.bat     # Windows 雙擊極速推送腳本
├── scripts/
│   ├── search_github.py     # 零依賴核心探測與深探腳本 (支援自訂查詢、目錄樹、依賴透視與克隆指引)
│   └── push_github.ps1      # PowerShell GitHub 推送核心模組
├── tests/
│   └── test_radar.py        # 零依賴單元測試套件
└── references/
    └── search_syntax_cheatsheet.md # GitHub 高階搜尋語法手冊與 CLI 速查表
```

---

## ⚡ 快速開始

### 1. 安裝至 Antigravity 全域技能

在專案目錄下執行：
```powershell
.\install.ps1
```
安裝完成後，技能將註冊至 `~/.gemini/config/skills/github-project-radar`，在任何專案對話中皆可自動調用。

### 2. 命令列獨立使用

#### 搜尋最新發布的潛力新星（例：最近 14 天內新建且 Stars 介於 20~500 的 Agent 項目）
```bash
python scripts/search_github.py --topic "agent,llm" --days 14 --min-stars 20 --max-stars 500 --limit 10
```

#### 使用自訂高階語法與活躍度篩選（近 7 天內有代碼推送的 MCP 專案）
```bash
python scripts/search_github.py -q "mcp server" --pushed-days 7 --min-stars 30 --limit 10
```

#### 查看今日或本週 GitHub Trending 熱門榜
```bash
# 全語言今日榜
python scripts/search_github.py --mode trending --since daily --limit 10

# Python 本週榜
python scripts/search_github.py --mode trending --language python --since weekly --limit 10
```

#### 深度探測單一專案（透視目錄結構、測試/文件健全度、核心依賴與 README）
```bash
python scripts/search_github.py --info "DietrichGebert/ponytail"
```

#### 多專案橫向選型對比矩陣 (`--compare`)
```bash
python scripts/search_github.py --compare "crewAIInc/crewAI,run-llama/llama_index"
```

#### 一鍵匯出報告至本地檔案 (`-o / --output`)
```bash
python scripts/search_github.py --compare "fastapi/fastapi,tiangolo/sqlmodel" -o comparison.md
python scripts/search_github.py -q "mcp server" --days 30 --min-stars 15 -o radar_report.md
```

#### 輸出純 JSON 格式（供腳本或 Pipeline 接軌）
```bash
python scripts/search_github.py --keyword "mcp server" --days 30 --min-stars 15 --json
```

---

## 🔑 GitHub Token 設定（可選）

未帶 Token 時，GitHub 匿名 Search API 限制為每分鐘 10 次。若需高頻密集檢索，可透過以下任一方式設定（腳本會自動讀取）：

1. **同目錄 `.env` 檔案**：
   ```env
   GITHUB_TOKEN=ghp_your_personal_access_token
   ```
2. **家目錄配置**：在 `~/.github_radar_token` 或 `~/.github_token` 貼入 Token。
3. **環境變數**：
   * **PowerShell**: `$env:GITHUB_TOKEN = "ghp_..."`
   * **CMD**: `set GITHUB_TOKEN=ghp_...`
```cmd
set GITHUB_TOKEN=ghp_your_personal_access_token
```

或在指令中帶入 `--token <token>`。

---

## 📄 授權條款
MIT License

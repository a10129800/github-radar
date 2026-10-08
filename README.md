# 🚀 GitHub Project Radar (開源專案雷達)

> 為 AI Coding Agent（如 Google Antigravity）打造的高效開源專案雷達技能。支援 GitHub Trending 趨勢追蹤、即時新創項目過濾、限流診斷、四維度工程深度評估與技術選型對比。

[![Python Standard Library](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-0%20(Pure%20Stdlib)-success.svg)](scripts/search_github.py)
[![Ponytail](https://img.shields.io/badge/Architecture-Lean%20%2F%20Ponytail%204.12-orange.svg)](.agents/rules/ponytail.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

### 🌟 2026-10 最新工程升級：Ponytail 極簡瘦身重構

本專案已全面導入 **Ponytail 4.12.0 極簡主義開發標準**，透過嚴格的過度設計審查進行代碼瘦身，在**功能 100% 完整且零外部依賴**的前提下大幅收斂複雜度：

* 📉 **主腳本代碼精簡**：[`scripts/search_github.py`](scripts/search_github.py) 從 860 行縮減至 **770 行（淨減 90 行，-10.5%）**。
* 📉 **安裝腳本精簡**：[`install.ps1`](install.ps1) 從 38 行縮減至 **25 行（淨減 13 行，-34.2%）**。
* 🛡️ **維持 0 依賴**：100% 純 Python 標準函式庫，完全免 `pip install`，開箱即跑。
* 📄 **詳細工作報告與展示**：
  * 🌐 **[官方首頁 Web 版 (index.html)](index.html)** — 精美互動卡片、指令產生器與可展開報告全文
  * 📄 **[今日優化總結報告 (GitHub 線上直閱版)](daily_report_2026_10_08.md)** — GitHub 原生 Markdown 排版，點擊直接看
  * 🖨️ **[A4 / PDF 列印下載版 (HTML)](daily_report_2026_10_08.html)** — 支援 Ctrl+P 一鍵匯出正式工程彙報 PDF

---

## ✨ 核心特點

- **零外部依賴 (Zero Dependency)**：核心腳本純以 Python 3 標準庫實現，開箱即用，免 `pip install`，啟動極速。
- **極簡高效架構 (Lean Architecture)**：全專案融入 Ponytail 規範，杜絕多餘抽象層，單一 pass 完成熱門卡片爬蟲與結構透視。
- **Windows UTF-8 防護**：內建終端編碼自動安全防護，避免繁中環境下輸出 Emoji 造成編碼崩潰。
- **高自由度複合檢索 (P1)**：支援 `-q / --query` 自訂進階語句、`--pushed-days` 活躍度過濾、`--min-stars` 與 `--max-stars` 區間挖掘潛力新星。
- **Token 智慧尋標**：依序檢測 CLI 參數、系統環境變數與本地 `.env`，不寫多餘探測邏輯。
- **Rate Limit 智慧診斷**：GitHub API 遇到 403 限流時，自動解析重置時間並提供因應指引。
- **Trending 輕量擷取與自動備援**：單一高效率正規擷取函數；網頁遭攔截時自動無縫切換為 Search API 近期活躍專案探測。
- **工程級深度探測模式 (P2, `--info`)**：一鍵透視目錄樹結構、自動化健全度檢測（測試/文件/範例/CI/CD/Agent規格）、技術棧設定檔與核心依賴萃取，以及 README 摘錄。
- **跨專案技術選型對比 (`--compare`)**：支援橫向對比矩陣，一鍵產出多專案維護狀態、依賴與健康指標比較表。
- **內建極簡技能體系**：整合 Ponytail 6 項專案技能（`/ponytail`、`/ponytail-review`、`/ponytail-audit` 等），開發隨時防膨脹。

---

## 📂 目錄結構

```text
github-project-radar/
├── .agents/                 # Workspace Customizations 技能與規範
│   ├── rules/
│   │   └── ponytail.md      # 極簡工程師原則（YAGNI、標準庫優先）
│   └── skills/              # 專案內建 6 大 Ponytail 技能
│       ├── ponytail/        # /ponytail 極簡模式切換
│       ├── ponytail-audit/  # /ponytail-audit 全專案過度設計體檢
│       ├── ponytail-review/ # /ponytail-review 變更 Diff 審查
│       ├── ponytail-debt/   # /ponytail-debt 技術債追蹤
│       ├── ponytail-gain/   # /ponytail-gain 基準測試記分板
│       └── ponytail-help/   # /ponytail-help 模式指令速查
├── index.html               # 官方單頁網站 (整合新手指南、開發筆記與互動指令器)
├── daily_report_2026_10_08.md   # 📄 今日優化總結報告 (Markdown 線上直閱版)
├── daily_report_2026_10_08.html # 🖨️ 今日優化總結報告 (A4 / PDF 列印版)
├── SKILL.md                 # Antigravity 技能主說明與工作流引導
├── AGENTS.md                # 通用跨 Agent 規則規範 (Claude/Cursor/Windsurf 相容)
├── USER_GUIDE.md            # 小白超新手使用指南 (說人話免代碼說明書)
├── DEVELOPER_NOTES.md       # 業界開發筆記 (架構演進、設計哲學與踩坑復盤)
├── README.md                # 專案說明文件
├── LICENSE                  # MIT 開源授權條款
├── .env.example             # GitHub Token 配置範本
├── .gitignore               # 敏感憑證與快取忽略規則
├── install.ps1              # Windows PowerShell 全域安裝腳本 (精簡原生版)
├── uninstall.ps1            # Windows PowerShell 全域解除安裝腳本
├── 一鍵推送到GitHub.bat     # Windows 雙擊極速推送腳本
├── scripts/
│   ├── search_github.py     # 零依賴核心探測腳本 (經 Ponytail 瘦身重構)
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

## 🌿 極簡主義架構（Lean & Ponytail Architecture）

本專案奉行「最少代碼解決真實問題、零外部依賴、拒绝無謂抽象」的工程哲學。

### 📊 瘦身重構具體成效表

| 模組 / 功能 | 重構前 | 重構後 | 效益 |
| :--- | :--- | :--- | :---: |
| **Trending 爬蟲** | 87 行狀態機解析器與正則備援重複並存 | 合併為單一輕量 `parse_trending_html` 函數 | **-52 行** |
| **Token 讀取** | 搜尋四處目錄並翻找家目錄冷門隱藏檔 | 僅保留標準 CLI、環境變數與同層 `.env` | **-18 行** |
| **對比矩陣生成** | 內部巢狀定義多個閉包小函數 | 採用線性元組對照迭代與三元表達式 | **-12 行** |
| **JSON 字典投影** | 手動 `for` 迴圈逐筆 `append` 11 個欄位 | 採用清單推導式搭配白名單解包映射 | **-8 行** |
| **UTF-8 安全防護** | 雙重 try-except 巢狀屬性檢查 | 走訪輸出串流統一安全 `reconfigure` | **-6 行** |
| **PowerShell 安裝** | 手動判斷目錄、手動刪除再新增 | 活用原生 `Copy-Item -Force` 直接覆蓋 | **-13 行** |

### 🛠️ 內建 Ponytail 技能呼叫方式

在支援 Agent（如 Google Antigravity、Claude Code、Cursor 等）中直接輸入以下指令即可觸發：
* `/ponytail` 或 `/ponytail lite` / `/ponytail ultra`：開啟極簡開發模式（依階梯原則強制最少變更與標準庫優先）。
* `/ponytail-review`：專門針對變更 Diff 進行過度設計專項 Code Review。
* `/ponytail-audit`：掃描整份專案並列出可精簡或刪除的代碼清單。
* `/ponytail-debt`：收集專案中的 `ponytail:` 技術債與簡化標記。
* `/ponytail-help`：查看模式與指令速查表。

---

## 🔑 GitHub Token 設定（可選）

未帶 Token 時，GitHub 匿名 Search API 限制為每分鐘 10 次。若需高頻密集檢索，可透過以下任一方式設定（腳本會自動讀取）：

1. **同目錄 `.env` 檔案**：
   ```env
   GITHUB_TOKEN=ghp_your_personal_access_token
   ```
2. **環境變數**：
   * **PowerShell**: `$env:GITHUB_TOKEN = "ghp_your_personal_access_token"`
   * **CMD**: `set GITHUB_TOKEN=ghp_your_personal_access_token`
   * **Bash/Linux/macOS**: `export GITHUB_TOKEN="ghp_your_personal_access_token"`
3. **指令參數**：
   在執行時直接帶入 `--token ghp_...`。

---

## 📄 授權條款
MIT License

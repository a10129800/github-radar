# GitHub Search 語法與雷達實戰 Cheatsheet

本文件整理搜尋 GitHub 最新、爆紅與前沿開源專案的高階語法指南，並提供與 `search_github.py` 指令的一對一速查表。

---

## 1. 核心搜尋維度與原生語法

| 搜尋維度 | 語法範例 | 說明 |
| :--- | :--- | :--- |
| **建立時間 (Created)** | `created:>2026-03-01` | 搜尋指定日期之後新建的 Repo |
| **最近推送 (Pushed)** | `pushed:>2026-03-25` | 排除已荒廢專案，鎖定近期活躍維護中專案 |
| **星星門檻 (Stars)** | `stars:>=50` 或 `stars:10..500` | 鎖定起步期但已獲關注的潛力新星（區間篩選） |
| **主題標籤 (Topic)** | `topic:agent topic:llm` | 符合 GitHub Topics 標籤（精準分類） |
| **程式語言 (Language)** | `language:python language:rust` | 限定主語言 |
| **搜尋欄位 (In)** | `in:name,description "mcp server"` | 限定關鍵字出現在名稱或描述中 |
| **授權協議 (License)** | `license:mit license:apache-2.0` | 商業友好開源協議 |
| **分支數 (Forks)** | `forks:>=10` | 具備衍生社群活力的項目 |

---

## 2. 實戰場景與 `search_github.py` 指令速查

### 場景 A：探索最近 14 天內新建且快速累積人氣的潛力新星（AI Agent）
* **需求**：排除幾萬星的老牌項目，聚焦 20~500 星起步新項目。
* **CLI 指令**：
  ```bash
  python scripts/search_github.py --topic "agent,llm" --days 14 --min-stars 20 --max-stars 500 --limit 10
  ```

### 場景 B：探索最近 7 天內有積極提交代碼的 MCP (Model Context Protocol) 專案
* **需求**：使用自由 Query 與 Pushed 活躍度過濾。
* **CLI 指令**：
  ```bash
  python scripts/search_github.py -q "mcp server" --pushed-days 7 --min-stars 25 --limit 10
  ```

### 場景 C：探索最近 30 天內發布的 Rust 系統工具 / CLI
* **需求**：指定語言與主題。
* **CLI 指令**：
  ```bash
  python scripts/search_github.py --language rust --topic cli --days 30 --min-stars 50 --limit 10
  ```

### 場景 D：單一專案深度透視（目錄樹、測試/文件健全度、核心依賴與快速克隆）
* **需求**：在 clone 前一眼看穿專案工程實力與代碼架構。
* **CLI 指令**：
  ```bash
  python scripts/search_github.py --info "DietrichGebert/ponytail"
  ```

### 場景 E：追蹤本日 / 本週 GitHub Trending 趨勢
* **全語言今日榜**：
  ```bash
  python scripts/search_github.py --mode trending --since daily --limit 10
  ```
* **Python 本週榜**：
  ```bash
  python scripts/search_github.py --mode trending --language python --since weekly --limit 10
  ```

### 場景 F：多專案技術選型對比矩陣 (Comparison Matrix)
* **需求**：橫向評估多個競品專案之 Stars、更新活躍度、測試/文件健全度與核心依賴。
* **CLI 指令**：
  ```bash
  python scripts/search_github.py --compare "crewAIInc/crewAI,run-llama/llama_index"
  ```

### 場景 G：一鍵匯出調研報告至檔案 (`-o`)
* **需求**：將對比矩陣或搜尋結果保存為 Markdown 或 JSON 檔案，供技術文檔留存。
* **CLI 指令**：
  ```bash
  python scripts/search_github.py --compare "fastapi/fastapi,tiangolo/sqlmodel" -o report.md
  python scripts/search_github.py -q "mcp server" --limit 10 -o mcp_radar.md
  ```

---

## 3. GitHub Trending 網址速查

* **今日熱榜（全部語言）**：`https://github.com/trending?since=daily`
* **本週熱榜（指定語言）**：
  * Python: `https://github.com/trending/python?since=weekly`
  * TypeScript: `https://github.com/trending/typescript?since=weekly`
  * Rust: `https://github.com/trending/rust?since=weekly`
  * Go: `https://github.com/trending/go?since=weekly`

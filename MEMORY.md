# 🧠 專案開發與對話記憶 (Project Memory Log)

**記錄日期**: 2026-10-07  
**核心主題**: GitHub Project Radar 專案打磨、小白化首頁改造與全方位交付紀錄

---

## 📌 核心共識與理念（用戶喜好）
1. **拒絕自嗨與艱澀術語**：
   - 訪客與非程式背景使用者無法理解「JSON Schema / urllib / CP950 / state machine」等詞彙。
   - 產品頁面必須直擊「**痛點與好處**」：手動搜尋痛點 vs 雷達優勢（痛點對比表）。
   - 核心特色必須用具體生動的比喻：「**淘金黑馬模式**（20~500 星挖寶）」、「**工程照妖鏡**（免下載 0.8s 避開空殼專案）」、「**PK 決鬥擂台**（雙專案橫向對比）」、「**AI 隨身外掛**（自然語言零門檻）」。
2. **零依賴與極致體驗**：
   - 前端網頁純原生 HTML/CSS/JS，不引入任何 npm/webpack 構建工具，隨開即用，可部署至 GitHub Pages。
   - Python 後端維持標準庫零外部依賴，支援跨平台編碼（UTF-8 & Windows CP950/GBK 容錯）。
   - 提供 Windows 使用者一鍵操作腳本（`.bat` 封裝 PowerShell，避開 Windows CMD 的編碼跳脫字元坑）。

---

## 🛠️ 今日主要交付里程碑

### 1. 核心腳本能力完備 (`scripts/search_github.py`)
- **P1 搜尋核心**：
  - 支援關鍵字搜尋 (`-q`)、最近推送時間過濾 (`--pushed-days`)、星數區間 (`--min-stars`, `--max-stars`)、開源授權篩選 (`--license`)。
  - 整合 GitHub Trending（每日/每週熱門探索）。
  - 自動 Token 探測（`--token` -> 環變 -> `.env` -> `~/.github_radar_token`）。
- **P2 深度探測與橫向比較**：
  - `--info "owner/repo"`：透過 GitHub Contents API 探測專案一級目錄結構、健康度清單（`tests/`, `docs/`, `examples/`, `.github/`, `AGENTS.md`）及技術棧依賴（`package.json`, `Cargo.toml`, `pyproject.toml`, `requirements.txt`, `go.mod`）。
  - `--compare "repoA,repoB"`：自動生成 Markdown 橫向技術選型對比表。
  - `-o / --output`：支援導出 Markdown 或 JSON 檔案。

### 2. 完整文檔與規範體系
- [USER_GUIDE.md](file:///e:/IDE資料/github-project-radar/USER_GUIDE.md)：針對完全不懂程式的小白寫的白話使用手冊。
- [DEVELOPER_NOTES.md](file:///e:/IDE資料/github-project-radar/DEVELOPER_NOTES.md)：業界架構開發筆記，詳解架構設計、踩坑歷程（API Rate Limit、Windows 編碼、無依賴原則）與未來演進。
- [AGENTS.md](file:///e:/IDE資料/github-project-radar/AGENTS.md)：跨 AI 助手標準調用協議（Claude Code, Cursor, Windsurf, Antigravity）。
- [SKILL.md](file:///e:/IDE資料/github-project-radar/SKILL.md)：Agent Skill 標準定義。
- [references/search_syntax_cheatsheet.md](file:///e:/IDE資料/github-project-radar/references/search_syntax_cheatsheet.md)：GitHub 進階搜尋語法速查表。

### 3. 發布與安裝工具鏈
- `一鍵推送到GitHub.bat`：Windows 雙擊即執行的推送腳本，自動調用 `scripts/push_github.ps1`。
- `install.ps1` / `uninstall.ps1`：一鍵安裝為 Antigravity 全域 Skill。
- `tests/test_radar.py`：單元測試套件。

### 4. 產品主頁大改造 (`index.html`)
- **受眾視角翻新**：徹底摒棄技術自嗨，採用暗黑霓虹科技視覺與雷達掃描動畫。
- **痛點對比表**：清晰展示「痛苦的手動搜尋」vs「使用 Radar」。
- **四大超能力展區**：淘金模式、工程照妖鏡、PK 擂台、AI 外掛。
- **即時模擬預覽**：直觀呈現照妖鏡健康檢查卡與 PK 對比表格。
- **三步上手指南 + 指令產生器**：小白照著做 30 秒能上手，支援一鍵複製指令。
- **折疊式技術深水區**：供高階工程師查閱架構設計與踩坑記錄，不干擾小白閱覽體驗。

---

## 🧭 未來維護與推廣建議
1. 若需推送到 GitHub，可直接雙擊執行根目錄的 `一鍵推送到GitHub.bat`。
2. 倉庫可直接在 GitHub Repository Settings 啟用 GitHub Pages（選擇 `main` 分支根目錄 `/`），即可直接對外展示 `index.html`。
3. `ponytail-4.12.0` 目前已加入 `.gitignore`，後續可視情況整理至 `samples/` 或刪除。

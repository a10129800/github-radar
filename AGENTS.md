# 🚀 AGENTS.md — GitHub Project Radar

> Universal Agent instructions for discovering, filtering, and evaluating open-source GitHub repositories.
> Works with Claude Code, Cursor, Windsurf, Google Antigravity, Codex, Devin, and any AI coding assistant.

---

## 🎯 When to Use This Skill
Activate this workflow when the user asks to:
- Find latest or trending GitHub projects in any domain (e.g., AI agents, RAG, MCP servers, Rust CLI, Next.js).
- Spot hidden gems or newborn repositories (`stars:20..500`, created recently).
- Track GitHub Trending (daily/weekly) across languages.
- Deeply inspect, benchmark, or evaluate an open-source repository before cloning.

---

## 🛠️ Tool Execution

The repository includes a zero-dependency Python 3 standard library script: `scripts/search_github.py`.

### 1. Discover Newborn or Active Repositories
```bash
# Discover projects created in the last 14 days with 20~500 stars (hidden gems)
python scripts/search_github.py --topic "agent,llm" --days 14 --min-stars 20 --max-stars 500 --limit 10

# Search recently active projects with custom query and pushed cutoff
python scripts/search_github.py -q "mcp server" --pushed-days 7 --min-stars 30 --limit 10
```

### 2. Track GitHub Trending Repositories
```bash
# Daily overall trending
python scripts/search_github.py --mode trending --since daily --limit 10

# Weekly trending for Python / Rust / TypeScript
python scripts/search_github.py --mode trending --language python --since weekly --limit 10
```

### 3. Deep-Dive Inspection (`--info`)
Run this before recommending any repo to get top-level directory layout, health checklist, core tech stack manifests, and README excerpt:
```bash
python scripts/search_github.py --info "owner/repo"
```

### 4. Cross-Project Comparison Matrix (`--compare`)
Compare multiple repositories side-by-side for tech stack selection:
```bash
python scripts/search_github.py --compare "crewAIInc/crewAI,run-llama/llama_index"
```

### 5. Export Reports to Local Files (`-o`)
```bash
python scripts/search_github.py --compare "fastapi/fastapi,tiangolo/sqlmodel" -o comparison.md
python scripts/search_github.py -q "mcp server" --days 30 --min-stars 15 --json -o results.json
```

---

## 📋 Evaluation Guidelines (The 4 Pillars)
When reporting repositories to the user, always provide concrete technical analysis:
1. **Core Problem & Value**: What exact problem does it solve that existing solutions (e.g. LangChain, vLLM) do not?
2. **Architecture & Health**: Inspect directory structure (`tests/`, `docs/`, `examples/`), CI/CD, and core dependencies. Distinguish between toy concepts/PoCs and production-ready codebases.
3. **Quick Start**: Provide 1~3 executable lines (`git clone --depth 1`, `uv run`, `docker compose up`).
4. **License & Maturity**: Check license compatibility (MIT, Apache-2.0) and whether it is archived or a fork.

---

## 🔑 Authentication Note
Anonymous GitHub API allows 10 search requests per minute. To increase to 30+ req/min, store your Personal Access Token in `.env` as `GITHUB_TOKEN=ghp_...` or set the `GITHUB_TOKEN` environment variable. The script auto-discovers it.

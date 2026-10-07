#!/usr/bin/env python3
"""
GitHub Project Radar & Trending Repositories Helper Script.
Zero-dependency script (pure Python standard library) to search latest
or trending GitHub repositories with robust error handling, rate-limit
diagnostics, fallback mechanisms, directory structure tree inspection,
manifest dependencies analysis, and deep-dive inspection.
"""

import sys
import os
import json
import argparse
import datetime
import base64
import urllib.request
import urllib.parse
import urllib.error
import re
import time
from html.parser import HTMLParser

# 1. Windows Terminal UTF-8 Safety (Prevents CP950 / charmap UnicodeEncodeError)
if sys.platform.startswith("win"):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def resolve_token(token=None):
    """
    Resolve GitHub token from multiple sources in priority order:
    1. CLI argument `--token`
    2. Environment variable `GITHUB_TOKEN`
    3. Local `.env` file (current working directory or script directory)
    4. User home config file (~/.github_radar_token or ~/.github_token)
    """
    if token:
        return token.strip()

    # 1. Environment variable
    env_token = os.environ.get("GITHUB_TOKEN")
    if env_token:
        return env_token.strip()

    # 2. Check .env files in CWD and script folder
    search_dirs = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))]
    for d in search_dirs:
        env_path = os.path.join(d, ".env")
        if os.path.isfile(env_path):
            try:
                with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GITHUB_TOKEN="):
                            val = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if val:
                                return val
            except Exception:
                pass

    # 3. Check user home config files
    home = os.path.expanduser("~")
    for fname in [".github_radar_token", ".github_token"]:
        token_path = os.path.join(home, fname)
        if os.path.isfile(token_path):
            try:
                with open(token_path, "r", encoding="utf-8", errors="ignore") as f:
                    val = f.read().strip()
                    if val:
                        return val
            except Exception:
                pass

    return None


def get_headers(token=None):
    headers = {
        "User-Agent": "GitHub-Project-Radar/1.3 (Agentic-Tool)",
        "Accept": "application/vnd.github.v3+json"
    }
    api_token = resolve_token(token)
    if api_token:
        headers["Authorization"] = f"token {api_token}"
    return headers


def execute_request_with_retry(req, timeout=15, retries=1):
    """Execute a urllib request with 1 retry on timeout or network glitches."""
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                headers = dict(resp.headers)
                body = resp.read().decode("utf-8", errors="ignore")
                return resp.status, headers, body
        except urllib.error.HTTPError as e:
            # Return HTTP status and response headers directly
            headers = dict(e.headers)
            body = e.read().decode("utf-8", errors="ignore")
            return e.code, headers, body
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(1.0)
                continue
            raise last_err


def handle_rate_limit(status_code, headers, body=""):
    """Diagnose rate limit issues and output user-friendly warnings."""
    if status_code in (403, 429):
        reset_epoch = headers.get("x-ratelimit-reset")
        reset_info = ""
        if reset_epoch:
            try:
                reset_dt = datetime.datetime.fromtimestamp(int(reset_epoch))
                now = datetime.datetime.now()
                diff_sec = max(0, int((reset_dt - now).total_seconds()))
                reset_info = f"（限額約在 {diff_sec} 秒後重置）"
            except Exception:
                pass

        sys.stderr.write(
            f"\n[⚠️ 速率限制告警] GitHub API 請求已達限額！{reset_info}\n"
            f"  - 未帶 Token 之 Search API 限制為每分鐘 10 次。\n"
            f"  - 建議方案 1：建立 .env 檔案填寫 GITHUB_TOKEN=ghp_...，或使用 --token <PAT> 參數，享有 30次/分 以上配額。\n"
            f"  - 建議方案 2：若無 Token，請稍候重試，或使用 Web Search 工具進行替代檢索。\n\n"
        )


def search_github_api(query, sort="stars", order="desc", per_page=10, token=None):
    """Search repositories using GitHub Search API with rate-limit protection."""
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": min(per_page, 100)
    }
    url = f"https://api.github.com/search/repositories?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=get_headers(token))

    try:
        status, headers, body = execute_request_with_retry(req, timeout=15)
        if status == 200:
            data = json.loads(body)
            return data.get("items", [])
        else:
            handle_rate_limit(status, headers, body)
            if status not in (403, 429):
                sys.stderr.write(f"[Error] GitHub API 請求失敗 ({status}): {body[:180]}\n")
            return []
    except Exception as e:
        sys.stderr.write(f"[Error] 網路連線錯誤: {e}\n")
        return []


def parse_manifest_dependencies(manifest_name, raw_content):
    """Safely parse core dependencies from key project manifest files."""
    deps = []
    try:
        if manifest_name == "package.json":
            pkg = json.loads(raw_content)
            prod_deps = list((pkg.get("dependencies") or {}).keys())
            if prod_deps:
                deps.extend(prod_deps[:8])
            dev_deps = list((pkg.get("devDependencies") or {}).keys())
            if dev_deps and len(deps) < 8:
                deps.extend([f"{d} (dev)" for d in dev_deps[:4]])

        elif manifest_name in ("pyproject.toml", "requirements.txt"):
            for line in raw_content.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("["):
                    continue
                # Simple package name extraction
                match = re.match(r"^([a-zA-Z0-9_\-\.]+)", line)
                if match:
                    pkg = match.group(1).lower()
                    if pkg not in ("python", "setuptools", "wheel") and pkg not in deps:
                        deps.append(pkg)
                if len(deps) >= 8:
                    break

        elif manifest_name == "Cargo.toml":
            in_deps = False
            for line in raw_content.splitlines():
                line = line.strip()
                if line.startswith("[dependencies"):
                    in_deps = True
                    continue
                elif line.startswith("[") and in_deps:
                    break
                if in_deps and "=" in line and not line.startswith("#"):
                    crate = line.split("=")[0].strip()
                    if crate and crate not in deps:
                        deps.append(crate)
                if len(deps) >= 8:
                    break

        elif manifest_name == "go.mod":
            in_require = False
            for line in raw_content.splitlines():
                line = line.strip()
                if line.startswith("require ("):
                    in_require = True
                    continue
                elif in_require and line.startswith(")"):
                    break
                if in_require and line and not line.startswith("//"):
                    mod = line.split()[0].strip()
                    if mod:
                        deps.append(mod.split("/")[-1])
                elif line.startswith("require ") and not line.startswith("require ("):
                    parts = line.split()
                    if len(parts) >= 2:
                        deps.append(parts[1].split("/")[-1])
                if len(deps) >= 8:
                    break
    except Exception:
        pass
    return deps


def fetch_repo_structure_and_tech_stack(clean_repo, headers):
    """
    Fetch top-level repository contents to assess engineering health,
    directory layout, and core tech stack manifests.
    """
    contents_url = f"https://api.github.com/repos/{clean_repo}/contents"
    structure_info = {
        "dirs": [],
        "manifest_files": [],
        "agent_configs": [],
        "health_checklist": {
            "has_tests": False,
            "has_docs": False,
            "has_examples": False,
            "has_ci_cd": False
        },
        "detected_stack": [],
        "core_dependencies": []
    }

    try:
        req = urllib.request.Request(contents_url, headers=headers)
        status, _, body = execute_request_with_retry(req, timeout=10)
        if status == 200:
            items = json.loads(body)
            dirs = []
            files = []
            primary_manifest = None

            for it in items:
                name = it.get("name", "")
                itype = it.get("type", "")
                if itype == "dir":
                    dirs.append(name)
                    lower = name.lower()
                    if lower in ("test", "tests", "spec", "testing"):
                        structure_info["health_checklist"]["has_tests"] = True
                    elif lower in ("doc", "docs", "documentation"):
                        structure_info["health_checklist"]["has_docs"] = True
                    elif lower in ("example", "examples", "demo", "samples"):
                        structure_info["health_checklist"]["has_examples"] = True
                    elif lower == ".github":
                        structure_info["health_checklist"]["has_ci_cd"] = True
                elif itype == "file":
                    files.append(name)
                    lower = name.lower()
                    # Check manifests
                    if lower in ("package.json", "pyproject.toml", "requirements.txt", "cargo.toml", "go.mod", "pom.xml", "dockerfile"):
                        structure_info["manifest_files"].append(name)
                        if not primary_manifest and lower in ("package.json", "pyproject.toml", "cargo.toml", "requirements.txt", "go.mod"):
                            primary_manifest = it
                    # Check agent configs
                    if lower in ("skill.md", "agents.md", "claude.md", ".cursorrules", "plugin.json"):
                        structure_info["agent_configs"].append(name)

            structure_info["dirs"] = sorted(dirs)

            # Peek into the primary manifest to extract dependencies snippet
            if primary_manifest:
                manifest_name = primary_manifest.get("name", "")
                manifest_url = primary_manifest.get("url", "")
                if manifest_url:
                    try:
                        m_req = urllib.request.Request(manifest_url, headers=headers)
                        m_status, _, m_body = execute_request_with_retry(m_req, timeout=8)
                        if m_status == 200:
                            m_data = json.loads(m_body)
                            m_content = base64.b64decode(m_data.get("content", "")).decode("utf-8", errors="ignore")
                            deps = parse_manifest_dependencies(manifest_name, m_content)
                            if deps:
                                structure_info["core_dependencies"] = deps
                                structure_info["detected_stack"].append(f"{manifest_name}")
                    except Exception:
                        pass
    except Exception:
        pass

    return structure_info


def fetch_repo_info(owner_repo, token=None):
    """Deep-dive into a single repo: metadata, release, structure tree, tech stack, and README."""
    clean_repo = owner_repo.strip().strip("/")
    if "/" not in clean_repo:
        sys.stderr.write(f"[Error] Repo 格式應為 'owner/repo'，例如: 'facebook/react'\n")
        return None

    headers = get_headers(token)
    repo_url = f"https://api.github.com/repos/{clean_repo}"
    readme_url = f"https://api.github.com/repos/{clean_repo}/readme"
    release_url = f"https://api.github.com/repos/{clean_repo}/releases/latest"

    result = {
        "full_name": clean_repo,
        "html_url": f"https://github.com/{clean_repo}",
        "description": "",
        "stars": 0,
        "forks": 0,
        "open_issues": 0,
        "subscribers_count": 0,
        "license": "N/A",
        "language": "N/A",
        "created_at": "",
        "updated_at": "",
        "pushed_at": "",
        "archived": False,
        "is_fork": False,
        "default_branch": "main",
        "topics": [],
        "latest_release": None,
        "readme_snippet": "",
        "structure": {}
    }

    # 1. Repo Metadata
    try:
        req = urllib.request.Request(repo_url, headers=headers)
        status, resp_headers, body = execute_request_with_retry(req, timeout=12)
        if status == 200:
            data = json.loads(body)
            result["description"] = data.get("description") or "無描述"
            result["stars"] = data.get("stargazers_count", 0)
            result["forks"] = data.get("forks_count", 0)
            result["open_issues"] = data.get("open_issues_count", 0)
            result["subscribers_count"] = data.get("subscribers_count", 0)
            result["license"] = (data.get("license") or {}).get("spdx_id") or "N/A"
            result["language"] = data.get("language") or "N/A"
            result["created_at"] = (data.get("created_at") or "")[:10]
            result["updated_at"] = (data.get("updated_at") or "")[:10]
            result["pushed_at"] = (data.get("pushed_at") or "")[:10]
            result["archived"] = data.get("archived", False)
            result["is_fork"] = data.get("fork", False)
            result["default_branch"] = data.get("default_branch", "main")
            result["topics"] = data.get("topics", [])
        else:
            handle_rate_limit(status, resp_headers, body)
            sys.stderr.write(f"[Error] 無法獲取 Repo 資訊 ({status})\n")
            return None
    except Exception as e:
        sys.stderr.write(f"[Error] 獲取 Repo 失敗: {e}\n")
        return None

    # 2. Latest Release (Optional)
    try:
        req = urllib.request.Request(release_url, headers=headers)
        status, _, body = execute_request_with_retry(req, timeout=8)
        if status == 200:
            rel = json.loads(body)
            result["latest_release"] = {
                "tag_name": rel.get("tag_name"),
                "name": rel.get("name") or rel.get("tag_name"),
                "published_at": (rel.get("published_at") or "")[:10],
                "body_summary": (rel.get("body") or "").strip()[:300].replace("\r", "")
            }
    except Exception:
        pass

    # 3. Readme Snippet (Optional)
    try:
        req = urllib.request.Request(readme_url, headers=headers)
        status, _, body = execute_request_with_retry(req, timeout=10)
        if status == 200:
            readme_data = json.loads(body)
            encoded = readme_data.get("content", "")
            if encoded:
                raw_readme = base64.b64decode(encoded).decode("utf-8", errors="ignore")
                clean_lines = []
                for line in raw_readme.splitlines():
                    stripped = line.strip()
                    # Filter out noise badges and raw images
                    if stripped.startswith("[![") or stripped.startswith("<img") or stripped.startswith("<p align"):
                        continue
                    clean_lines.append(line)
                clean_text = "\n".join(clean_lines).strip()
                result["readme_snippet"] = clean_text[:1200]
    except Exception:
        pass

    # 4. Top-level Structure & Tech Stack Inspection
    result["structure"] = fetch_repo_structure_and_tech_stack(clean_repo, headers)

    return result


class TrendingHTMLParser(HTMLParser):
    """Robust lightweight parser to extract repos from github.com/trending."""
    def __init__(self):
        super().__init__()
        self.repos = []
        self.current_repo = {}
        self.in_article = False
        self.in_h2 = False
        self.in_desc = False
        self.in_lang = False
        self.depth_in_article = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "").split()

        if tag == "article" or (tag in ("div", "li") and any("Box-row" in c for c in classes)):
            self.in_article = True
            self.depth_in_article = 1
            self.current_repo = {"stars_today": "", "description": "", "language": "", "stars": "", "forks": ""}
        elif self.in_article:
            self.depth_in_article += 1

        if self.in_article:
            if tag in ("h1", "h2", "h3"):
                self.in_h2 = True
            elif tag == "a" and self.in_h2:
                href = attr_dict.get("href", "").strip()
                parts = [p for p in href.strip("/").split("/") if p]
                if len(parts) == 2 and not self.current_repo.get("full_name"):
                    repo_path = f"{parts[0]}/{parts[1]}"
                    self.current_repo["full_name"] = repo_path
                    self.current_repo["url"] = f"https://github.com/{repo_path}"
            elif tag in ("p", "div") and (any("col-9" in c for c in classes) or "description" in attr_dict.get("class", "")):
                self.in_desc = True
            elif tag == "span" and attr_dict.get("itemprop") == "programmingLanguage":
                self.in_lang = True

    def handle_endtag(self, tag):
        if self.in_article:
            self.depth_in_article -= 1
            if tag in ("h1", "h2", "h3"):
                self.in_h2 = False
            elif tag in ("p", "div") and self.in_desc:
                self.in_desc = False
            elif tag == "span" and self.in_lang:
                self.in_lang = False

            if tag == "article" or self.depth_in_article <= 0:
                self.in_article = False
                if self.current_repo.get("full_name"):
                    self.repos.append(self.current_repo)
                self.current_repo = {}

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_desc:
            prev = self.current_repo.get("description", "")
            self.current_repo["description"] = (prev + " " + text).strip()
        elif self.in_lang:
            self.current_repo["language"] = text
        elif any(k in text.lower() for k in ("stars today", "stars this week", "stars this month")):
            self.current_repo["stars_today"] = text


def regex_fallback_trending(html):
    """Regex fallback to extract repos if HTML structure changes."""
    repos = []
    pattern = re.compile(r'<h[12][^>]*>\s*<a[^>]*href=["\']/([a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+)["\']', re.IGNORECASE)
    matches = pattern.findall(html)
    seen = set()
    for repo_path in matches:
        if repo_path in seen or "/" not in repo_path:
            continue
        seen.add(repo_path)
        repos.append({
            "full_name": repo_path,
            "url": f"https://github.com/{repo_path}",
            "description": "Trending 開源專案",
            "language": "N/A",
            "stars_today": "Trending"
        })
    return repos


def fetch_trending(language="", since="daily", token=None, limit=10):
    """Fetch repos from GitHub Trending page with multi-tier fallback."""
    lang_path = f"/{language}" if language else ""
    url = f"https://github.com/trending{lang_path}?since={since}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    })

    try:
        status, _, html = execute_request_with_retry(req, timeout=12)
        if status == 200:
            parser = TrendingHTMLParser()
            parser.feed(html)
            repos = parser.repos
            if not repos:
                repos = regex_fallback_trending(html)
            if repos:
                return repos
    except Exception as e:
        sys.stderr.write(f"[Warning] Trending 頁面連線異常 ({e})，正在切換 API 備援探索...\n")

    # API Fallback: Explore recently pushed repos with high stars
    sys.stderr.write(f"[Info] 啟動備援機制：透過 Search API 搜尋近期活躍熱門專案...\n")
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    q_parts = [f"pushed:>{cutoff}", "stars:>100"]
    if language:
        q_parts.append(f"language:{language}")
    query = " ".join(q_parts)
    api_items = search_github_api(query=query, sort="stars", order="desc", per_page=limit, token=token)

    fallback_repos = []
    for it in api_items:
        fallback_repos.append({
            "full_name": it.get("full_name"),
            "url": it.get("html_url"),
            "description": it.get("description") or "無描述",
            "language": it.get("language") or "N/A",
            "stars_today": f"⭐ {it.get('stargazers_count', 0):,}"
        })
    return fallback_repos


def format_markdown(repos, is_api=True):
    """Format repository list as a rich markdown report."""
    if not repos:
        return (
            "⚠️ 未找到符合條件的開源專案。\n"
            "💡 建議調降 --min-stars 門檻、放寬 --days / --pushed-days 區間，或簡化 --keyword / -q 查詢條件後重試。"
        )

    lines = []
    lines.append("| 專案名稱 | 主語言 | Stars / 趨勢 | 簡介與特色 | 連結 |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")

    for r in repos:
        if is_api:
            name = r.get("full_name", "")
            url = r.get("html_url", "")
            lang = r.get("language") or "N/A"
            stars = f"⭐ {r.get('stargazers_count', 0):,}"
            desc = (r.get("description") or "無描述").replace("|", "\\|").replace("\n", " ")
            if len(desc) > 80:
                desc = desc[:77] + "..."
            lines.append(f"| **{name}** | `{lang}` | {stars} | {desc} | [GitHub Repo]({url}) |")
        else:
            name = r.get("full_name", "")
            url = r.get("url", "")
            lang = r.get("language") or "N/A"
            trend = r.get("stars_today") or "Trending"
            desc = (r.get("description") or "無描述").replace("|", "\\|").replace("\n", " ")
            if len(desc) > 80:
                desc = desc[:77] + "..."
            lines.append(f"| **{name}** | `{lang}` | 🚀 {trend} | {desc} | [GitHub Repo]({url}) |")

    return "\n".join(lines)


def format_repo_detail_markdown(detail):
    """Format single repo deep dive information into an engineering-grade report."""
    if not detail:
        return "⚠️ 未能取得該專案詳細資訊。"

    topics_str = " ".join([f"`#{t}`" for t in detail.get("topics", [])]) or "無標籤"
    rel = detail.get("latest_release")
    rel_str = f"`{rel['tag_name']}` ({rel['published_at']})" if rel else "尚未發布 Release"

    # Status alerts
    alerts = []
    if detail.get("archived"):
        alerts.append("> [!WARNING]\n> **本專案已被封存 (Archived)**：此 Repo 處於唯讀狀態，已停止積極維護。")
    if detail.get("is_fork"):
        alerts.append("> [!NOTE]\n> **Fork 衍生專案**：此專案源自上游分支。")

    alert_block = ("\n\n".join(alerts) + "\n\n") if alerts else ""

    # Structure & Health
    struct = detail.get("structure", {})
    health = struct.get("health_checklist", {})
    dirs = struct.get("dirs", [])
    manifests = struct.get("manifest_files", [])
    agent_configs = struct.get("agent_configs", [])
    deps = struct.get("core_dependencies", [])

    checklist_items = [
        f"{'✅' if health.get('has_tests') else '❌'} 測試套件 (`tests/`)",
        f"{'✅' if health.get('has_docs') else '❌'} 文件目錄 (`docs/`)",
        f"{'✅' if health.get('has_examples') else '❌'} 範例程式 (`examples/`)",
        f"{'✅' if health.get('has_ci_cd') else '❌'} 自動化 CI/CD (`.github/`)"
    ]
    if agent_configs:
        checklist_items.append(f"🤖 Agent 規格適配 ({', '.join(agent_configs)})")

    dirs_display = " ".join([f"`📁 {d}/`" for d in dirs[:10]]) or "（無頂層子目錄或純單檔）"
    manifests_display = ", ".join([f"`{m}`" for m in manifests]) or "無偵測到標準構建設定"
    deps_display = ", ".join([f"`{d}`" for d in deps]) if deps else "無或未提取"

    readme_block = ""
    if detail.get("readme_snippet"):
        readme_block = (
            "\n### 📖 README 核心摘錄\n"
            "```markdown\n"
            f"{detail['readme_snippet']}\n"
            "```\n"
    clone_block = (
        f"\n### 📥 快速獲取與本地測試\n"
        f"```bash\n"
        f"# 淺層克隆（極速，不拉取完整歷史紀錄）\n"
        f"git clone --depth 1 {detail['html_url']}.git\n\n"
        f"# 或使用 GitHub CLI\n"
        f"gh repo clone {detail['full_name']}\n"
        f"```\n"
    )

    return (
        f"## 🔍 專案深度剖析：[{detail['full_name']}]({detail['html_url']})\n\n"
        f"{alert_block}"
        f"* **主要語言**：`{detail['language']}` | **授權協議**：`{detail['license']}`\n"
        f"* **社群熱度**：⭐ {detail['stars']:,} Stars | 🍴 {detail['forks']:,} Forks | ❗ {detail['open_issues']} Issues | 👀 {detail['subscribers_count']} Watchers\n"
        f"* **時間節點**：創建於 `{detail['created_at']}` | 最近代碼推送 `{detail['pushed_at']}`\n"
        f"* **標籤主題**：{topics_str}\n"
        f"* **最新發布**：{rel_str}\n"
        f"* **核心描述**：{detail['description']}\n\n"
        f"### 📁 工程架構與健全度透視\n"
        f"* **頂層目錄**：{dirs_display}\n"
        f"* **健全度檢測**：{' | '.join(checklist_items)}\n"
        f"* **構建與設定**：{manifests_display}\n"
        f"* **核心依賴項**：{deps_display}\n"
        f"{readme_block}"
        f"{clone_block}"
    )


def format_compare_markdown(details):
    """Format multiple repositories into a side-by-side comparison matrix."""
    valid_details = [d for d in details if d is not None]
    if not valid_details:
        return "⚠️ 未能取得欲對比之專案資訊。"

    names = [f"**[{d['full_name']}]({d['html_url']})**" for d in valid_details]
    headers = ["維度 / 評估指標"] + names

    rows = []
    # 1. Description
    rows.append(["**核心定位與描述**"] + [(d["description"] or "無描述")[:60] + "..." if len(d["description"] or "") > 60 else (d["description"] or "無描述") for d in valid_details])
    # 2. Language & License
    rows.append(["**主要語言**"] + [f"`{d['language']}`" for d in valid_details])
    rows.append(["**授權協議 (License)**"] + [f"`{d['license']}`" for d in valid_details])
    # 3. Community Stats
    rows.append(["**社群熱度 (Stars / Forks)**"] + [f"⭐ {d['stars']:,} / 🍴 {d['forks']:,}" for d in valid_details])
    rows.append(["**未結 Issue / 關注者**"] + [f"❗ {d['open_issues']:,} / 👀 {d['subscribers_count']:,}" for d in valid_details])
    # 4. Activity
    rows.append(["**最近代碼推送 (Pushed)**"] + [f"`{d['pushed_at']}`" for d in valid_details])
    rows.append(["**專案建立時間**"] + [f"`{d['created_at']}`" for d in valid_details])
    # 5. Release
    def get_rel_str(d):
        r = d.get("latest_release")
        return f"`{r['tag_name']}` ({r['published_at']})" if r else "未發布 Release"
    rows.append(["**最新發布版本**"] + [get_rel_str(d) for d in valid_details])
    # 6. Status
    rows.append(["**維護狀態**"] + [("⚠️ 唯讀封存 (Archived)" if d.get("archived") else "🌱 活躍維護中") for d in valid_details])
    # 7. Health Checklist
    def check_icon(d, key):
        has = d.get("structure", {}).get("health_checklist", {}).get(key, False)
        return "✅ 有" if has else "❌ 無"
    rows.append(["**🧪 單元測試 (`tests/`)**"] + [check_icon(d, "has_tests") for d in valid_details])
    rows.append(["**📚 開發文件 (`docs/`)**"] + [check_icon(d, "has_docs") for d in valid_details])
    rows.append(["**💡 範例程式 (`examples/`)**"] + [check_icon(d, "has_examples") for d in valid_details])
    rows.append(["**⚡ 自動化 CI/CD (`.github/`)**"] + [check_icon(d, "has_ci_cd") for d in valid_details])
    # 8. Agent config
    rows.append(["**🤖 Agent 規範適配**"] + [", ".join(d.get("structure", {}).get("agent_configs", [])) or "—" for d in valid_details])
    # 9. Dependencies
    rows.append(["**📦 核心依賴摘要**"] + [", ".join(d.get("structure", {}).get("core_dependencies", [])[:5]) or "無/未解析" for d in valid_details])

    # Build markdown table
    lines = ["# ⚖️ 開源專案技術選型對比矩陣 (Comparison Matrix)\n"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join([":---"] * len(headers)) + " |")
    for r in rows:
        escaped = [c.replace("\n", " ").replace("|", "\\|") for c in r]
        lines.append("| " + " | ".join(escaped) + " |")

    # Quick clone snippet for all
    lines.append("\n### 📥 快速獲取所有對比專案")
    lines.append("```bash")
    for d in valid_details:
        lines.append(f"git clone --depth 1 {d['html_url']}.git")
    lines.append("```\n")

    return "\n".join(lines)


def output_result(content, output_path=None):
    """Output result to stdout and optionally write to a file."""
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            sys.stderr.write(f"\n[✅ 報告已匯出] 檔案已成功儲存至: {output_path}\n")
        except Exception as e:
            sys.stderr.write(f"\n[Error] 儲存檔案失敗: {e}\n")
    print(content)


def main():
    parser = argparse.ArgumentParser(
        description="Search latest and trending GitHub repositories with robust diagnostics, custom queries, compare matrix, and deep inspection."
    )
    parser.add_argument("--mode", choices=["search", "trending"], default="search", help="Mode: search or trending")
    parser.add_argument("-q", "--query", type=str, default="", help="Custom GitHub search query syntax (e.g. 'topic:agent stars:>=50')")
    parser.add_argument("--keyword", type=str, default="", help="Keyword to search in repo name/description/readme")
    parser.add_argument("--topic", type=str, default="", help="Specific GitHub topic (e.g. llm, agent, rag, rust)")
    parser.add_argument("--language", type=str, default="", help="Programming language (e.g. python, rust, typescript)")
    parser.add_argument("--days", type=int, default=None, help="Created within the last N days (e.g. 14)")
    parser.add_argument("--pushed-days", type=int, default=None, help="Pushed/updated within the last N days (e.g. 7)")
    parser.add_argument("--min-stars", type=int, default=None, help="Minimum stars threshold (e.g. 10)")
    parser.add_argument("--max-stars", type=int, default=None, help="Maximum stars threshold to spot hidden gems (e.g. 500)")
    parser.add_argument("--license", type=str, default="", help="License filter (e.g. mit, apache-2.0)")
    parser.add_argument("--sort", choices=["stars", "forks", "updated"], default="stars", help="Sort field")
    parser.add_argument("--since", choices=["daily", "weekly", "monthly"], default="daily", help="Trending timeframe")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of repositories to return")
    parser.add_argument("--json", action="store_true", help="Output pure JSON format")
    parser.add_argument("--token", type=str, default=None, help="GitHub Personal Access Token (can also be read from GITHUB_TOKEN or .env)")
    parser.add_argument("--info", type=str, default="", help="Deep-dive into a single repo (e.g. 'owner/repo')")
    parser.add_argument("-c", "--compare", type=str, default="", help="Compare multiple repositories separated by comma (e.g. 'repoA,repoB')")
    parser.add_argument("-o", "--output", type=str, default="", help="Save report output to a local file (e.g. 'report.md')")

    args = parser.parse_args()

    # Mode: Compare multiple repositories
    if args.compare:
        repo_names = [r.strip() for r in args.compare.split(",") if r.strip()]
        details = []
        for rname in repo_names:
            det = fetch_repo_info(rname, token=args.token)
            if det:
                details.append(det)
        if args.json:
            out_str = json.dumps(details, ensure_ascii=False, indent=2)
        else:
            out_str = format_compare_markdown(details)
        output_result(out_str, args.output)
        return

    # Mode: Deep-dive single repo
    if args.info:
        detail = fetch_repo_info(args.info, token=args.token)
        if args.json:
            out_str = json.dumps(detail, ensure_ascii=False, indent=2)
        else:
            out_str = format_repo_detail_markdown(detail)
        output_result(out_str, args.output)
        return

    # Mode: Trending
    if args.mode == "trending":
        repos = fetch_trending(language=args.language, since=args.since, token=args.token, limit=args.limit)
        if args.limit and len(repos) > args.limit:
            repos = repos[:args.limit]
        if args.json:
            out_str = json.dumps(repos, ensure_ascii=False, indent=2)
        else:
            out_str = format_markdown(repos, is_api=False)
        output_result(out_str, args.output)
        return

    # Mode: Search
    query_parts = []
    if args.query:
        query_parts.append(args.query.strip())
    if args.keyword:
        query_parts.append(args.keyword.strip())
    if args.topic:
        for t in args.topic.split(","):
            if t.strip():
                query_parts.append(f"topic:{t.strip()}")
    if args.language:
        query_parts.append(f"language:{args.language.strip()}")
    if args.license:
        query_parts.append(f"license:{args.license.strip()}")

    # Date filters
    raw_query = args.query or ""
    if args.days is not None and args.days > 0 and "created:" not in raw_query:
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=args.days)).strftime("%Y-%m-%d")
        query_parts.append(f"created:>{cutoff_date}")
    elif args.days is None and not args.pushed_days and not args.query and not args.keyword and not args.topic:
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        query_parts.append(f"created:>{cutoff_date}")

    if args.pushed_days is not None and args.pushed_days > 0 and "pushed:" not in raw_query:
        push_cutoff = (datetime.datetime.now() - datetime.timedelta(days=args.pushed_days)).strftime("%Y-%m-%d")
        query_parts.append(f"pushed:>{push_cutoff}")

    # Stars filters (support single threshold or range min..max)
    if "stars:" not in raw_query:
        if args.min_stars is not None and args.max_stars is not None:
            query_parts.append(f"stars:{args.min_stars}..{args.max_stars}")
        elif args.min_stars is not None:
            query_parts.append(f"stars:>={args.min_stars}")
        elif args.max_stars is not None:
            query_parts.append(f"stars:<={args.max_stars}")
        elif not args.query and not args.keyword:
            query_parts.append("stars:>=10")

    query = " ".join(query_parts).strip()
    if not query:
        query = f"stars:>100 created:>{(datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')}"

    items = search_github_api(query=query, sort=args.sort, order="desc", per_page=args.limit, token=args.token)

    if args.json:
        simplified = []
        for it in items:
            simplified.append({
                "name": it.get("name"),
                "full_name": it.get("full_name"),
                "html_url": it.get("html_url"),
                "description": it.get("description"),
                "language": it.get("language"),
                "stars": it.get("stargazers_count"),
                "forks": it.get("forks_count"),
                "open_issues": it.get("open_issues_count"),
                "created_at": (it.get("created_at") or "")[:10],
                "pushed_at": (it.get("pushed_at") or "")[:10],
                "topics": it.get("topics", [])
            })
        out_str = json.dumps(simplified, ensure_ascii=False, indent=2)
    else:
        out_str = format_markdown(items, is_api=True)

    output_result(out_str, args.output)


if __name__ == "__main__":
    main()

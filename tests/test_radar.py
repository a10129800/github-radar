#!/usr/bin/env python3
"""
Unit tests for GitHub Project Radar helper script.
Zero-dependency tests using Python standard library `unittest`.
"""

import unittest
import os
import sys

# Ensure scripts directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

import search_github


class TestRadarCore(unittest.TestCase):

    def test_parse_package_json(self):
        raw_json = """{
            "name": "sample-agent",
            "dependencies": {
                "react": "^18.2.0",
                "next": "^14.0.0",
                "lucide-react": "^0.300.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0",
                "eslint": "^8.0.0"
            }
        }"""
        deps = search_github.parse_manifest_dependencies("package.json", raw_json)
        self.assertIn("react", deps)
        self.assertIn("next", deps)
        self.assertIn("lucide-react", deps)
        self.assertTrue(any("typescript" in d for d in deps))

    def test_parse_cargo_toml(self):
        raw_cargo = """[package]
name = "fast-cli"
version = "0.1.0"

[dependencies]
tokio = { version = "1.0", features = ["full"] }
clap = { version = "4.0" }
serde = "1.0"

[dev-dependencies]
tempfile = "3.0"
"""
        deps = search_github.parse_manifest_dependencies("Cargo.toml", raw_cargo)
        self.assertIn("tokio", deps)
        self.assertIn("clap", deps)
        self.assertIn("serde", deps)

    def test_parse_requirements_txt(self):
        raw_req = """
# Production dependencies
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic==2.5.0
# Comment line
torch
"""
        deps = search_github.parse_manifest_dependencies("requirements.txt", raw_req)
        self.assertIn("fastapi", deps)
        self.assertIn("uvicorn", deps)
        self.assertIn("pydantic", deps)
        self.assertIn("torch", deps)

    def test_parse_go_mod(self):
        raw_gomod = """module github.com/user/project

go 1.22

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/stretchr/testify v1.8.4
)
"""
        deps = search_github.parse_manifest_dependencies("go.mod", raw_gomod)
        self.assertIn("gin", deps)
        self.assertIn("testify", deps)

    def test_format_compare_markdown(self):
        mock_a = {
            "full_name": "owner/repoA",
            "html_url": "https://github.com/owner/repoA",
            "description": "Repo A description",
            "stars": 1200,
            "forks": 150,
            "open_issues": 12,
            "subscribers_count": 45,
            "license": "MIT",
            "language": "Python",
            "created_at": "2026-01-01",
            "pushed_at": "2026-03-30",
            "archived": False,
            "latest_release": {"tag_name": "v1.0.0", "published_at": "2026-03-20"},
            "structure": {
                "health_checklist": {"has_tests": True, "has_docs": True, "has_examples": True, "has_ci_cd": True},
                "agent_configs": ["SKILL.md"],
                "core_dependencies": ["fastapi", "uvicorn"]
            }
        }
        mock_b = {
            "full_name": "owner/repoB",
            "html_url": "https://github.com/owner/repoB",
            "description": "Repo B description",
            "stars": 450,
            "forks": 30,
            "open_issues": 5,
            "subscribers_count": 12,
            "license": "Apache-2.0",
            "language": "Rust",
            "created_at": "2026-02-15",
            "pushed_at": "2026-03-28",
            "archived": False,
            "latest_release": None,
            "structure": {
                "health_checklist": {"has_tests": False, "has_docs": True, "has_examples": False, "has_ci_cd": False},
                "agent_configs": [],
                "core_dependencies": ["tokio"]
            }
        }
        markdown = search_github.format_compare_markdown([mock_a, mock_b])
        self.assertIn("對比矩陣", markdown)
        self.assertIn("owner/repoA", markdown)
        self.assertIn("owner/repoB", markdown)
        self.assertIn("1,200", markdown)
        self.assertIn("Apache-2.0", markdown)
        self.assertIn("git clone", markdown)


if __name__ == "__main__":
    unittest.main()

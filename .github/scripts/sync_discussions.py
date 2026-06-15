#!/usr/bin/env python3
"""Sync GitHub Discussions to Markdown files."""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests

# === Конфиг: список дискуссий для синка ===========================
# Формат: (owner, repo, discussion_number, output_filename_without_ext)
DISCUSSIONS = [
    ("gonka-ai", "gonka", 1116, "discussion-1116"),
    # ("gonka-ai", "gonka", 1117, "discussion-1117"),
]

OUTPUT_DIR = Path("docs/community/gsc")
# ==================================================================

GH_TOKEN = os.environ["GH_TOKEN"]
API_URL = "https://api.github.com/graphql"

QUERY = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      title
      url
      number
      createdAt
      updatedAt
      author { login url }
      category { name emoji }
      body
      comments(first: 100) {
        nodes {
          author { login url }
          createdAt
          body
          replies(first: 100) {
            nodes {
              author { login url }
              createdAt
              body
            }
          }
        }
      }
    }
  }
}
"""


def gh_graphql(query: str, variables: dict) -> dict:
    r = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {GH_TOKEN}",
            "Accept": "application/vnd.github+json",
        },
        json={"query": query, "variables": variables},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def fmt_date(iso: str) -> str:
    """2024-01-15T10:30:00Z → 2024-01-15 10:30 UTC"""
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def user_link(author: dict | None) -> str:
    if not author:
        return "*[deleted user]*"
    return f"[@{author['login']}]({author['url']})"


def indent_body(body: str, prefix: str = "> ") -> str:
    """Префиксует каждую строку — для оформления реплаев."""
    return "\n".join(prefix + line if line else prefix.rstrip() for line in body.splitlines())


def build_markdown(d: dict) -> str:
    out = []

    # --- Front-matter ---
    out.append("---")
    out.append(f"source: {d['url']}")
    out.append(f"discussion_number: {d['number']}")
    out.append(f"synced_at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    out.append("---")
    out.append("")

    # --- Баннер ---
    out.append(
        f"> 🔄 **Авто-синхронизация:** этот документ автоматически обновляется из "
        f"[GitHub Discussion #{d['number']}]({d['url']}) каждые 6 часов. "
        f"Прямые правки в репозитории будут перезаписаны."
    )
    out.append("")

    # --- Заголовок и метаданные ---
    out.append(f"# {d['title']}")
    out.append("")
    cat = d.get("category") or {}
    cat_str = f"{cat.get('emoji', '')} {cat.get('name', '')}".strip()
    out.append(
        f"**Автор:** {user_link(d['author'])} · "
        f"**Категория:** {cat_str} · "
        f"**Создано:** {fmt_date(d['createdAt'])} · "
        f"**Обновлено:** {fmt_date(d['updatedAt'])}"
    )
    out.append("")
    out.append("---")
    out.append("")

    # --- Тело дискуссии ---
    out.append("## 📝 Описание")
    out.append("")
    out.append(d["body"] or "*(пусто)*")
    out.append("")

    # --- Комментарии ---
    comments = d["comments"]["nodes"]
    if comments:
        out.append("---")
        out.append("")
        out.append(f"## 💬 Комментарии ({len(comments)})")
        out.append("")

        for i, c in enumerate(comments, 1):
            out.append(f"### Комментарий {i} — {user_link(c['author'])}")
            out.append("")
            out.append(f"*{fmt_date(c['createdAt'])}*")
            out.append("")
            out.append(c["body"] or "*(пусто)*")
            out.append("")

            replies = c.get("replies", {}).get("nodes", [])
            for r in replies:
                out.append(f"**↳ Ответ от {user_link(r['author'])}** · *{fmt_date(r['createdAt'])}*")
                out.append("")
                out.append(indent_body(r["body"] or "*(пусто)*"))
                out.append("")

    return "\n".join(out)


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for owner, repo, number, slug in DISCUSSIONS:
        print(f"Fetching {owner}/{repo}#{number}...")
        data = gh_graphql(QUERY, {"owner": owner, "repo": repo, "number": number})
        disc = data["repository"]["discussion"]
        if disc is None:
            print(f"  ⚠️  Discussion #{number} not found, skipping.")
            continue

        md = build_markdown(disc)
        target = OUTPUT_DIR / f"{slug}.md"
        target.write_text(md, encoding="utf-8")
        print(f"  ✓ Written {target}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

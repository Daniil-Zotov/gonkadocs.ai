#!/usr/bin/env python3
"""Sync all GitHub Discussions, organized by category folders."""

import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import requests

OWNER = os.environ["REPO_OWNER"]
REPO = os.environ["REPO_NAME"]
OUTPUT_DIR = Path(os.environ["OUTPUT_DIR"])
GH_TOKEN = os.environ["GH_TOKEN"]

API_URL = "https://api.github.com/graphql"
HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
}

LIST_QUERY = """
query($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 50, after: $cursor, orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes { number title updatedAt }
    }
  }
}
"""

DETAIL_QUERY = """
query($owner: String!, $repo: String!, $number: Int!, $commentsCursor: String) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $number) {
      title url number createdAt updatedAt
      author { login url }
      category { name emoji slug }
      body
      answer {
        author { login url }
        createdAt body
      }
      comments(first: 50, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        totalCount
        nodes {
          author { login url }
          createdAt body isAnswer
          replies(first: 100) {
            nodes { author { login url } createdAt body }
          }
        }
      }
    }
  }
}
"""


def gh_graphql(query, variables, retries=3):
    for attempt in range(retries):
        r = requests.post(API_URL, headers=HEADERS,
                          json={"query": query, "variables": variables}, timeout=60)
        if r.status_code in (502, 503) and attempt < retries - 1:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            raise RuntimeError(f"GraphQL errors: {data['errors']}")
        return data["data"]


def list_all_discussions():
    out, cursor = [], None
    while True:
        data = gh_graphql(LIST_QUERY, {"owner": OWNER, "repo": REPO, "cursor": cursor})
        page = data["repository"]["discussions"]
        out.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return out


def fetch_discussion(number):
    first = gh_graphql(DETAIL_QUERY, {
        "owner": OWNER, "repo": REPO, "number": number, "commentsCursor": None,
    })
    disc = first["repository"]["discussion"]
    if disc is None:
        return None
    all_comments = list(disc["comments"]["nodes"])
    page_info = disc["comments"]["pageInfo"]
    while page_info["hasNextPage"]:
        nxt = gh_graphql(DETAIL_QUERY, {
            "owner": OWNER, "repo": REPO, "number": number,
            "commentsCursor": page_info["endCursor"],
        })
        more = nxt["repository"]["discussion"]["comments"]
        all_comments.extend(more["nodes"])
        page_info = more["pageInfo"]
    disc["comments"]["nodes"] = all_comments
    return disc


# --- Утилиты ------------------------------------------------------

def slugify(text, max_len=60):
    text = (text or "").strip().lower()
    text = re.sub(r"[^\w\s\-а-яё]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len] or "untitled"


def category_folder(cat):
    """Категория → имя папки. Использует slug от GitHub, если есть."""
    if not cat:
        return "uncategorized"
    # GitHub отдаёт `slug` для категории — он уже kebab-case
    return cat.get("slug") or slugify(cat.get("name", "uncategorized"))


def category_label(cat):
    if not cat:
        return "📂 Uncategorized"
    return f"{cat.get('emoji', '📂')} {cat.get('name', 'Uncategorized')}".strip()


def fmt_date(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")


def fmt_date_short(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")


def user_link(author):
    if not author:
        return "*[deleted]*"
    return f"[@{author['login']}]({author['url']})"


def indent_body(body, prefix="> "):
    return "\n".join(prefix + l if l else prefix.rstrip() for l in body.splitlines())


# --- Markdown-генерация -------------------------------------------

def build_discussion_md(d):
    out = []
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    title_escaped = d["title"].replace('"', '\\"')

    out += [
        "---",
        f'title: "#{d["number"]} — {title_escaped}"',
        f"source: {d['url']}",
        f"discussion_number: {d['number']}",
        f"category: {category_folder(d.get('category'))}",
        f"synced_at: {sync_time}",
        "---",
        "",
        f"> 🔄 **Авто-синхронизация:** из [Discussion #{d['number']}]({d['url']}) каждые 6 часов. "
        f"Прямые правки будут перезаписаны.",
        "",
        f"# {d['title']}",
        "",
        f"**Автор:** {user_link(d['author'])} · "
        f"**Категория:** {category_label(d.get('category'))} · "
        f"**Создано:** {fmt_date(d['createdAt'])} · "
        f"**Обновлено:** {fmt_date(d['updatedAt'])}",
        "",
        "---",
        "",
        "## 📝 Описание",
        "",
        d["body"] or "*(пусто)*",
        "",
    ]

    if d.get("answer"):
        a = d["answer"]
        out += [
            "---", "",
            "## ✅ Выбранный ответ", "",
            f"**От:** {user_link(a['author'])} · *{fmt_date(a['createdAt'])}*", "",
            a["body"] or "*(пусто)*", "",
        ]

    comments = d["comments"]["nodes"]
    if comments:
        out += ["---", "", f"## 💬 Комментарии ({len(comments)})", ""]
        for i, c in enumerate(comments, 1):
            mark = " ✅" if c.get("isAnswer") else ""
            out += [
                f"### Комментарий {i}{mark} — {user_link(c['author'])}", "",
                f"*{fmt_date(c['createdAt'])}*", "",
                c["body"] or "*(пусто)*", "",
            ]
            for r in c.get("replies", {}).get("nodes", []):
                out += [
                    f"**↳ Ответ от {user_link(r['author'])}** · *{fmt_date(r['createdAt'])}*", "",
                    indent_body(r["body"] or "*(пусто)*"), "",
                ]

    return "\n".join(out)


def build_category_index(category_name, category_label_str, items):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    items_sorted = sorted(items, key=lambda x: x["number"], reverse=True)
    out = [
        "---",
        f'title: "{category_label_str}"',
        "---",
        "",
        f"# {category_label_str}",
        "",
        f"Дискуссии в категории **{category_label_str}**. Всего: **{len(items_sorted)}**. "
        f"Обновлено: `{sync_time}`.",
        "",
        "[← ко всем категориям](../index.md)",
        "",
        "| # | Заголовок | Автор | Обновлено |",
        "|---:|---|---|---|",
    ]
    for it in items_sorted:
        title_clean = it["title"].replace("|", "\\|")
        out.append(
            f"| [{it['number']}]({it['_filename']}) "
            f"| [{title_clean}]({it['_filename']}) "
            f"| {user_link(it.get('author'))} "
            f"| {fmt_date_short(it['updatedAt'])} |"
        )
    out.append("")
    return "\n".join(out)


def build_global_index(by_category, total):
    sync_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = [
        "---",
        'title: "GitHub Discussions"',
        "---",
        "",
        f"# GitHub Discussions — `{OWNER}/{REPO}`",
        "",
        f"Срез всех обсуждений из репозитория "
        f"[{OWNER}/{REPO}](https://github.com/{OWNER}/{REPO}/discussions). "
        f"Всего: **{total}**. Обновлено: `{sync_time}`.",
        "",
        "## 📂 Категории",
        "",
        "| Категория | Дискуссий |",
        "|---|---:|",
    ]
    for folder in sorted(by_category):
        items = by_category[folder]
        label = items[0]["_category_label"]
        out.append(f"| [{label}]({folder}/index.md) | {len(items)} |")
    out.append("")

    # Последние 20 дискуссий через все категории
    flat = [it for items in by_category.values() for it in items]
    flat.sort(key=lambda x: x["updatedAt"], reverse=True)
    recent = flat[:20]

    out += [
        "## 🕒 Последние обновлённые",
        "",
        "| # | Заголовок | Категория | Автор | Обновлено |",
        "|---:|---|---|---|---|",
    ]
    for it in recent:
        title_clean = it["title"].replace("|", "\\|")
        path = f"{it['_category_folder']}/{it['_filename']}"
        out.append(
            f"| [{it['number']}]({path}) "
            f"| [{title_clean}]({path}) "
            f"| {it['_category_label']} "
            f"| {user_link(it.get('author'))} "
            f"| {fmt_date_short(it['updatedAt'])} |"
        )
    out.append("")
    return "\n".join(out)


# --- Main ---------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Listing discussions in {OWNER}/{REPO}...")
    listing = list_all_discussions()
    print(f"Found {len(listing)}.")

    by_category = defaultdict(list)
    # Файлы, которые должны остаться (относительно OUTPUT_DIR)
    seen_paths = {Path("index.md")}

    for meta in listing:
        number = meta["number"]
        print(f"  → #{number} {meta['title'][:60]}")
        disc = fetch_discussion(number)
        if disc is None:
            continue

        folder = category_folder(disc.get("category"))
        label = category_label(disc.get("category"))
        slug = slugify(disc["title"])
        filename = f"{number:04d}-{slug}.md"

        cat_dir = OUTPUT_DIR / folder
        cat_dir.mkdir(parents=True, exist_ok=True)

        (cat_dir / filename).write_text(build_discussion_md(disc), encoding="utf-8")
        seen_paths.add(Path(folder) / filename)
        seen_paths.add(Path(folder) / "index.md")

        by_category[folder].append({
            "number": disc["number"],
            "title": disc["title"],
            "author": disc.get("author"),
            "updatedAt": disc["updatedAt"],
            "_filename": filename,
            "_category_folder": folder,
            "_category_label": label,
        })

    # index.md в каждой категории
    for folder, items in by_category.items():
        label = items[0]["_category_label"]
        (OUTPUT_DIR / folder / "index.md").write_text(
            build_category_index(folder, label, items), encoding="utf-8"
        )

    # Глобальный index.md
    (OUTPUT_DIR / "index.md").write_text(
        build_global_index(by_category, len(listing)), encoding="utf-8"
    )

    # Удаляем то, чего больше нет
    for path in OUTPUT_DIR.rglob("*.md"):
        rel = path.relative_to(OUTPUT_DIR)
        if rel not in seen_paths:
            print(f"  ✗ removing stale {rel}")
            path.unlink()
    # Удаляем пустые папки от исчезнувших категорий
    for p in sorted(OUTPUT_DIR.glob("*"), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()

    print(f"Done. {len(listing)} discussions across {len(by_category)} categories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

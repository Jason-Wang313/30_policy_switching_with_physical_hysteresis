from __future__ import annotations

import csv
import re
import time
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

API = "https://api.crossref.org/works"
HEADERS = {"User-Agent": "Mozilla/5.0 (codex literature sweep)"} 

QUERIES = [
    "robot policy switching hysteresis",
    "chatter-free switching robot control",
    "hybrid control robot hysteresis contact",
    "dexterous manipulation switching policy",
    "safe reinforcement learning policy switching",
    "hysteresis robot control manipulation",
    "contact-rich manipulation policy",
    "skill switching robotics",
    "adaptive robot control hysteresis",
    "policy supervisor robotics",
]


def norm(s: str | None) -> str:
    s = (s or "").replace("\n", " ").strip()
    return re.sub(r"\s+", " ", s)


def rel(title: str, query: str, cited: int) -> float:
    t = title.lower()
    q = query.lower()
    score = 0.0
    for k, w in {
        "policy": 2,
        "switch": 3,
        "switching": 5,
        "hysteresis": 10,
        "chatter": 8,
        "hybrid": 3,
        "contact": 4,
        "robot": 4,
        "manipulation": 4,
        "control": 2,
        "skill": 2,
        "safe": 1,
        "rl": 1,
    }.items():
        if k in t or k in q:
            score += w
    score += min(cited, 200) / 100.0
    return round(score, 3)


def main():
    rows = {}
    per_query = 250
    cursor = 0
    progress = DOCS / "literature_sweep_progress.json"
    for query in QUERIES:
        for page in range(5):
            params = {"query.title": query, "rows": 100, "offset": page * 100}
            try:
                r = requests.get(API, params=params, headers=HEADERS, timeout=60)
                r.raise_for_status()
                items = r.json()["message"]["items"]
            except Exception as exc:
                progress.write_text(f'{{"query": "{query}", "page": {page}, "error": "{exc}"}}', encoding="utf-8")
                time.sleep(0.5)
                continue
            for it in items:
                doi = norm(it.get("DOI"))
                title = norm(it.get("title", [""])[0] if it.get("title") else "")
                if not doi or doi in rows:
                    continue
                year = None
                parts = it.get("published", {}).get("date-parts") or it.get("created", {}).get("date-parts")
                if parts and parts[0]:
                    year = parts[0][0]
                cited = it.get("is-referenced-by-count", 0) or 0
                rows[doi] = {
                    "doi": doi,
                    "query_seed": query,
                    "title": title,
                    "year": year or "",
                    "venue": norm((it.get("container-title") or [""])[0]),
                    "publisher": norm(it.get("publisher")),
                    "type": norm(it.get("type")),
                    "cited_by_count": cited,
                    "relevance_score": rel(title, query, cited),
                    "url": f"https://doi.org/{doi}",
                }
            progress.write_text(f'{{"rows": {len(rows)}, "query": "{query}", "page": {page}}}', encoding="utf-8")
            time.sleep(0.2)

    out = DOCS / "related_work_matrix.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["doi", "query_seed", "title", "year", "venue", "publisher", "type", "cited_by_count", "relevance_score", "url"],
        )
        writer.writeheader()
        for row in sorted(rows.values(), key=lambda r: (-r["relevance_score"], -int(r["cited_by_count"]), r["title"])):
            writer.writerow(row)
    print(f"saved {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()

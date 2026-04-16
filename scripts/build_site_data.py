#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOVELS_DIR = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Novels"
OUT_JSON = ROOT / "data" / "site-data.json"
OUT_JS = ROOT / "data" / "site-data.js"

AUTHOR = {
    "name": "Jorge Aguirre",
    "firstName": "Jorge",
    "lastName": "Aguirre",
    "kicker": "Author portfolio",
    "microNote": "Speculative thrillers, political dystopias, and dark fantasy",
    "tagline": (
        "Speculative thrillers, political dystopias, and dark fantasy about systems "
        "that promise safety and quietly demand surrender."
    ),
    "deck": (
        "Across dead-witness trials, water tribunals, memory clinics, climate electorates, "
        "ritual houses, Mars colonies, and legitimacy machines, the throughline is consistent: "
        "these novels live where power becomes procedural, intimate, and impossible to ignore."
    ),
    "panelCopy": (
        "The right-hand rail tracks the manuscripts that best show the range: high-pressure "
        "speculative thrillers, one mythic epic, and a library organized around moral pressure."
    ),
    "about": (
        "Jorge Aguirre writes for readers who want elegant premises, ruthless momentum, and "
        "questions that stay hot after the final page. The protagonists are usually witnesses, "
        "auditors, nurses, lawyers, pilots, or rulers who believe systems can be made legible "
        "until they discover those systems were built to decide whose lives count."
    ),
}

SECTIONS = {
    "featured": (
        "These are the manuscripts that best explain the brand at a glance: near-future pressure "
        "cookers, conspiracy engines, a dark fantasy counterpoint, and stories where the official "
        "narrative is almost always the first lie."
    ),
    "library": (
        "Every title below was pulled from the active novels folder in iCloud Drive, then grouped "
        "into three in-house tracks so the portfolio scans like a body of work rather than a stack "
        "of unrelated ideas."
    ),
    "obsessions": (
        "The range is real, but the obsessions repeat. Again and again these books ask who controls "
        "truth, what grief becomes when systems monetize it, and how beauty or procedure can disguise coercion."
    ),
    "footer": (
        "This site is intentionally portfolio-first. It avoids invented publication claims and sticks "
        "to what the manuscript library actually supports: titles, loglines, promise, thematic pressure, and range."
    ),
}

TRACKS = {
    "pressure-systems": "Pressure Systems",
    "memory-and-identity": "Memory and Identity",
    "epic-orders": "Epic Orders",
}

OVERRIDES = {
    "Borrowed Witness": {
        "title": "Borrowed Witness",
        "track": "pressure-systems",
        "accent": "#d5603b",
        "featured": True,
        "tags": ["Dead testimony", "Courtroom pressure", "Grief tech"],
    },
    "Clean Slate": {
        "title": "What the Body Kept",
        "track": "memory-and-identity",
        "accent": "#8b4a44",
        "featured": True,
        "tags": ["Memory clinic", "Body horror", "Secret archive"],
    },
    "Night Shift": {
        "title": "Night Shift",
        "track": "pressure-systems",
        "accent": "#d78b38",
        "featured": True,
        "tags": ["Hospital AI", "One-night clock", "Medical thriller"],
        "genre": "Near-future medical thriller",
    },
    "Second Self": {
        "title": "Second Self",
        "track": "memory-and-identity",
        "accent": "#48819a",
        "featured": False,
        "tags": ["Digital family", "Reintegration", "Consent"],
    },
    "THE ARCHITECT": {
        "title": "The Architect",
        "track": "pressure-systems",
        "accent": "#5f738a",
        "featured": False,
        "tags": ["Engineered lives", "Domestic conspiracy", "Free will"],
    },
    "The Blue Fire": {
        "title": "The Blue Fire",
        "track": "epic-orders",
        "accent": "#416fc2",
        "featured": True,
        "tags": ["Blue Wizards", "Corrupted mission", "Cult empire"],
        "genre": "Epic fantasy / mythic political tragedy",
    },
    "The Ethics Floor": {
        "title": "The Ethics Floor",
        "track": "pressure-systems",
        "accent": "#7f8b8b",
        "featured": True,
        "tags": ["Impossible murder", "Luxury tower", "AI witness"],
    },
    "The First Return": {
        "title": "The First Return",
        "track": "epic-orders",
        "accent": "#9a9453",
        "featured": False,
        "tags": ["Mars colony", "Home vs rescue", "Inheritance"],
    },
    "The Guest": {
        "title": "By Invitation",
        "track": "memory-and-identity",
        "accent": "#6e5d51",
        "featured": False,
        "tags": ["Ritual house", "Damaged texts", "Gothic suspense"],
    },
    "The Hollow Crown": {
        "title": "The Hollow Crown",
        "track": "epic-orders",
        "accent": "#a57436",
        "featured": True,
        "tags": ["Legitimacy machine", "Court intrigue", "Relic magic"],
    },
    "The Second Jury": {
        "title": "The Second Jury",
        "track": "pressure-systems",
        "accent": "#158778",
        "featured": False,
        "tags": ["Split verdict", "AI retrial", "Manhunt"],
    },
    "The Second Sun": {
        "title": "The Second Sun",
        "track": "pressure-systems",
        "accent": "#e15b2f",
        "featured": True,
        "tags": ["Climate authority", "Election sabotage", "Orbital shield"],
    },
    "The Water Jury": {
        "title": "The Water Jury",
        "track": "pressure-systems",
        "accent": "#2b93a8",
        "featured": True,
        "tags": ["Televised scarcity", "Mother-daughter", "Civic cruelty"],
    },
}

CURRENT_FOCUS = [
    "night-shift",
    "what-the-body-kept",
    "the-blue-fire",
]

FEATURED_ORDER = [
    "borrowed-witness",
    "what-the-body-kept",
    "night-shift",
    "the-water-jury",
    "the-ethics-floor",
    "the-second-sun",
    "the-hollow-crown",
    "the-blue-fire",
]

OBSERVATIONS = [
    {
        "title": "Institutions Sell Safety",
        "body": (
            "Hospitals, courts, towers, clinics, agencies, and crown-states all say the same thing first: "
            "trust the system and nobody gets hurt. The novels start exactly where that sales pitch breaks."
        ),
    },
    {
        "title": "Truth Gets Curated",
        "body": (
            "Official records are never neutral here. They are edited, staged, optimized, ritualized, or "
            "commercialized until the protagonists have to decide whether truth can survive the format built to contain it."
        ),
    },
    {
        "title": "Private Grief Turns Public",
        "body": (
            "Love, bereavement, loyalty, and memory do not stay personal. Again and again they become inputs for "
            "larger systems of control, which is what gives the thrillers their human heat."
        ),
    },
    {
        "title": "Beautiful Machines Bite",
        "body": (
            "The settings are polished, elegant, high-functioning, and initially persuasive. Then the reader notices "
            "what those systems require from the people trapped inside them and the surface glamour becomes menace."
        ),
    },
]


def normalize_text(value: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    normalized = value
    for src, target in replacements.items():
        normalized = normalized.replace(src, target)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug


def title_case_folder(folder_name: str) -> str:
    lowered = folder_name.replace("_", " ").strip()
    return " ".join(word.capitalize() for word in lowered.split())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(markdown: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*\n+(.*?)(?=^## |\Z)"
    match = re.search(pattern, markdown, re.S | re.M)
    return normalize_text(match.group(1)) if match else ""


def extract_first_heading(markdown: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown, re.M)
    return normalize_text(match.group(1)) if match else ""


def first_sentence(text: str) -> str:
    normalized = normalize_text(text)
    parts = re.split(r"(?<=[.!?])\s+", normalized)
    return parts[0] if parts else normalized


def first_sentences(text: str, count: int = 2) -> str:
    normalized = normalize_text(text)
    parts = [part for part in re.split(r"(?<=[.!?])\s+", normalized) if part]
    return " ".join(parts[:count]) if parts else normalized


def parse_bullet_book(path: Path, folder_name: str) -> dict:
    text = read_text(path)
    pairs = {}
    for line in text.splitlines():
        match = re.match(r"- ([^:]+):\s*(.+)", line.strip())
        if match:
            key, value = match.groups()
            pairs[normalize_text(key).lower()] = normalize_text(value)

    title = pairs.get("working title") or pairs.get("title") or title_case_folder(folder_name)
    logline = pairs.get("logline") or pairs.get('one-sentence "what if?"') or pairs.get(
        "one-sentence what if?"
    )
    theme_question = (
        pairs.get("theme question")
        or pairs.get("human truth")
        or pairs.get("human truth under the speculative lie")
        or pairs.get('one-sentence "what if?"')
        or pairs.get("one-sentence what if?")
    )
    return {
        "title": title,
        "genre": pairs.get("genre / shelf", "Speculative fiction"),
        "logline": logline or "",
        "promise": pairs.get("reader promise", ""),
        "themeQuestion": theme_question or "",
        "sourceLabel": str(path.relative_to(NOVELS_DIR)),
    }


def build_clean_slate(folder: Path) -> dict:
    path = folder / "story-bible" / "00-book-dna.md"
    text = read_text(path)
    title = extract_first_heading(text) or "What the Body Kept"
    promise = extract_section(text, "Core Promise")
    what_if = extract_section(text, "One-Sentence What If?")
    return {
        "title": title,
        "genre": "Upmarket speculative crime thriller / literary suspense",
        "logline": what_if or (
            "Five carefully selected patients arrive at an elite Swiss memory clinic and discover the "
            "clinic kept every erased memory in a private archive."
        ),
        "promise": first_sentences(promise, 2),
        "themeQuestion": (
            "If pain is also evidence, memory, and obligation, who gets to decide which parts of a self are disposable?"
        ),
        "sourceLabel": str(path.relative_to(NOVELS_DIR)),
    }


def build_night_shift(folder: Path) -> dict:
    path = folder / "Night Shift - novel skeleton.md"
    text = read_text(path)
    hook = extract_section(text, "One-line hook")
    human_truth = extract_section(text, "The human truth underneath the premise")
    return {
        "title": "Night Shift",
        "genre": OVERRIDES["Night Shift"]["genre"],
        "logline": hook,
        "promise": (
            "One hospital, one overnight shift, one diagnostic AI making lethal recommendations, "
            "and one nurse trying to prove it before sunrise."
        ),
        "themeQuestion": human_truth or (
            "What happens when clinical judgment gets treated as inefficiency instead of responsibility?"
        ),
        "sourceLabel": str(path.relative_to(NOVELS_DIR)),
    }


def build_first_return(folder: Path) -> dict:
    path = folder / "story-bible" / "00-book-dna.md"
    text = read_text(path)
    core_promise = extract_section(text, "Core Promise")
    what_if = extract_section(text, "One-Sentence What If?")
    return {
        "title": "The First Return",
        "genre": "Upmarket speculative suspense / Mars political drama",
        "logline": what_if,
        "promise": first_sentences(core_promise, 2),
        "themeQuestion": (
            "When does rescue become a softer form of violence, especially when home is the place built inside the danger?"
        ),
        "sourceLabel": str(path.relative_to(NOVELS_DIR)),
    }


def build_blue_fire(folder: Path) -> dict:
    path = folder / "The Blue Fire Novel Skeleton.pdf"
    try:
        result = subprocess.run(
            ["pdftotext", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
        pdf_text = normalize_text(result.stdout)
    except (FileNotFoundError, subprocess.CalledProcessError):
        pdf_text = ""

    central_question_match = re.search(r"Central Question: (.+?)(?: SETTING| THEMES|$)", pdf_text)
    premise_match = re.search(r"PREMISE (.+?) SETTING", pdf_text)
    premise = normalize_text(premise_match.group(1)) if premise_match else (
        "The untold story of the Blue Wizards sent east to contest Sauron, only to become the founders "
        "of the cult they were meant to resist."
    )
    premise = normalize_text(premise.split("Central Question:")[0])
    theme_question = (
        normalize_text(central_question_match.group(1))
        if central_question_match
        else "What happens when saviors begin to believe they are necessary?"
    )
    return {
        "title": "The Blue Fire",
        "genre": OVERRIDES["The Blue Fire"]["genre"],
        "logline": premise,
        "promise": (
            "Two emissaries sent to save Middle-earth's East become the architects of a sacred empire built "
            "on obedience, spectacle, and betrayal."
        ),
        "themeQuestion": theme_question,
        "sourceLabel": str(path.relative_to(NOVELS_DIR)),
    }


def build_book(folder_name: str) -> dict | None:
    folder = NOVELS_DIR / folder_name
    if folder_name == "Clean Slate":
        return build_clean_slate(folder)
    if folder_name == "Night Shift":
        return build_night_shift(folder)
    if folder_name == "The First Return":
        return build_first_return(folder)
    if folder_name == "The Blue Fire":
        return build_blue_fire(folder)

    dna_path = folder / "story-bible" / "00-book-dna.md"
    if dna_path.exists():
        return parse_bullet_book(dna_path, folder_name)
    return None


def build_books() -> list[dict]:
    books = []
    for folder_name, override in OVERRIDES.items():
        parsed = build_book(folder_name)
        if not parsed:
            continue

        title = override["title"]
        track_slug = override["track"]
        book = {
            "title": title,
            "slug": slugify(title),
            "trackSlug": track_slug,
            "track": TRACKS[track_slug],
            "accent": override["accent"],
            "featured": override["featured"],
            "tags": override["tags"],
            "genre": normalize_text(parsed["genre"]),
            "logline": normalize_text(parsed["logline"]),
            "promise": normalize_text(parsed["promise"]),
            "themeQuestion": normalize_text(parsed["themeQuestion"]),
            "sourceLabel": normalize_text(parsed["sourceLabel"]),
        }
        books.append(book)

    books.sort(key=lambda item: (item["track"], item["title"]))
    return books


def order_featured(books: list[dict]) -> list[dict]:
    lookup = {book["slug"]: book for book in books}
    return [lookup[slug] for slug in FEATURED_ORDER if slug in lookup]


def build_tracks(books: list[dict]) -> list[dict]:
    tracks = [{"slug": "all", "label": "All projects", "count": len(books)}]
    for slug, label in TRACKS.items():
        count = sum(1 for book in books if book["trackSlug"] == slug)
        tracks.append({"slug": slug, "label": label, "count": count})
    return tracks


def build_snapshot(books: list[dict]) -> list[dict]:
    pressure_count = sum(1 for book in books if book["trackSlug"] == "pressure-systems")
    memory_count = sum(1 for book in books if book["trackSlug"] == "memory-and-identity")
    epic_count = sum(1 for book in books if book["trackSlug"] == "epic-orders")
    return [
        {"label": "Projects parsed", "value": str(len(books)).zfill(2)},
        {"label": "Pressure systems", "value": str(pressure_count).zfill(2)},
        {"label": "Memory and identity", "value": str(memory_count).zfill(2)},
        {"label": "Epic orders", "value": str(epic_count).zfill(2)},
    ]


def main() -> None:
    books = build_books()
    featured = order_featured(books)
    current_lookup = {book["slug"]: book for book in books}
    current_focus = [current_lookup[slug] for slug in CURRENT_FOCUS if slug in current_lookup]

    payload = {
        "author": {
            **AUTHOR,
            "sourceNote": "parsed from iCloud Drive / Novels",
        },
        "currentYear": 2026,
        "sections": SECTIONS,
        "featured": featured,
        "books": books,
        "tracks": build_tracks(books),
        "snapshot": build_snapshot(books),
        "currentFocus": current_focus,
        "obsessions": OBSERVATIONS,
        "footerNotes": [
            "Every title and logline here was sourced from manuscript materials in the Novels folder.",
            "The library is grouped into custom tracks so the range reads as a body of work.",
            "Contact information was not inferred; add a preferred email or agent line before publishing.",
        ],
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    js_payload = "window.__AUTHOR_SITE_DATA__ = " + json.dumps(payload, indent=2) + ";\n"
    OUT_JS.write_text(js_payload, encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_JS}")


if __name__ == "__main__":
    main()

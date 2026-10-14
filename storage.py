"""Local JSON storage for journal entries."""
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "entries.json"
CHECKINS_FILE = DATA_DIR / "checkins.json"
SUPPORT_PLAN_FILE = DATA_DIR / "support_plan.json"
DAILY_PRACTICE_FILE = DATA_DIR / "daily_practice.json"
CUSTOM_WISDOM_FILE = DATA_DIR / "custom_wisdom.json"


def load_entries() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_entry(entry: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entries = load_entries()
    entry["date"] = datetime.now().isoformat(timespec="seconds")
    entries.append(entry)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def has_had_before(categories: list[str] | str) -> bool:
    """Check whether any of these thinking-trap categories has shown up in a past entry."""
    if not categories:
        return False
    if isinstance(categories, str):
        categories = [categories]
    wanted = set(categories)
    for e in load_entries():
        past = e.get("category")
        if not past:
            continue
        past_categories = {past} if isinstance(past, str) else set(past)
        if wanted & past_categories:
            return True
    return False


def load_checkins() -> list[dict]:
    if not CHECKINS_FILE.exists():
        return []
    with open(CHECKINS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_checkin(signs: list[str], tier: str, also_good: str = "") -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    checkins = load_checkins()
    checkins.append(
        {
            "date": datetime.now().isoformat(timespec="seconds"),
            "signs": signs,
            "tier": tier,
            "also_good": also_good,
        }
    )
    with open(CHECKINS_FILE, "w", encoding="utf-8") as f:
        json.dump(checkins, f, ensure_ascii=False, indent=2)


def load_support_plan() -> str:
    if not SUPPORT_PLAN_FILE.exists():
        return ""
    with open(SUPPORT_PLAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("text", "")


def save_support_plan(text: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SUPPORT_PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"text": text, "updated": datetime.now().isoformat(timespec="seconds")},
            f,
            ensure_ascii=False,
            indent=2,
        )


def load_custom_wisdom() -> list[dict]:
    """User-added wisdom-library entries (Step 3), stored alongside the seeded content."""
    if not CUSTOM_WISDOM_FILE.exists():
        return []
    with open(CUSTOM_WISDOM_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_custom_wisdom(text: str, categories: list[str], source: str = "My own truths") -> None:
    """Add a user-written wisdom/truth entry. An empty category list means it applies generally."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entries = load_custom_wisdom()
    entries.append(
        {
            "category": categories,
            "source": source or "My own truths",
            "text": text,
            "date": datetime.now().isoformat(timespec="seconds"),
        }
    )
    with open(CUSTOM_WISDOM_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def delete_custom_wisdom(index: int) -> None:
    """Remove a user-added wisdom entry by its index in load_custom_wisdom()."""
    entries = load_custom_wisdom()
    if 0 <= index < len(entries):
        del entries[index]
        with open(CUSTOM_WISDOM_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)


def load_daily_practice_log() -> list[dict]:
    if not DAILY_PRACTICE_FILE.exists():
        return []
    with open(DAILY_PRACTICE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def has_done_daily_practice(day: str) -> bool:
    return any(e["date"] == day for e in load_daily_practice_log())


def mark_daily_practice_done(day: str, practice: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    log = load_daily_practice_log()
    log.append({"date": day, "practice": practice})
    with open(DAILY_PRACTICE_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

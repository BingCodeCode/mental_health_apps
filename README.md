# Live From My Head

A personal, local-first Streamlit app for working through an overthinking spiral in the
moment: calm down, journal it out, spot the thinking trap, pull up some grounding wisdom,
apply a targeted practice, then close with some self-kindness. Built for one person's own
patterns (overthinking, control, people-pleasing, inner critic) — not a clinical tool, and
not built by a psychologist.

> 🔒 **Privacy note:** this is a *self*-journaling tool. All data (journal entries, check-ins,
> support plan) is stored locally as JSON under `data/`. `.gitignore` excludes all private
> data from version control, so none of it is ever committed. Nothing is sent anywhere.

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Flow

1. **Early warning sign check-in** (optional entry point) — quick self-check against a
   list of warning signs, tiered green/yellow/orange, with an editable support plan.
2. **Step 1 — Calm down & feel, then journal** — breathe, free-write, note one good thing.
3. **Step 2 — Thought tree & thinking traps** — write the raw, unfiltered thought, check
   whether it's a thought or a fact, then categorize it against a list of common thinking
   traps (mind reading, catastrophizing, all-or-nothing, inner critic, etc.).
4. **Step 3 — Wisdom library** — relevant quotes/realizations filtered by the trap
   category from Step 2, plus the ability to add your own.
5. **Step 4 — Apply a targeted practice** — a practice matched to the category (courage to
   be disliked, inner-critic plan, let-go/surrender, overthinking).
6. **Step 5 — Be kind to yourself** — a closing self-compassion / "friend question" step.

## Layout

Data is persisted to `data/*.json` via [`storage.py`](./storage.py); most content (thinking
traps, practices) lives in [`content.py`](./content.py), while the wisdom library quotes
live in `library/wisdom_library.json` (local-only, see privacy note above) so they're easy
to add to without touching code. A non-personal
[`library/wisdom_library.sample.json`](./library/wisdom_library.sample.json) is tracked in
the repo to show the format, and is used automatically as a fallback if your real
`wisdom_library.json` doesn't exist yet.

## Known gaps / roadmap

Tracked as TODOs at the top of [`app.py`](./app.py):

- Step 2: use an LLM to infer the core belief from the written thought instead of manual
  category selection.
- Step 3: tailor/pick wisdom quotes based on the exact thought text, not just category.
- Warning-sign check-in: the signs list is fixed (not yet editable), and there's no trend
  view over past check-ins.

The wisdom library and thinking-traps list are intentionally a small seed set, meant to
grow from real use over time rather than be exhaustive up front.

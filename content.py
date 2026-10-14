"""Static content for the app, seeded from the planning notebooks."""
import json
from pathlib import Path

LIBRARY_DIR = Path(__file__).parent / "library"

CORE_PROBLEMS = {
    "overthinking": {"emoji": "🌀", "label": "Overthinking"},
    "control": {"emoji": "🎯", "label": "Control"},
}

THINKING_TRAPS = [
    {"name": "Mind Reading", "root": "control", "description": "assuming you know what others are thinking (e.g. \"She/he doesn't like me\")."},
    {"name": "Fortune Telling", "root": "control", "description": "predicting a bad outcome as if it were certain."},
    {"name": "All-or-Nothing Thinking", "root": "overthinking", "description": "black-and-white, no middle ground."},
    {"name": "Overgeneralization", "root": "overthinking", "description": "one bad event becomes \"always\" / \"never\"."},
    {"name": "Mental Filter", "root": "overthinking", "description": "only seeing the negative detail, ignoring the rest."},
    {"name": "Discounting the Positive", "root": "overthinking", "description": "good things \"don't count\"."},
    {"name": "Catastrophizing", "root": "control", "description": "blowing things out of proportion."},
    {"name": "Emotional Reasoning", "root": "overthinking", "description": "\"I feel it, so it must be true.\""},
    {"name": "Should Statements", "root": "control", "description": "rigid rules for self/others (\"I should/must...\")."},
    {"name": "Labeling", "root": "overthinking", "description": "\"I'm a failure\" instead of \"I made a mistake.\""},
    {"name": "Personalization", "root": "control", "description": "taking blame/responsibility for things outside your control."},
    {"name": "Inner Critic", "root": None, "description": "a harsh internal voice attacking/judging you directly (e.g. \"you're annoying\", \"you're not good enough\")."},
    {"name": "Other", "root": None, "description": "doesn't fit a category above."},
]


def _load_wisdom_library() -> list[dict]:
    """Quotes/realizations live in library/wisdom_library.json (data, not code) so they're
    easy to grow over time without touching this file. That file is gitignored (personal
    content), so fall back to the tracked sample file if it's missing (e.g. fresh clone)."""
    path = LIBRARY_DIR / "wisdom_library.json"
    if not path.exists():
        path = LIBRARY_DIR / "wisdom_library.sample.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


WISDOM_LIBRARY = _load_wisdom_library()

LET_GO_PRACTICES = [
    "😮‍💨 Box breathing: in 4, hold 4, out 4, hold 4 — repeat until your body settles.",
    "🖐️ 5-4-3-2-1 grounding: name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste.",
    "📝 Write the worry down, then set it aside — it doesn't need solving right now.",
    "🧩 Pick one next step only: the smallest possible action, ignore the rest of the pile.",
    "🫶 Name it: \"I'm scared/worried right now\" — naming the feeling takes some of its power away.",
    "🚶 Move your body: a short walk or stretch to burn off anxious energy.",
]

EXPOSURE_EXERCISES = [
    "Let someone else pick where to eat tonight.",
    "Send a message without re-reading it first.",
    "Leave something undone/imperfect on purpose.",
    "Go somewhere without planning the route.",
    "Say yes to a plan without knowing all the details.",
    "Spend a day with no to-do list.",
    "Don't check Teams and emails so often — let messages sit unread/unanswered for a while.",
]

# Pool for the daily "let go / stop controlling" practice reminder.
DAILY_PRACTICE_POOL = LET_GO_PRACTICES + EXPOSURE_EXERCISES

COURAGE_TO_BE_DISLIKED = [
    "🦁 Courage to be disliked: accept that not everyone will approve of you, and that's okay.",
    "🎨 Courage to be yourself: show your own colors instead of molding yourself to fit others' expectations.",
    "🙅 Courage to not please people: stop seeking validation/approval as your main driver for action.",
]

COURAGE_PRACTICES = [
    "🗣️ Say your actual opinion once today, even if it's not what the other person wants to hear.",
    "🙋 Decline a request/invite you don't want to do, without over-explaining or apologizing for it.",
    "✋ Let a disagreement or silence stand instead of smoothing it over to keep everyone comfortable.",
    "🚫 Catch yourself mid-sentence softening an opinion to please someone, and say the real one instead.",
    "💬 Ask for what you actually want in a situation, instead of defaulting to what's easiest for others.",
    "👕 Choose/do something that's just \"you\" today, even if it's not what others would pick.",
]

# For automatic/intrusive thoughts that fire when feeling vulnerable — overthinking-rooted categories.
OVERTHINKING_PRACTICES = [
    "🏷️ Label it fast: \"that's an automatic thought, not a fact\" — name it and move on, don't investigate it.",
    "🌊 Let it surf: picture it as a wave — it rises, peaks, and passes on its own if you don't paddle after it.",
    "🫂 Vulnerable ≠ unsafe: when it shows up right after feeling exposed, that's the trigger, not evidence something's wrong.",
    "✋ Don't investigate: you don't need to find out why it came or whether it's true right now.",
    "🧷 Anchor to one physical sense: touch something, feel your feet on the ground — pulls attention out of the loop.",
    "📝 One-line note, not an essay: jot it down in a few words so it's acknowledged, then put the pen down.",
]

CORE_STANCE = (
    "The core stance for both: let the thought be there. Don't push it away, don't fight it, "
    "don't engage with its content — just notice it and let it sit, without trying to resolve "
    "or argue with it."
)

# From inner_critic.ipynb — a repeatable plan, not an attempt to destroy the critic.
INNER_CRITIC_PLAN = [
    {
        "step": "1. Catch it",
        "text": "When you notice \"Did I do something wrong?\" / \"Was I annoying?\" — pause and label it: "
        "\"This is my inner critic speaking.\" Don't immediately investigate whether it's true.",
    },
    {
        "step": "2. Check facts once, briefly",
        "text": "Ask: \"Did I actually behave badly?\" Answer once, plainly (e.g. \"No, I was friendly. "
        "That's enough.\") Then stop — don't reopen the case with \"but maybe my tone...\".",
    },
    {
        "step": "3. Ask the friend question",
        "text": "\"If my best friend had done exactly what I did, would I judge her this harshly?\" "
        "Give yourself the same answer you'd give her.",
    },
    {
        "step": "4. Talk TO the critic, not FROM it",
        "text": "\"I know you're afraid I'll be rejected or disliked. You're trying to protect me. But "
        "attacking me isn't helping. I'm an adult now, and I can handle someone not liking me.\"",
    },
    {
        "step": "5. If you're really hurting",
        "text": "Don't analyse anything. Hand on your chest, breathe slowly: \"I'm hurting right now. "
        "I don't deserve to attack myself. It's okay, I'm here for me.\"",
    },
]

WARNING_SIGNS = [
    "Overthinking or thoughts racing",
    "Sleeping worse than usual",
    "Feeling unusually anxious or low",
    "Feeling more irritable or overwhelmed",
    "Losing interest in things I normally enjoy",
    "Withdrawing from people",
    "Finding it harder to concentrate",
    "Struggling with everyday things",
]

# Tiers keyed by number of signs present, matching the plan sketched in explore.ipynb.
RELAPSE_ACTION_PLAN = {
    "green": {
        "label": "🟢 Doing well",
        "advice": "Normal life — keep going.",
    },
    "yellow": {
        "label": "🟡 Early warning signs",
        "advice": "Reduce stress, prioritize sleep, exercise, talk to your partner.",
    },
    "orange": {
        "label": "🟠 Several warning signs present",
        "advice": "You may be going through a more difficult period. Consider slowing down and doing something that usually helps you stay well.",
    },
    "red": {
        "label": "🔴 Many warning signs present",
        "advice": "Follow your support plan and contact a healthcare professional now — don't wait.",
    },
}

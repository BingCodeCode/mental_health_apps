"""Live From My Head — entry point. Step 1 of the flow: calm down, journal, note one good thing."""
# TODO (known gaps, not yet implemented):
# - Step 2: have an LLM infer the core belief from the written thought instead of manual entry.
# - Step 3: wisdom quotes are now filtered by Step 2's selected categories (plus generic ones);
#   still TODO: have an LLM tailor/pick quotes based on the exact thought text, not just category.
# - Step 4: every thinking-trap category now maps to a practice (only "Other" falls back to the
#   default); revisit if new categories are added later.
# - By design, the app always continues from Step 2 into Steps 3-5 regardless of the recurring
#   checkbox (intentional — not a gap).
# - Warning-sign check-in: signs list is fixed and not yet editable, and there's no trend view
#   over past check-ins (data/checkins.json) to catch signs worsening over time.
from datetime import date

import streamlit as st

from content import (
    CORE_STANCE,
    COURAGE_PRACTICES,
    COURAGE_TO_BE_DISLIKED,
    INNER_CRITIC_PLAN,
    LET_GO_PRACTICES,
    OVERTHINKING_PRACTICES,
    RELAPSE_ACTION_PLAN,
    THINKING_TRAPS,
    WARNING_SIGNS,
    WISDOM_LIBRARY,
)
from storage import (
    delete_custom_wisdom,
    has_had_before,
    load_checkins,
    load_custom_wisdom,
    load_support_plan,
    save_checkin,
    save_custom_wisdom,
    save_entry,
    save_support_plan,
)

st.set_page_config(page_title="Live From My Head", page_icon="🧠")

# Bump up base font size across the whole app — default Streamlit text is too small.
st.markdown(
    """
    <style>
    html, body, [class*="st-"], p, li, label, span, div {
        font-size: 1.15rem !important;
    }
    h1 { font-size: 2.4rem !important; }
    h2 { font-size: 1.9rem !important; }
    h3 { font-size: 1.5rem !important; }
    textarea, input {
        font-size: 1.15rem !important;
    }
    .st-key-start_button button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-color: #2e7d32 !important;
    }
    .st-key-start_button button:hover {
        background-color: #1b5e20 !important;
        border-color: #1b5e20 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "step" not in st.session_state:
    st.session_state.step = "entry"
if "entry" not in st.session_state:
    st.session_state.entry = {}


def go_to(step: str) -> None:
    st.session_state.step = step


def _wisdom_is_generic(category) -> bool:
    """A wisdom entry with no category (None, or an empty list for custom entries) applies to all."""
    if category is None:
        return True
    if isinstance(category, list):
        return len(category) == 0
    return False


def _wisdom_matches(category, categories: list[str]) -> bool:
    if _wisdom_is_generic(category):
        return True
    if isinstance(category, str):
        return category in categories
    return bool(set(category) & set(categories))


if st.session_state.step == "entry":
    st.title("🧠 Live From My Head")
    st.markdown(
        "<p style='font-size:1.4em'>Oh hey, you again — back with something on your mind? "
        "Fine, come on in, no judgment here. Take a breath, write it out, and let it pass "
        "through whenever you're ready.</p>",
        unsafe_allow_html=True,
    )

    if st.button("🚨 Check in on early warning signs"):
        go_to("checkin")
        st.rerun()

    with st.container(key="start_button"):
        if st.button("Start", use_container_width=True):
            go_to("step1")
            st.rerun()

elif st.session_state.step == "checkin":
    st.header("🚨 Early warning sign check-in")
    st.caption(
        "A snapshot of how you're feeling right now — not a verdict on your whole day. Mood "
        "shifts, so check in again whenever it changes."
    )
    st.info("🌱 Reminder: when stressed or overwhelmed, give yourself low demands — doing enough is enough.")

    checked_signs = [sign for sign in WARNING_SIGNS if st.checkbox(sign)]

    if len(checked_signs) == 0:
        tier = "green"
    elif len(checked_signs) <= 2:
        tier = "yellow"
    elif len(checked_signs) <= 4:
        tier = "orange"
    else:
        tier = "red"

    plan = RELAPSE_ACTION_PLAN.get(tier, {"label": "Unknown", "advice": "No advice available."})
    st.subheader(plan["label"])
    st.write(plan["advice"])
    st.caption("This only reflects warning signs — it's fine to feel good things at the same time too.")

    also_good = st.text_input("Anything good also true right now? (optional)")

    if tier in ("orange", "red") and st.button("View my support plan →"):
        go_to("support_plan")
        st.rerun()

    if st.button("Save check-in"):
        save_checkin(checked_signs, tier, also_good)
        st.success("Check-in saved.")

    today_checkins = [c for c in load_checkins() if c["date"].startswith(str(date.today()))]
    if today_checkins:
        tier_order = ["green", "yellow", "orange", "red"]
        today_tiers = [c["tier"] for c in today_checkins if c["tier"] in tier_order]
        if len(set(today_tiers)) > 1:
            best = min(today_tiers, key=tier_order.index)
            worst = max(today_tiers, key=tier_order.index)
            best_label = RELAPSE_ACTION_PLAN.get(best, {}).get("label", best)
            worst_label = RELAPSE_ACTION_PLAN.get(worst, {}).get("label", worst)
            st.caption(f"Today ranged from {best_label} to {worst_label} — both can be true in the same day.")
        with st.expander(f"Today's check-ins ({len(today_checkins)})"):
            for c in reversed(today_checkins):
                line = f"**{c['date']}** — {RELAPSE_ACTION_PLAN.get(c['tier'], {}).get('label', c['tier'])}"
                if c.get("also_good"):
                    line += f" (also good: {c['also_good']})"
                st.write(line)

    if st.button("Back to start"):
        go_to("entry")
        st.rerun()

elif st.session_state.step == "support_plan":
    st.header("📋 My support plan")

    loaded_plan = load_support_plan()
    plan_height = max(250, 25 * (loaded_plan.count("\n") + 1))
    plan_text = st.text_area(
        "My support plan",
        value=loaded_plan,
        height=plan_height,
    )

    if st.button("Save plan"):
        save_support_plan(plan_text)
        st.success("Support plan saved.")

    if st.button("Back"):
        go_to("checkin")
        st.rerun()

elif st.session_state.step == "step1":
    st.header("Step 1: Calm down & feel, then journal")

    st.write(
        "Before anything else, take a moment to slow down and notice what you're feeling "
        "in your body/mind — a few slow breaths."
    )
    if st.button("I've taken a breath"):
        st.balloons()
        st.success("💚 Nice. That's already something — well done.")

    st.subheader("Journal (optional)")
    journal_text = st.text_area(
        "Write freely about what you feel and what you're thinking right now.",
        value=st.session_state.entry.get("journal_text", ""),
        height=200,
    )

    st.subheader("One good thing")
    good_thing = st.text_input(
        "Note one good thing or something that made you happy today — doesn't have to be big.",
        value=st.session_state.entry.get("good_thing", ""),
    )

    if st.button("Continue"):
        st.session_state.entry["journal_text"] = journal_text
        st.session_state.entry["good_thing"] = good_thing
        go_to("step2")
        st.rerun()

elif st.session_state.step == "step2":
    st.header("Step 2: Thought tree & thinking traps")

    st.caption(
        "Write it down, don't hold back — dump your thoughts, no matter how bad or scary they "
        "are. Write the most real and cruel thought you have, exactly as it is."
    )
    thought_text = st.text_area(
        "I am aware that I have a thought that ___",
        value=st.session_state.entry.get("thought_text", ""),
        height=350,
    )

    if thought_text.strip():
        is_fact = st.radio("Is this a thought or a fact?", ["Thought", "Fact"], horizontal=True)

        if is_fact == "Fact":
            st.info("Just to close: in most cases, it is not a fact.")
            if st.button("Continue"):
                st.session_state.entry["thought_text"] = thought_text
                st.session_state.entry["is_fact"] = True
                save_entry(dict(st.session_state.entry))
                st.success("Saved. Since you marked this as a fact, there's nothing more to walk through here.")
        else:
            st.caption(
                "A thought is just a thought, not a fact. It could be wrong — very wrong. "
                "You have been so wrong before. It feeling very true doesn't necessarily mean "
                "it is a fact."
            )

            categories = st.multiselect(
                "Categorize the thought (pick one or more):",
                [t["name"] for t in THINKING_TRAPS],
            )
            for name in categories:
                trap = next(t for t in THINKING_TRAPS if t["name"] == name)
                st.caption(f"**{name}** — {trap['description']}")

            with st.expander("Optional: what core belief does this point to?"):
                st.caption("🤖 TODO: have an LLM infer the core belief from the written thought.")
                core_belief = st.text_input(
                    "e.g. \"I'm not good enough\", \"I'm unlovable\", \"I'm not safe/in control\""
                )

            suggested_recurring = has_had_before(categories)
            recurring = st.checkbox(
                "Have I had this thought before?",
                value=suggested_recurring,
            )

            if recurring:
                st.markdown(
                    "<p style='font-size:1.6em; line-height:1.5;'>"
                    "Aha, you again, my old best friend. Welcome back to me again. "
                    "I have had you before, maybe many times.<br><br>"
                    "Don't push it away. Let it sit beside me. Tell it: \"you can be here.\" "
                    "Don't engage, don't play tennis — sit side by side, peacefully.<br><br>"
                    "<b>Pause. Breathe. Notice what I'm feeling.</b>"
                    "</p>",
                    unsafe_allow_html=True,
                )
                st.caption(
                    "Why not engage: the more you think a thought, the deeper the neural pathway "
                    "it carves — so engaging/playing tennis with it only traps you deeper. To stop "
                    "it from getting deeper, stop repeating the path. Let it sit beside you instead "
                    "of running it again."
                )

            if st.button("Continue", key="step2_continue", disabled=not categories):
                st.session_state.entry["thought_text"] = thought_text
                st.session_state.entry["is_fact"] = False
                st.session_state.entry["category"] = categories
                st.session_state.entry["core_belief"] = core_belief
                st.session_state.entry["recurring"] = recurring
                go_to("step3")
                st.rerun()

elif st.session_state.step == "step3":
    st.header("Step 3: Wisdom library")

    st.caption("You've been here before. This is what you learned last time.")
    st.caption("🤖 TODO: have an LLM pick/tailor quotes to the exact thought text, not just the category.")

    categories = st.session_state.entry.get("category") or []
    if isinstance(categories, str):  # backward compatibility with older single-category entries
        categories = [categories]

    # Seeded content first, then the reader's own added truths — category-specific before generic.
    relevant_quotes = [
        {**entry, "is_custom": False}
        for entry in WISDOM_LIBRARY
        if _wisdom_matches(entry["category"], categories)
    ]
    relevant_quotes += [
        {**entry, "is_custom": True, "custom_index": idx}
        for idx, entry in enumerate(load_custom_wisdom())
        if _wisdom_matches(entry["category"], categories)
    ]
    relevant_quotes.sort(key=lambda entry: _wisdom_is_generic(entry["category"]))

    quotes_by_source: dict[str, list[dict]] = {}
    for entry in relevant_quotes:
        quotes_by_source.setdefault(entry["source"], []).append(entry)

    for source, group in quotes_by_source.items():
        st.markdown(f"**{source}:**")
        for entry in group:
            st.markdown(f"> \"{entry['text']}\"")
            if entry["is_custom"]:
                if st.button("🗑️ Remove", key=f"del_custom_wisdom_{entry['custom_index']}"):
                    delete_custom_wisdom(entry["custom_index"])
                    st.rerun()

    with st.expander("➕ Add your own truth"):
        st.caption(
            "Write your own reminder/realization to add to the library. Leave categories empty "
            "to have it show up for every thought, or pick the thinking traps it applies to."
        )
        new_truth_text = st.text_area("My truth", key="new_truth_text", height=100)
        new_truth_categories = st.multiselect(
            "Applies to (optional — leave empty for general):",
            [t["name"] for t in THINKING_TRAPS],
            key="new_truth_categories",
        )
        new_truth_source_type = st.radio(
            "Source",
            ["My own truths", "From a book"],
            horizontal=True,
            key="new_truth_source_type",
        )
        if new_truth_source_type == "From a book":
            new_truth_book = st.text_input(
                "Book title / author (optional)", key="new_truth_book"
            )
            new_truth_source = f"From books — {new_truth_book.strip()}" if new_truth_book.strip() else "From books"
        else:
            new_truth_source = "My own truths"
        if st.button("Save truth", disabled=not new_truth_text.strip()):
            save_custom_wisdom(new_truth_text.strip(), new_truth_categories, new_truth_source)
            del st.session_state["new_truth_text"]
            del st.session_state["new_truth_categories"]
            del st.session_state["new_truth_source_type"]
            if "new_truth_book" in st.session_state:
                del st.session_state["new_truth_book"]
            st.toast("Added to your wisdom library.")
            st.rerun()

    if st.button("Continue", key="step3_continue"):
        go_to("step4")
        st.rerun()

elif st.session_state.step == "step4":
    st.header("Step 4: Apply a targeted practice")

    categories = st.session_state.entry.get("category") or []
    if isinstance(categories, str):  # backward compatibility with older single-category entries
        categories = [categories]

    let_go_categories = {"Fortune Telling", "Catastrophizing", "Should Statements", "Personalization"}
    overthinking_categories = {
        "All-or-Nothing Thinking",
        "Overgeneralization",
        "Mental Filter",
        "Discounting the Positive",
        "Emotional Reasoning",
        "Labeling",
    }

    shown_any = False

    if "Mind Reading" in categories:
        shown_any = True
        st.subheader("🦁 Courage to be disliked")
        for item in COURAGE_TO_BE_DISLIKED:
            st.write(f"- {item}")
        st.subheader("🎯 Practice: don't please, dare to be you")
        for item in COURAGE_PRACTICES:
            st.write(f"- {item}")

    if "Inner Critic" in categories:
        shown_any = True
        st.subheader("🗣️ Inner-critic plan")
        st.caption("Not to destroy the critic — to recognize it, stop treating it as an authority, and respond with kindness.")
        for item in INNER_CRITIC_PLAN:
            st.markdown(f"**{item['step']}**")
            st.write(item["text"])

    # The "let it sit, don't engage" stance only fits the let-go/overthinking practices below —
    # it would contradict the active-engagement advice in Courage/Inner-critic above.
    if let_go_categories.intersection(categories) or overthinking_categories.intersection(categories):
        st.markdown(f"*{CORE_STANCE}*")

    if let_go_categories.intersection(categories):
        shown_any = True
        st.subheader("🌀 Let go / surrender")
        for item in LET_GO_PRACTICES:
            st.write(f"- {item}")

    if overthinking_categories.intersection(categories):
        shown_any = True
        st.subheader("🌀 Overthinking: let the automatic thought pass")
        for item in OVERTHINKING_PRACTICES:
            st.write(f"- {item}")

    if not shown_any:
        st.subheader("🦁 Courage to be disliked")
        st.caption("Defaulting here since this is usually your pattern — thoughts about what others think of you.")
        for item in COURAGE_TO_BE_DISLIKED:
            st.write(f"- {item}")
        st.subheader("🎯 Practice: don't please, dare to be you")
        for item in COURAGE_PRACTICES:
            st.write(f"- {item}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="step4_back"):
            go_to("step3")
            st.rerun()
    with col2:
        if st.button("Continue", key="step4_continue"):
            st.session_state.step5_submitted = False
            go_to("step5")
            st.rerun()

elif st.session_state.step == "step5":
    if st.session_state.get("finished"):
        st.success("💗 Saved. You showed up for yourself today — that's enough.")
        if st.button("Close for now 🌙"):
            st.session_state.finished = False
            go_to("entry")
            st.rerun()
    else:
        st.header("💗 Step 5: Be kind to yourself")

        st.caption(
            "You tend to criticize yourself a lot, often without even noticing. This last bit isn't "
            "another technique — it's a deliberate pause to catch that before it runs unchecked."
        )
        st.markdown(
            "<p style='font-size:1.3em'>🌱 The critic is learned — it's not you. You weren't born "
            "with it: at six years old, you didn't have this self-critic at all. It got added later, "
            "which means it isn't a fixed, fundamental part of who you are. It can be unlearned too.</p>",
            unsafe_allow_html=True,
        )

        categories = st.session_state.entry.get("category") or []
        if isinstance(categories, str):  # backward compatibility with older single-category entries
            categories = [categories]

        if "Inner Critic" in categories:
            st.info(
                "🫶 Hand on your chest, breathe slowly: \"I'm hurting right now. I don't deserve to "
                "attack myself. It's okay, I'm here for me.\""
            )

        st.subheader("The friend question")
        st.caption("If a friend told you this exact thought, what would you say back to them?")

        if not st.session_state.get("step5_submitted"):
            friend_reply = st.text_area(
                "What would I say to a friend who had this exact thought?",
                value=st.session_state.entry.get("friend_reply", ""),
                height=120,
            )
            if st.button("Here is what I'd say to a friend", disabled=not friend_reply.strip()):
                st.session_state.entry["friend_reply"] = friend_reply
                st.session_state.step5_submitted = True
                st.rerun()
        else:
            friend_reply = st.session_state.entry.get("friend_reply", "")
            st.markdown(
                f"<p style='font-size:1.2em'><b>Now say that to yourself:</b><br>\"{friend_reply}\"</p>",
                unsafe_allow_html=True,
            )
            if st.button("I'm done for now"):
                save_entry(dict(st.session_state.entry))
                st.session_state.entry = {}
                st.session_state.step5_submitted = False
                st.session_state.finished = True
                st.rerun()

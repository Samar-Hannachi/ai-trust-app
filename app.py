# final_app.py
import os
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

# -----------------------------
# Prolific integration helpers
# -----------------------------
def get_prolific_pid() -> str:
    # Read PROLIFIC_PID from the URL, fallback to typed ID field later
    params = st.experimental_get_query_params()
    return params.get("PROLIFIC_PID", [""])[0]

PROLIFIC_COMPLETION_URL = "https://app.prolific.com/submissions/complete?cc=REPLACE_WITH_YOUR_CODE"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "responses.csv")

# -----------------------------
# Page & Global UI
# -----------------------------
st.set_page_config(
    page_title="Trust Dynamics Survey",
    page_icon="🧪",
    layout="wide",
)

# Minimal CSS for "cards"
st.markdown(
    """
    <style>
      .app-container {max-width: 1100px; margin: 0 auto;}
      .card {border: 1px solid rgba(0,0,0,0.08); border-radius: 14px; padding: 18px 20px;
             background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom: 18px;}
      .muted {color: rgba(0,0,0,0.6); font-size: 0.95rem;}
      .pill {display:inline-block; padding:4px 10px; border-radius:999px; border:1px solid rgba(0,0,0,0.1);
             margin-right:6px; margin-bottom:6px; font-size:0.9rem;}
      .ok {background:#E8F5E9; border-color:#C8E6C9;}
      .warn {background:#FFF3E0; border-color:#FFE0B2;}
      .sep {height: 8px;}
      .levels-grid {display:grid; grid-template-columns: 80px 1fr; gap:10px; align-items:start;}
      .level-badge {font-weight:600; background:#F7FAFC; border:1px solid #EDF2F7;
                    border-radius:10px; text-align:center; padding:6px 8px;}
      .sticky-submit {position: sticky; bottom: 0; padding: 10px 0;
                      background: linear-gradient(180deg, rgba(255,255,255,0), #ffffff 40%);}
      .stSlider, .stRadio {margin-top: -8px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
def card(title: str, subtitle: str | None = None):
    c = st.container()
    with c:
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {title}")
        if subtitle:
            st.markdown(f"<div class='muted'>{subtitle}</div>", unsafe_allow_html=True)
    return c

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)

def get_simulated_response(user_input, tone):
    tone_map = {
        "Empathetic": "I understand how you feel. Here's a gentle and understanding answer:",
        "Neutral": "Here is a balanced, factual response:",
        "Authoritative": "This is a confident and firm answer to your question:"
    }
    return f"[{tone} Tone] {tone_map[tone]} '{user_input}'"

def init_state():
    if "used_tones" not in st.session_state:
        st.session_state.used_tones = {}  # scenario_index -> list of tones used
    if "scenario_done" not in st.session_state:
        st.session_state.scenario_done = {}  # scenario_index -> bool
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

init_state()

# -----------------------------
# Sidebar: Progress overview
# -----------------------------
with st.sidebar:
    st.header("🧭 Survey Progress")
    steps = ["Consent", "Demographics", "Comfort", "Scenarios", "Submit"]
    consent_ok = st.session_state.get("consent_ok", False)
    demo_ok = st.session_state.get("demo_ok", False)
    comfort_set = st.session_state.get("comfort_set", False)
    scenarios_done_count = sum(1 for v in st.session_state.scenario_done.values() if v)
    total_scenarios = 3
    scenarios_ok = scenarios_done_count == total_scenarios

    statuses = [
        ("Consent", consent_ok),
        ("Demographics", demo_ok),
        ("Comfort", comfort_set),
        (f"Scenarios ({scenarios_done_count}/{total_scenarios})", scenarios_ok),
        ("Submit", False),
    ]
    for label, ok in statuses:
        st.markdown(
            f"<span class='pill {'ok' if ok else 'warn'}'>{'✅' if ok else '⏳'} {label}</span>",
            unsafe_allow_html=True,
        )

st.title("Trust in AI — Interactive Survey")
st.markdown("<div class='app-container'>", unsafe_allow_html=True)

# -----------------------------
# CONSENT
# -----------------------------
c = card("Consent Form", "Please review and agree to continue.")
with c:
    with st.expander("Read the consent information", expanded=True):
        st.write(
            """
Welcome to the Trust in AI study. This survey is part of an academic research project aiming to understand how individuals interact with and trust AI systems in medical contexts.

Your participation is voluntary, and your responses will remain anonymous. You may withdraw at any time. The data collected will be used for research purposes only.

**Important:** Only reformulated answers will be accepted. Direct copy-pastes of the questions will be rejected.
            """
        )
    consent_given = st.checkbox("I have read the above information and I consent to participate in this study.")
    if not consent_given:
        st.warning("You must provide consent to continue.")
    st.session_state.consent_ok = bool(consent_given)
end_card()

if not consent_given:
    st.stop()

# -----------------------------
# DEMOGRAPHICS
# -----------------------------
c = card("Demographic Information", "Please provide the following information before beginning the scenarios.")
with c:
    col1, col2 = st.columns([1, 1])
    with col1:
        typed_prolific_id = st.text_input("Prolific ID (if not auto-filled from Prolific)")
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
        gender = st.selectbox(
            "Gender",
            [
                "Woman", "Man", "Trans-woman", "Trans-man", "Gender fluid", "Agender",
                "Androgynous", "Bi-gender", "Non-binary", "Demi-man", "Demi-woman",
                "Genderqueer", "Gender non conforming", "Tri-gender", "All genders",
                "In the middle of woman and man", "Intersex", "Not sure", "Rather not say", "Other"
            ]
        )
    with col2:
        education = st.selectbox(
            "Highest level of education",
            [
                "No schooling completed", "Some high school, no diploma",
                "High school graduate (or equivalent)",
                "Some college credit, no degree",
                "Associate degree", "Bachelor's degree", "Master's degree",
                "Doctorate degree", "Other"
            ]
        )
        occupation = st.selectbox(
            "Occupation",
            ["Self-employed", "Unemployed", "Employed for wages", "Student", "Homemaker", "Military", "Retired", "Unable to work", "Other"]
        )
        residence = st.selectbox(
            "Country/Region of residence",
            ["North America", "South America", "Europe", "Asia", "Africa", "Antarctica", "Australia", "Oceania"]
        )
        birth_country = st.selectbox(
            "Country/Region of birth",
            ["North America", "South America", "Europe", "Asia", "Africa", "Antarctica", "Australia", "Oceania"]
        )
    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)
    ai_familiarity = st.radio("Background/familiarity with AI", ["None", "Basic", "Intermediate", "Expert"], horizontal=True)

    # Prefer PID from URL; fallback to typed field
    prolific_pid = get_prolific_pid() or typed_prolific_id

    demo_ok = (
        (prolific_pid or "").strip() != "" and
        age is not None and
        gender is not None and
        education is not None and
        occupation is not None and
        residence is not None and
        birth_country is not None and
        ai_familiarity is not None
    )
    st.session_state.demo_ok = bool(demo_ok)
end_card()

# -----------------------------
# COMFORT LEVEL
# -----------------------------
c = card("Comfort With AI Diagnosis")
with c:
    st.write("How comfortable would you be receiving a healthcare diagnosis from an AI system?")
    comfort_level = st.slider("Comfort Level (0 = Not at all comfortable, 5 = Very comfortable)", 0, 5, key="comfort_level")
    st.session_state.comfort_set = True
end_card()

# -----------------------------
# AI AUTONOMY LEVELS
# -----------------------------
c = card("Levels of Autonomous Medical Consultation", "A progressive overview of AI involvement in care.")
with c:
    st.write("This table outlines the progressive integration of AI into medical interventions, from no AI to full automation.")
    levels = [
        ("Level 0", "No AI use; physician in charge (human doctor)."),
        ("Level 1", "AI consultation assistance (no automation); physician in charge (human doctor)."),
        ("Level 2", "Partial AI consultation automation; physician in charge (human doctor) with AI assistance."),
        ("Level 3", "Conditional AI consultation automation; AI doctor with human oversight."),
        ("Level 4", "Advanced AI consultation automation; AI doctor with human oversight."),
        ("Level 5", "Full AI consultation automation; AI doctor.")
    ]
    for lvl, desc in levels:
        colA, colB = st.columns([0.25, 1.75])
        with colA:
            st.markdown(f"<div class='level-badge'>{lvl}</div>", unsafe_allow_html=True)
        with colB:
            st.write(desc)
end_card()

# -----------------------------
# SCENARIOS
# -----------------------------
scenarios = [
    "Your mother, 60 years old, has been trying to manage her diabetes with dietary changes and metformin. However, she is struggling with frequent high blood sugar readings. During her visit with her doctor, she feels overwhelmed by medical jargon and does not fully understand her treatment plan.",
    "Your grandfather, 80 years old, slips in a puddle and breaks his hip. After his visit to the doctor, he still suffers a lot from his situation.",
    "You notice a change in your 20-year-old brother’s behavior. He is becoming less talkative and isolating from friends and family, and withdrawing from his usual physical activities. He seems to be displaying symptoms of depression."
]
tones_all = ["Empathetic", "Neutral", "Authoritative"]

c = card("Scenario Exercises", "Engage with each scenario below. Try all three AI tones per scenario.")
with c:
    for i, scenario in enumerate(scenarios):
        st.markdown(f"#### Scenario {i+1}")
        st.write(scenario)

        user_input = st.text_input(f"What would you ask the AI for Scenario {i+1}?", key=f"input_{i}")
        used = st.session_state.used_tones.get(i, [])
        remaining = [t for t in tones_all if t not in used]

        col1, col2 = st.columns([1, 1])
        with col1:
            if user_input:
                tone_choice = st.radio(
                    "Choose the tone for the AI response",
                    remaining if remaining else tones_all,
                    horizontal=True,
                    key=f"tone_{i}",
                    disabled=(len(remaining) == 0)
                )
            else:
                tone_choice = None
        with col2:
            can_generate = bool(user_input and tone_choice and (tone_choice in remaining))
            generate = st.button(
                f"Generate {tone_choice or '…'} Response",
                key=f"generate_{i}",
                disabled=not can_generate
            )

        if generate and can_generate:
            answer = get_simulated_response(user_input, tone_choice)
            st.text_area(f"{tone_choice} Response", answer, height=150, key=f"response_{tone_choice}_{i}")
            _ = st.radio(
                "How much do you trust this AI response?",
                ["Low", "Moderate", "High"],
                key=f"trust_{tone_choice}_{i}",
                horizontal=True,
            )
            used.append(tone_choice)
            st.session_state.used_tones[i] = used

        if user_input and len(used) >= 3:
            st.session_state.scenario_done[i] = True
            st.success("✅ You've tested all tones for this scenario. Move on to the next.")
        elif user_input and len(used) > 0:
            st.info(f"Progress: {len(used)}/3 tones tried for this scenario.")
end_card()

# -----------------------------
# SUBMISSION (SAVE TO CSV)
# -----------------------------
all_answered = (
    st.session_state.consent_ok and
    st.session_state.demo_ok and
    st.session_state.comfort_set and
    all(st.session_state.scenario_done.get(i, False) for i in range(len(scenarios)))
)

def build_record():
    """Collect all answers into a flat dict for CSV storage."""
    record = {
        "timestamp_iso": datetime.utcnow().isoformat(),
        "session_id": st.session_state.session_id,
        "prolific_pid": prolific_pid,
        "age": age,
        "gender": gender,
        "education": education,
        "occupation": occupation,
        "residence": residence,
        "birth_country": birth_country,
        "ai_familiarity": ai_familiarity,
        "comfort_level": st.session_state.get("comfort_level"),
    }

    # Scenario-specific fields
    for i in range(len(scenarios)):
        q = st.session_state.get(f"input_{i}", "")
        record[f"scenario_{i+1}_question"] = q

        # For each tone, save generated response (simulated) and trust rating if present
        for tone in tones_all:
            resp_key = f"response_{tone}_{i}"
            trust_key = f"trust_{tone}_{i}"
            record[f"scenario_{i+1}_{tone}_response"] = st.session_state.get(resp_key, "")
            record[f"scenario_{i+1}_{tone}_trust"] = st.session_state.get(trust_key, "")

        # Save which tones were actually used
        used = st.session_state.used_tones.get(i, [])
        record[f"scenario_{i+1}_tones_used"] = "|".join(used)

    return record

def append_to_csv(row_dict: dict, csv_path: str):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_row = pd.DataFrame([row_dict])
    header = not os.path.exists(csv_path)
    df_row.to_csv(csv_path, mode="a", header=header, index=False, encoding="utf-8")

with st.container():
    st.markdown("<div class='sticky-submit'>", unsafe_allow_html=True)
    colL, colR = st.columns([5, 2])
    with colL:
        if all_answered:
            if st.button("Submit Survey ✅", use_container_width=True):
                record = build_record()
                append_to_csv(record, CSV_PATH)
                st.success("Thank you for your participation! Your responses have been recorded.")
                st.info(f"If you are on Prolific, please **complete your submission**: {PROLIFIC_COMPLETION_URL}")
                st.caption(f"Saved to: {CSV_PATH}")
        else:
            if st.button("Submit Survey", use_container_width=True):
                st.error("Please complete all required sections before submitting.")
            st.caption("Complete all scenarios and fields above to enable submission.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

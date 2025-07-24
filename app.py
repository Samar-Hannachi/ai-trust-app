# final_app.py
import streamlit as st
# UI Setup
st.set_page_config(page_title="Trust Dynamics Survey")
st.title("Trust in AI — Interactive Survey")
# --- Consent Section ---
st.header("Consent Form")
st.write("""
Welcome to the Trust in AI study. This survey is part of an academic research project aiming to understand how individuals interact with and trust AI systems in medical contexts.

Your participation is voluntary, and your responses will remain anonymous. You may withdraw at any time. The data collected will be used for research purposes only.
         
Only reformulated answers will be accepted - Any copy paste of the questions will be rejected.
""")
consent_given = st.checkbox("I have read the above information and I consent to participate in this study.")

if not consent_given:
    st.warning("You must provide consent to continue.")
    st.stop()
# Simulated AI response function (replace with OpenAI when quota is available)
def get_simulated_response(user_input, tone):
    tone_map = {
        "Empathetic": "I understand how you feel. Here's a gentle and understanding answer:",
        "Neutral": "Here is a balanced, factual response:",
        "Authoritative": "This is a confident and firm answer to your question:"
    }
    return f"[{tone} Tone] {tone_map[tone]} '{user_input}'"
# --- Demographics Section ---
st.header("Demographic Information")
st.write("Please provide the following information before beginning the scenarios.")
name = st.text_input("Enter your Prolific ID")
age = st.number_input("Your Age", min_value=10, max_value=100, step=1)
gender = st.selectbox("Gender", ["Woman", "Man", "Trans-woman", "Trans-man", "Gender fluid", "Agender", "Androgynous", "Bi-gender", "Non-binary", "Demi-man", "Demi-woman", "Genderqueer", "Gender non conforming", "Tri-gender", "All genders", "In the middle of woman and man", "Intersex", "Not sure", "Rather not say", "Other"])
education = st.selectbox("Highest Level of Education", ["No schooling completed", "Some high-school, No diploma", "High school graduate, diploma or the equivalent", "Some college credit, no credit", "Associate degree", "Bachelor's degree", "Master's degree", "Doctorate degree", "Other"])
occupation = st.selectbox("Occupation",["Self-employed", "Unemployed", "Employed for wages", "Student", "Homemaker", "Military", "Retired", "Unable to work", "Other"])
residence = st.selectbox("Country of residence",["North America", "South America", "Europe", "Asia", "Africa", "Antarctica", "Australia", "Oceania"])
live = st.selectbox("Coutry of birth",["North America", "South America", "Europe", "Asia", "Africa", "Antarctica", "Australia", "Oceania"])

st.markdown("---")

ai_familiarity = st.radio("What is your background or familiarity with AI?", ["None", "Basic", "Intermediate", "Expert"])

st.markdown("---")
st.subheader("Levels of Autonomous Medical Consultation")
st.write("This table outlines the progressive integration of AI into medical interventions. We delineate six stages, each representing a gradual increase in the extent to which AI contributes to the medical procedures employed.")

st.markdown("""
0. **Level 0** – No AI use; physician subject : human doctor.  
1. **Level 1** – AI consultation assistance (no automation); physician subject : human doctor.  
2. **Level 2** – Partial AI consultation automation; physician subject : human doctor with AI assistance.  
3. **Level 3** – Conditional AI consultation automation; physician subject : AI doctor with human assistance.  
4. **Level 4** – Advanced AI consultation automation; physician subject : AI doctor with human assistance.  
5. **Level 5** – Full AI consultation automation; physician subject : AI doctor.
""")
st.subheader("How comfortable would you be receiving a healthcare diagnosis from an AI system?")
comfort_level = st.slider("Comfort Level (0 = Not at all comfortable, 5 = Very comfortable)", 0, 5)

st.markdown("---")
st.write("Please engage with each scenario below and provide your thoughts. Once you have engaged with each AI tone, you will receive this message : ✅ You've tested all tones for this scenario. Move on to the next.")

# Scenario definitions
scenarios = [
    "Your mother, 60 years-old, has been trying to manage her diabetes with dietary changes and metformin. However, she is struggling with frequent high blood sugar readings. During her visit with her doctor, she feels overwhelmed with all the medical jargon and does not fully understand her treatment plan.",
    "Your grandfather, 80-years-old, slips in a puddle and breaks his hip bone. After his visit to the doctor, he still suffers a lot from his situation.",
    "You are witnessing a change in your brother's behavior who is 20 years-old. He is becoming less talkative and isolating from his friends and family members. He is also withdrawing from his usual physical activities. He is obviously displaying symptoms of depression."
]

# Loop through scenarios
for i, scenario in enumerate(scenarios):
    st.subheader(f"Scenario {i+1}")
    st.write(scenario)

    user_input = st.text_input(f"What would you ask the AI for Scenario {i+1}?", key=f"input_{i}")
    used_tones = st.session_state.get(f"used_tones_{i}", [])
    remaining_tones = [tone for tone in ["Empathetic", "Neutral", "Authoritative"] if tone not in used_tones]

    if user_input and remaining_tones:
        selected_tone = st.selectbox("Choose the tone for the AI response:", remaining_tones, key=f"tone_select_{i}")
        if st.button(f"Generate {selected_tone} Response", key=f"generate_{i}"):
            answer = get_simulated_response(user_input, selected_tone)
            st.text_area(f"{selected_tone} Response", answer, height=150, key=f"response_{selected_tone}_{i}")
            trust = st.radio("How much do you trust this AI response?", ["Low", "Moderate", "High"], key=f"trust_{selected_tone}_{i}")
            used_tones.append(selected_tone)
            st.session_state[f"used_tones_{i}"] = used_tones
    elif user_input:
        st.info("✅ You've tested all tones for this scenario. Move on to the next.")

if st.button("Submit responses"):
    # Save results
    st.success("✅ Thank you for your participation!")

import streamlit as st
#import openai
import csv
from datetime import datetime
from openai import OpenAI
#client = OpenAI()
# SETUP
st.set_page_config(page_title="Trust in AI", layout="centered")
#openai.api_key = "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"  # Replace with your actual key

# PAGE TITLE
st.title("Trust in AI – Survey")

# --- CONSENT & DEMOGRAPHICS ---
with st.form("user_form"):
    name = st.text_input("Name (optional)")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["", "Female", "Male", "Other"])
    background = st.text_area("Your familiarity with AI?")
    submitted = st.form_submit_button("Start Interaction")

# --- AI INTERACTION ---
if submitted:
    st.session_state['user_info'] = {
        "name": name,
        "age": age,
        "gender": gender,
        "background": background,
        "timestamp": str(datetime.now())
    }

    st.success("Survey started. Scroll down to interact with the AI.")

if 'user_info' in st.session_state:
    st.header("🧠 AI Interaction")
    persona = st.selectbox("Choose an AI Persona", ["Clinical", "Friendly", "Cautious"])
    user_input = st.text_input("Ask a question to the AI")

    if st.button("Ask"):
        system_prompt = f"You are a {persona} medical AI assistant responding to user queries."
        with st.spinner("AI is thinking..."):
            try:
                #client = OpenAI()
                # Simulated AI response while quota is exceeded
                answer = f"[Simulated {persona} response] Based on your question: '{user_input}', here's a typical answer..."
                st.warning("You are in development mode – OpenAI responses are simulated.")


                #response = client.chat.completions.create(
                    #model="gpt-4o",
                    #messages=[
                        #{"role": "system", "content": system_prompt},
                        #{"role": "user", "content": user_input}
                    #]
                #)

                #answer = response.choices[0].message.content
                st.write("AI Response:", answer)
                st.session_state['last_response'] = answer
                st.session_state['last_question'] = user_input
            except Exception as e:
                st.error(f"OpenAI error: {e}")

# --- TRUST RATING ---
    if 'last_response' in st.session_state:
        st.subheader("📝 Rate the AI Response")

        trust = st.slider("How much do you trust this response?", 1, 5, 3)
        clarity = st.slider("How clear was the response?", 1, 5, 3)
        safety = st.slider("How safe did the response feel?", 1, 5, 3)

        if st.button("Submit Response"):
            row = {
                **st.session_state['user_info'],
                "persona": persona,
                "question": st.session_state['last_question'],
                "response": st.session_state['last_response'],
                "trust": trust,
                "clarity": clarity,
                "safety": safety
            }

            with open("survey_results.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=row.keys())
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(row)

            st.success("Your response has been recorded. Thank you!")


import streamlit as st
import csv
from datetime import datetime
import openai

openai.api_key = "YOUR_API_KEY"

def ask_llm(prompt, persona):
    system_msg = {"role": "system", "content": f"You are a {persona} AI."}
    user_msg = {"role": "user", "content": prompt}
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[system_msg, user_msg]
    )
    return response.choices[0].message.content

st.title("Trust Dynamics Survey")

if "step" not in st.session_state:
    st.session_state.step = 0

if st.session_state.step == 0:
    st.write("Consent and Demographics")
    name = st.text_input("Name (optional)")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["", "Female", "Male", "Other"])
    if st.button("Next"):
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.step = 1

elif st.session_state.step == 1:
    st.write("Interact with the AI")
    persona = st.selectbox("Select AI Persona", ["Clinical", "Friendly", "Cautious"])
    prompt = st.text_input("Ask your question:")
    if st.button("Submit Question"):
        response = ask_llm(prompt, persona)
        st.write("AI Response:", response)

        trust = st.slider("Trust?", 1, 5, 3)
        clarity = st.slider("Clarity?", 1, 5, 3)
        safety = st.slider("Safety?", 1, 5, 3)

        with open("trust_logs.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([
                st.session_state.name, st.session_state.age, st.session_state.gender,
                persona, prompt, response, trust, clarity, safety,
                datetime.now().isoformat()
            ])
        st.success("Response logged!")

    if st.button("Finish Survey"):
        st.session_state.step = 2

elif st.session_state.step == 2:
    st.write("Thank you for participating!")

import streamlit as st
import openai
import csv
from datetime import datetime

# Set your OpenAI API key
openai.api_key = "your-api-key-here"

# Initialize step
if "step" not in st.session_state:
    st.session_state.step = 0
if st.session_state.step == 0:
    st.title("Trust in AI – Consent & Demographics")

    st.write("Please answer the following questions to participate in the study.")

    name = st.text_input("Your Name (or leave blank for anonymous)")
    age = st.text_input("Your Age")
    gender = st.selectbox("Gender", ["Select", "Female", "Male", "Other"])
    background = st.text_input("What is your background or familiarity with AI?")

    consent = st.checkbox("I consent to participate in this study")

    if consent and st.button("Continue to AI Interaction"):
        st.session_state["name"] = name
        st.session_state["age"] = age
        st.session_state["gender"] = gender
        st.session_state["background"] = background
        st.session_state.step = 1
elif st.session_state.step == 1:
    st.title("Chat with the AI")

    persona = st.selectbox("Select AI Persona", ["Clinical", "Friendly", "Cautious", "Empathic"])
    user_input = st.text_input("Ask your question")

    if st.button("Send"):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a {persona} AI."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_reply = response.choices[0].message["content"]
        st.markdown(f"**AI Response:** {ai_reply}")

        trust = st.slider("How much do you trust this answer?", 1, 5, 3)
        clarity = st.slider("How clear was this answer?", 1, 5, 3)
        safety = st.slider("How safe do you feel using this answer?", 1, 5, 3)

        with open("trust_logs.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([
                st.session_state.name,
                st.session_state.age,
                st.session_state.gender,
                st.session_state.background,
                persona,
                user_input,
                ai_reply,
                trust,
                clarity,
                safety,
                datetime.now().isoformat()
            ])

    if st.button("Finish Survey"):
        st.session_state.step = 2
elif st.session_state.step == 2:
    st.title("Post-Interaction Questions")

    overall_trust = st.slider("Overall, how much do you trust this AI?", 1, 5, 3)
    would_use = st.radio("Would you use this AI in real life?", ["Yes", "No", "Not sure"])
    feedback = st.text_area("Any comments or feedback?")

    if st.button("Submit Final Response"):
        with open("trust_logs.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([
                st.session_state.name,
                "FINAL",
                "",
                "",
                "",
                "",
                "",
                overall_trust,
                would_use,
                feedback,
                datetime.now().isoformat()
            ])
        st.success("Thank you for participating!")
        st.balloons()

{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Defaulting to user installation because normal site-packages is not writeable\n",
      "Requirement already satisfied: streamlit in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (1.45.1)\n",
      "Requirement already satisfied: pyarrow>=7.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (20.0.0)\n",
      "Requirement already satisfied: pandas<3,>=1.4.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (2.2.3)\n",
      "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (3.1.44)\n",
      "Requirement already satisfied: tenacity<10,>=8.1.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (9.1.2)\n",
      "Requirement already satisfied: toml<2,>=0.10.1 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: requests<3,>=2.27 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (2.32.3)\n",
      "Requirement already satisfied: tornado<7,>=6.0.3 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (6.4.2)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.4.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (4.12.2)\n",
      "Requirement already satisfied: blinker<2,>=1.5.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (1.9.0)\n",
      "Requirement already satisfied: click<9,>=7.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (8.1.7)\n",
      "Requirement already satisfied: pillow<12,>=7.1.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (11.0.0)\n",
      "Requirement already satisfied: protobuf<7,>=3.20 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (6.31.1)\n",
      "Requirement already satisfied: pydeck<1,>=0.8.0b4 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (0.9.1)\n",
      "Requirement already satisfied: altair<6,>=4.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (5.5.0)\n",
      "Requirement already satisfied: packaging<25,>=20 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (24.2)\n",
      "Requirement already satisfied: cachetools<6,>=4.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (5.5.2)\n",
      "Requirement already satisfied: numpy<3,>=1.23 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from streamlit) (2.0.2)\n",
      "Requirement already satisfied: jinja2 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from altair<6,>=4.0->streamlit) (3.1.4)\n",
      "Requirement already satisfied: narwhals>=1.14.2 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from altair<6,>=4.0->streamlit) (1.41.0)\n",
      "Requirement already satisfied: jsonschema>=3.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from altair<6,>=4.0->streamlit) (4.24.0)\n",
      "Requirement already satisfied: gitdb<5,>=4.0.1 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
      "Requirement already satisfied: smmap<6,>=3.0.1 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)\n",
      "Requirement already satisfied: attrs>=22.2.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (25.3.0)\n",
      "Requirement already satisfied: referencing>=0.28.4 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.36.2)\n",
      "Requirement already satisfied: rpds-py>=0.7.1 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.25.1)\n",
      "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2025.4.1)\n",
      "Requirement already satisfied: python-dateutil>=2.8.2 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from pandas<3,>=1.4.0->streamlit) (2.9.0.post0)\n",
      "Requirement already satisfied: pytz>=2020.1 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from pandas<3,>=1.4.0->streamlit) (2024.2)\n",
      "Requirement already satisfied: tzdata>=2022.7 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from pandas<3,>=1.4.0->streamlit) (2024.2)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from jinja2->altair<6,>=4.0->streamlit) (3.0.2)\n",
      "Requirement already satisfied: six>=1.5 in /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.15.0)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from requests<3,>=2.27->streamlit) (2024.8.30)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from requests<3,>=2.27->streamlit) (3.4.0)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from requests<3,>=2.27->streamlit) (2.2.3)\n",
      "\u001b[33mWARNING: You are using pip version 21.2.4; however, version 25.1.1 is available.\n",
      "You should consider upgrading via the '/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --upgrade pip' command.\u001b[0m\n",
      "Note: you may need to restart the kernel to use updated packages.\n",
      "Defaulting to user installation because normal site-packages is not writeable\n",
      "Collecting openai\n",
      "  Downloading openai-1.84.0-py3-none-any.whl (725 kB)\n",
      "\u001b[K     |████████████████████████████████| 725 kB 7.5 MB/s eta 0:00:01\n",
      "\u001b[?25hCollecting sniffio\n",
      "  Downloading sniffio-1.3.1-py3-none-any.whl (10 kB)\n",
      "Collecting httpx<1,>=0.23.0\n",
      "  Downloading httpx-0.28.1-py3-none-any.whl (73 kB)\n",
      "\u001b[K     |████████████████████████████████| 73 kB 6.4 MB/s eta 0:00:011\n",
      "\u001b[?25hCollecting jiter<1,>=0.4.0\n",
      "  Downloading jiter-0.10.0-cp39-cp39-macosx_11_0_arm64.whl (312 kB)\n",
      "\u001b[K     |████████████████████████████████| 312 kB 9.9 MB/s eta 0:00:01\n",
      "\u001b[?25hRequirement already satisfied: tqdm>4 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from openai) (4.67.1)\n",
      "Collecting pydantic<3,>=1.9.0\n",
      "  Downloading pydantic-2.11.5-py3-none-any.whl (444 kB)\n",
      "\u001b[K     |████████████████████████████████| 444 kB 10.1 MB/s eta 0:00:01\n",
      "\u001b[?25hCollecting distro<2,>=1.7.0\n",
      "  Downloading distro-1.9.0-py3-none-any.whl (20 kB)\n",
      "Collecting anyio<5,>=3.5.0\n",
      "  Downloading anyio-4.9.0-py3-none-any.whl (100 kB)\n",
      "\u001b[K     |████████████████████████████████| 100 kB 5.8 MB/s ta 0:00:01\n",
      "\u001b[?25hRequirement already satisfied: typing-extensions<5,>=4.11 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from openai) (4.12.2)\n",
      "Requirement already satisfied: idna>=2.8 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from anyio<5,>=3.5.0->openai) (3.10)\n",
      "Requirement already satisfied: exceptiongroup>=1.0.2 in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from anyio<5,>=3.5.0->openai) (1.2.2)\n",
      "Collecting httpcore==1.*\n",
      "  Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)\n",
      "\u001b[K     |████████████████████████████████| 78 kB 7.9 MB/s eta 0:00:01\n",
      "\u001b[?25hRequirement already satisfied: certifi in /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages (from httpx<1,>=0.23.0->openai) (2024.8.30)\n",
      "Collecting h11>=0.16\n",
      "  Downloading h11-0.16.0-py3-none-any.whl (37 kB)\n",
      "Collecting typing-inspection>=0.4.0\n",
      "  Downloading typing_inspection-0.4.1-py3-none-any.whl (14 kB)\n",
      "Collecting annotated-types>=0.6.0\n",
      "  Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)\n",
      "Collecting pydantic-core==2.33.2\n",
      "  Downloading pydantic_core-2.33.2-cp39-cp39-macosx_11_0_arm64.whl (1.9 MB)\n",
      "\u001b[K     |████████████████████████████████| 1.9 MB 11.4 MB/s eta 0:00:01\n",
      "\u001b[?25hInstalling collected packages: sniffio, h11, typing-inspection, pydantic-core, httpcore, anyio, annotated-types, pydantic, jiter, httpx, distro, openai\n",
      "Successfully installed annotated-types-0.7.0 anyio-4.9.0 distro-1.9.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 jiter-0.10.0 openai-1.84.0 pydantic-2.11.5 pydantic-core-2.33.2 sniffio-1.3.1 typing-inspection-0.4.1\n",
      "\u001b[33mWARNING: You are using pip version 21.2.4; however, version 25.1.1 is available.\n",
      "You should consider upgrading via the '/Library/Developer/CommandLineTools/usr/bin/python3 -m pip install --upgrade pip' command.\u001b[0m\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "%pip install streamlit\n",
    "%pip install openai"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "import openai \n",
    "openai.api_key = \"YOUR_API_KEY\"\n",
    "\n",
    "def ask_llm(prompt, persona):\n",
    "    system_msg = {\"role\": \"system\", \"content\": f\"You are a {persona} AI.\"}\n",
    "    user_msg = {\"role\": \"user\", \"content\": prompt}\n",
    "    response = openai.ChatCompletion.create(\n",
    "        model=\"gpt-4o\",\n",
    "        messages=[system_msg, user_msg]\n",
    "    )\n",
    "    return response.choices[0].message.content\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-06-05 10:27:01.624 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.660 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run /Users/samarhannachi/Library/Python/3.9/lib/python/site-packages/ipykernel_launcher.py [ARGUMENTS]\n",
      "2025-06-05 10:27:01.661 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.661 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.661 Session state does not function when running a script without `streamlit run`\n",
      "2025-06-05 10:27:01.661 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.661 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.662 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.662 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.662 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.662 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.662 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.663 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.663 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.663 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.663 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.663 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.664 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.665 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.665 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.665 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.665 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.665 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.665 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.666 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.666 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-05 10:27:01.666 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import csv\n",
    "from datetime import datetime\n",
    "\n",
    "st.title(\"Trust Dynamics Survey\")\n",
    "\n",
    "# Demographics\n",
    "if \"step\" not in st.session_state:\n",
    "    st.session_state.step = 0\n",
    "\n",
    "if st.session_state.step == 0:\n",
    "    st.write(\"Consent and Demographics\")\n",
    "    name = st.text_input(\"Name (optional)\")\n",
    "    age = st.text_input(\"Age\")\n",
    "    gender = st.selectbox(\"Gender\", [\"\", \"Female\", \"Male\", \"Other\"])\n",
    "    if st.button(\"Next\"):\n",
    "        st.session_state.name = name\n",
    "        st.session_state.age = age\n",
    "        st.session_state.gender = gender\n",
    "        st.session_state.step = 1\n",
    "\n",
    "elif st.session_state.step == 1:\n",
    "    st.write(\"Interact with the AI\")\n",
    "    persona = st.selectbox(\"Select AI Persona\", [\"Clinical\", \"Friendly\", \"Cautious\"])\n",
    "    prompt = st.text_input(\"Ask your question:\")\n",
    "    if st.button(\"Submit Question\"):\n",
    "        response = ask_llm(prompt, persona)\n",
    "        st.write(\"AI Response:\", response)\n",
    "\n",
    "        trust = st.slider(\"How much do you trust this answer?\", 1, 5, 3)\n",
    "        clarity = st.slider(\"How clear was this answer?\", 1, 5, 3)\n",
    "        safety = st.slider(\"How safe did you feel relying on this answer?\", 1, 5, 3)\n",
    "\n",
    "        # Save to CSV\n",
    "        with open(\"trust_logs.csv\", \"a\") as f:\n",
    "            writer = csv.writer(f)\n",
    "            writer.writerow([\n",
    "                st.session_state.name, st.session_state.age, st.session_state.gender,\n",
    "                persona, prompt, response, trust, clarity, safety,\n",
    "                datetime.now().isoformat()\n",
    "            ])\n",
    "        st.success(\"Response logged! You can ask another question or finish.\")\n",
    "\n",
    "    if st.button(\"Finish Survey\"):\n",
    "        st.session_state.step = 2\n",
    "\n",
    "elif st.session_state.step == 2:\n",
    "    st.write(\"Thank you for participating!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Errno 2] No such file or directory: '/path/to/trust-dynamics-survey'\n",
      "/\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/samarhannachi/Library/Python/3.9/lib/python/site-packages/IPython/core/magics/osm.py:393: UserWarning: using bookmarks requires you to install the `pickleshare` library.\n",
      "  bkms = self.shell.db.get('bookmarks', {})\n"
     ]
    }
   ],
   "source": [
    "%cd /path/to/trust-dynamics-survey"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

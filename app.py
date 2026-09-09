import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺",
    layout="centered"
)

# Retrieve the API key
API_KEY = os.getenv("GEMINI_API_KEY")

# Stop the app if the key is missing
if not API_KEY:
    st.error("API key is not configured. Please check your .env file.")
    st.stop()

# Initialize the Gemini client
client = genai.Client(api_key=API_KEY)

# -----------------------------
# Header Section
# -----------------------------
st.title("🩺 AI Health Assistant")
st.write(
    "Ask general questions about health, wellness, sleep, "
    "exercise, hydration, BMI, and healthy lifestyle."
)

# -----------------------------
# User Input Section
# -----------------------------
question = st.text_input(
    "Ask your health question:",
    placeholder="Example: Why is sleep important?"
)

# -----------------------------
# AI Generation Section
# -----------------------------
if st.button("Ask AI 🤖"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        # Construct the prompt with safety rules
        prompt = f"""
You are a helpful AI Health Assistant.

Answer the following question using simple and easy-to-understand
language.

Question:
{question}

Rules:
1. Give general health and wellness information.
2. Do not diagnose diseases.
3. Do not prescribe medicines or dosages.
4. Keep the answer clear and concise.
5. If the question is about a serious medical condition,
   recommend consulting a qualified healthcare professional.
"""
        
        try:
            # Show a loading spinner while waiting for the API
            with st.spinner("Generating answer..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            # Display the result
            st.subheader("🤖 AI Response")
            st.write(response.text)

        except Exception as e:
            st.error("Something went wrong while generating the answer.")
            st.write(str(e))

# -----------------------------
# Health Disclaimer
# -----------------------------
st.divider()

st.caption(
    "⚠️ Disclaimer: This AI Health Assistant provides general "
    "health and wellness information only. It is not a substitute "
    "for professional medical advice, diagnosis, or treatment."
)
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
import re

# Load environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error("API Key is missing. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# Initialize Gemini API client
client = genai.Client(api_key=api_key)

# Function to fetch caffeine content using Gemini API
def fetch_caffeine_content(energy_drink_name: str) -> float:
    prompt = (
        f"You are a factual assistant. Provide only a number. "
        f"What's the caffeine content in milligrams per serving of '{energy_drink_name}'?"
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        text = response.text.strip()
        match = re.search(r"([0-9]+\.?[0-9]*)", text)
        if match:
            return float(match.group(1))
        else:
            raise ValueError(f"No numeric value found in response: {text}")
    except Exception as e:
        st.error(f"Failed to fetch caffeine content: {e}")
        return None

# Streamlit app UI

def main():
    st.title("☕ Caffeine Intake Checker 🔋")
    st.write("Enter your gender, weight, energy drink, and number of servings to check if your total caffeine intake exceeds the recommended limit.")

    # Styled inputs with tighter spacing
    label_style = "font-size:18px;font-weight:bold;margin-bottom:2px;margin-top:4px;"
    st.markdown(f"<p style='{label_style}'>Gender</p>", unsafe_allow_html=True)
    gender = st.selectbox("", ["Male", "Female", "Other"])

    st.markdown(f"<p style='{label_style}'>Weight (lb)</p>", unsafe_allow_html=True)
    weight_lb = st.number_input("", min_value=1.0, step=0.1)

    st.markdown(f"<p style='{label_style}'>Energy Drink Name</p>", unsafe_allow_html=True)
    energy_drink = st.text_input("", "Red Bull")

    st.markdown(f"<p style='{label_style}'>Number of Servings</p>", unsafe_allow_html=True)
    servings = st.number_input("", min_value=1, step=1, value=1)

    if st.button("Check Caffeine"):
        caffeine_mg = fetch_caffeine_content(energy_drink)
        if caffeine_mg is not None:
            weight_kg = weight_lb * 0.45359237
            max_caffeine = 5.0 * weight_kg  # 5 mg per kg
            total_caffeine = caffeine_mg * servings

            st.write(f"**Gender:** {gender}")
            st.write(f"**Caffeine per serving of {energy_drink}:** {caffeine_mg:.1f} mg")
            st.write(f"**Number of servings:** {servings}")
            st.write(f"**Total caffeine intake:** {total_caffeine:.1f} mg")
            st.write(f"**Recommended max:** {max_caffeine:.1f} mg (5 mg/kg)")

            if total_caffeine > max_caffeine:
                st.error("⚠️ Too much caffeine! Consider limiting intake.")
            else:
                st.success("✅ Caffeine level is within the recommended limit.")

if __name__ == "__main__":
    main()
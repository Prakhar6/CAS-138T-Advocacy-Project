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

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Caffeine Intake Checker",
        page_icon="☕",
        layout="centered"
    )

    # Custom CSS for modern styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            font-size: 2.5rem !important;
            padding-bottom: 2rem;
        }
        .stSelectbox, .stNumberInput {
            margin-bottom: 1.5rem;
        }
        .stButton button {
            width: 100%;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .calculate-button button {
            background-color: #FF4B4B;
            color: white;
        }
        div[data-testid="stMarkdownContainer"] > p {
            font-size: 1.1rem;
            color: #555;
            margin-bottom: 0.5rem;
        }
        .drink-card {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid #eee;
        }
        .results-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #eee;
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state for drinks list if it doesn't exist
    if 'drinks' not in st.session_state:
        st.session_state.drinks = []
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    # App header with subtle description
    col1, col2 = st.columns([3, 1])  # 3: content column, 1: logo column
    with col2:
        st.image("logo.jpg", use_container_width=True)  # Your logo.jpg displayed here
    
    with col1:
        # App header with subtle description
        st.title("☕ Daily Caffeine Tracker")
        st.markdown("""
            <p style='font-size: 1.1rem; color: #666; margin-bottom: 2rem;'>
            Track your total caffeine consumption from multiple drinks
            </p>
        """, unsafe_allow_html=True)

    # Personal Information Section
    st.markdown("### Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            help="Select your gender"
        )
    
    with col2:
        weight_lb = st.number_input(
            "Weight (lb)",
            min_value=1.0,
            step=0.1,
            help="Enter your weight in pounds"
        )

    # Drink Addition Section
    st.markdown("### Add Drinks")
    col1, col2 = st.columns(2)
    
    with col1:
        new_drink = st.text_input(
            "Drink Name",
            placeholder="e.g., Red Bull",
            key="new_drink"
        )
    
    with col2:
        servings = st.number_input(
            "Number of Servings",
            min_value=1,
            step=1,
            value=1,
            key="servings"
        )

    # Add drink button
    if st.button("Add Drink", use_container_width=True):
        if new_drink:
            caffeine_content = fetch_caffeine_content(new_drink)
            if caffeine_content is not None:
                st.session_state.drinks.append({
                    "name": new_drink,
                    "servings": servings,
                    "caffeine_per_serving": caffeine_content
                })
                st.session_state.show_results = False  # Reset results view when new drink is added

    # Display added drinks
    if st.session_state.drinks:
        st.markdown("### Today's Drinks")
        
        for idx, drink in enumerate(st.session_state.drinks):
            # Create columns for drink info and delete button
            drink_col, del_col = st.columns([6, 1])
            
            with drink_col:
                st.markdown(f"""
                    <div class="drink-card">
                        <strong>{drink["name"]}</strong>
                        <p>Servings: {drink["servings"]}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with del_col:
                if st.button("❌", key=f"delete_{idx}", help="Delete this drink"):
                    st.session_state.drinks.pop(idx)
                    st.session_state.show_results = False  # Reset results view when drink is deleted
                    st.rerun()  # Using the new rerun() method instead of experimental_rerun()

        # Calculate button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Calculate Total Caffeine Intake", use_container_width=True, type="primary"):
            st.session_state.show_results = True

        # Show results only after calculate button is pressed
        if st.session_state.show_results:
            # Calculate total caffeine
            total_caffeine = sum(
                drink["caffeine_per_serving"] * drink["servings"]
                for drink in st.session_state.drinks
            )
            
            weight_kg = weight_lb * 0.45359237
            max_caffeine = 5.0 * weight_kg

            # Results section
            st.markdown("### Results")
            
            # Display detailed breakdown
            st.markdown("#### Drink Breakdown")
            for drink in st.session_state.drinks:
                drink_total = drink["caffeine_per_serving"] * drink["servings"]
                st.markdown(f"""
                    <div class="drink-card">
                        <strong>{drink["name"]}</strong>
                        <p>Caffeine per serving: {drink["caffeine_per_serving"]:.1f} mg</p>
                        <p>Servings: {drink["servings"]}</p>
                        <p>Total caffeine: {drink_total:.1f} mg</p>
                    </div>
                """, unsafe_allow_html=True)

            # Summary card
            st.markdown(f"""
                <div class="results-card">
                    <h4 style='margin-bottom: 1rem; color: #333;'>Daily Summary</h4>
                    <p><strong>Total caffeine consumed:</strong> {total_caffeine:.1f} mg</p>
                    <p><strong>Recommended maximum:</strong> {max_caffeine:.1f} mg</p>
                </div>
            """, unsafe_allow_html=True)

            if total_caffeine > max_caffeine:
                st.error("⚠️ Your total caffeine intake exceeds the recommended daily limit. Consider reducing consumption.")
            else:
                st.success("✅ Your total caffeine intake is within the recommended daily limit.")

if __name__ == "__main__":
    main()
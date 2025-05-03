# Advocacy-Project-Name---Caffeine-Intake-Calculator
## Overview

**Caffeine Intake Calculator** is a modern, interactive web app that helps users track their daily caffeine consumption from multiple drinks. The app leverages the Gemini API to fetch accurate caffeine content for any drink you enter, and provides personalized recommendations based on your weight and gender. The intuitive interface allows you to add, review, and remove drinks, and see if your total caffeine intake is within the recommended daily limit.

## Features

- **Personalized Tracking:** Enter your gender and weight for tailored caffeine recommendations.
- **Smart Drink Addition:** Add any drink by name and number of servings; the app fetches caffeine content automatically.
- **Dynamic Drink List:** View, update, and remove drinks from your daily list.
- **Instant Calculations:** See your total caffeine intake and compare it to your recommended maximum.
- **Visual Feedback:** Get clear alerts if you exceed healthy limits, and a breakdown of each drink’s contribution.

## Setup

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Set up your environment:**
    - Create a `.env` file in the project root with your Gemini API key:
      ```
      GEMINI_API_KEY=your_api_key_here
      ```

3. **Run the app:**
    ```bash
    streamlit run index.py
    ```

## Notes

- The app uses the Gemini API to fetch caffeine content, so an internet connection and valid API key are required.
- All calculations and recommendations are for informational purposes only.

---

*Developed for CAS-138T Advocacy Project*


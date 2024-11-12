# app.py
import openai
import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

#comment

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("openai_key")

# -------------------------
# 1. Background, containers, styling
# -------------------------
# CSS styles

st.markdown("""
<style>
/* background */
.stApp {
    background: url('https://i.ibb.co/MpbbQDx/meal-steal-bg.gif'); /*need to import better gif */
    background-size: cover; 
    background-position: top;
}

/* styling for subheader + other text elements */
.subheader-container {
    border: 2px solid white;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    max-width: 80%;  /* Adjusted for centering */
    margin: 0 auto;
}

.subheader-container img { 
    width: 300px;
}

/* Flex container for logo and subheader */
.header-container {
    display: flex;
    align-items: left; /* Center vertically */
    justify-content: left; /* Center horizontally */
    margin: 20px; /* Add some margin */
}

/* Styling for the logo */
.header-container img { 
    width: 100px; /* Adjust width for the logo */
    margin-right: 20px; /* Space between logo and subheader */
}

/* styling for tabs */
.stTabs [role='tab'] {
    border: 2px solid white;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: fit-content;  /* Allows the tab box to resize based on text content */
    margin: 0 5px;
    white-space: nowrap;  /* Prevents text from wrapping within the tab */
}

/* Tab panel styling to have a frosted effect */
.stTabs [role="tabpanel"] {
    border: 2px solid white;
    backdrop-filter: blur(20px);  /* Frosted effect */
    background: rgba(255, 255, 255, 0.1);  /* Background with slight opacity */
    padding: 20px;  /* Padding for content */
    border-radius: 10px;  /* Rounded corners */
    color: #DAD7CD;  /* Light text color */
}

/* General styles for meal plan section */
.meal-plan-section {
    margin-top: 20px; /* Space above meal plan section */
    padding: 20px; /* Padding for content */
    border-radius: 10px; /* Rounded corners */
    backdrop-filter: blur(20px); /* Frosted effect */
    background: rgba(255, 255, 255, 0.1); /* Slightly transparent background */
    color: #DAD7CD; /* Light text color */
}

/* Cards for meal plan (existing styles removed) */
.card {
    position: relative;
    width: 160px; /* Adjust width as needed */
    height: 220px; /* Adjust height as needed */
    background: #335D3B;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;  /* Font size of text in the card */
    font-weight: bold;
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.5s; /* Smooth transitions */
    margin: 5px;  /* Smaller gap between cards */
}

/* Styling for card hover effects */
.card::before,
.card::after {
    position: absolute;
    content: "";
    width: 20%;
    height: 20%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;  /* Font size for hover text */
    font-weight: bold;
    background-color: #67944C;
    transition: all 0.5s; /* Smooth transitions */
}

.card::before {
    top: 0;
    right: 0;
    border-radius: 0 15px 0 100%; /* Top right corner rounded */
}

.card::after {
    bottom: 0;
    left: 0;
    border-radius: 0 100% 0 15px; /* Bottom left corner rounded */
}

/* Hover effects for cards */
.card:hover::before,
.card:hover::after {
    width: 100%; /* Expand on hover */
    height: 100%; /* Expand on hover */
    border-radius: 15px; /* Rounded corners on hover */
}

.card:hover:after {
    content: "Meal Plan"; /* Show meal plan text on hover */
    color: #DAD7CD; /* Text color for visibility */
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #335D3B;
    color: #DAD7CD;
}

.stTabs [role="tabpanel"] {
    margin-top: 20px;  /* Adjust this value to create a gap */
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# 2. Logo, subheader
# -------------------------

st.markdown("""
<div class='text-container'>
    <img src="https://i.ibb.co/tmQpKH2/1-removebg-preview.png" alt="Meal Steal Logo" style="display: block; margin: 0 auto;">
    <div class='subheader-container'>
        <h2>Get Fit, Eat Smart, Spend Less</h2>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 3. User input form/sidebar
# -------------------------

st.sidebar.header('Preferences Hub')
st.sidebar.markdown("Fill out your preferences to tailor your meal plan!")

# Collect user preferences
age = st.sidebar.number_input('Age', min_value=10, max_value=90)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300)
goal = st.sidebar.selectbox('Health Goal', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'])
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian', 'None'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', '')
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
activity_type = st.sidebar.multiselect('Types of Physical Activity', ['Cardio', 'Strength Training', 'Yoga/Pilates', 'Sports', 'Other'])
meal_frequency = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)

# Construct API prompt based on user input
user_data_prompt = f"""
Generate a personalized meal plan based on the following user preferences:
- Age: {age}
- Gender: {gender}
- Weight: {weight} kg
- Height: {height} cm
- Health Goal: {goal}
- Dietary Preferences: {', '.join(dietary_pref) if dietary_pref else 'None'}
- Allergies: {allergies if allergies else 'None'}
- Exercise Level: {exercise_level}
- Types of Physical Activity: {', '.join(activity_type) if activity_type else 'None'}
- Meal Frequency: {meal_frequency}
- Meal Prep Time: {meal_prep}
- Plan Duration: {days} days
"""

# Use session state to manage meal plan generation
if "meal_plan_text" not in st.session_state:
    st.session_state.meal_plan_text = ""

# Submit Button for generating meal plan
if st.sidebar.button("Cook Up My Plan!"):
    st.write("Generating your personalized meal plan...")

    # Call OpenAI API
try:
    with st.spinner("Fetching your personalized meal plan..."):
        response = openai.Completion.create(
            engine="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",  # Use your fine-tuned model here
            prompt=user_data_prompt,
            max_tokens=500
        )
    st.session_state.meal_plan_text = response.choices[0].text.strip()

except Exception as e:
    st.error("Error fetching meal plan. Please try again.")
    st.session_state.meal_plan_text = ""


# -------------------------
# 4. Tabs for additional content
# -------------------------

tab1, tab2, tab3, tab4 = st.tabs(['Your Meal Plan', 'Adjust Your Plan', 'Recipes', 'Nutritional Info'])

# Display meal plan in "Your Meal Plan" tab
with tab1:
    st.markdown('<h2 style="text-align: center;">Your Personalized Meal Plan</h2>', unsafe_allow_html=True)
    if st.session_state.meal_plan_text:
        st.write(st.session_state.meal_plan_text)
    else:
        st.write("No meal plan generated yet. Fill out your preferences and submit to get started.")

# Placeholder content for remaining tabs
with tab2:
    st.subheader('Adjust Your Meal Plan')
    st.write('Adjust your meal plan here.')

with tab3:
    st.subheader('Recipes')
    st.write('Find recipes here.')

with tab4:
    st.subheader('Nutritional Info')
    st.write('View nutritional info here.')

# ----
# Footer
# ----

st.markdown("""
    <footer>
        <p style="text-align: center; color: #DAD7CD;">© 2024 Meal Steal. All rights reserved.</p>
    </footer>
""", unsafe_allow_html=True)
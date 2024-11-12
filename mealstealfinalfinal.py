import streamlit as st
import openai
import os
from dotenv import load_dotenv
 
# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
 
# CSS and layout styling
st.markdown("""
<style>
/* Add your custom CSS here */
</style>
""", unsafe_allow_html=True)
 
# Logo and Header
st.markdown("""
<div class='text-container'>
<img src="https://i.ibb.co/tmQpKH2/1-removebg-preview.png" alt="Meal Steal Logo" style="display: block; margin: 0 auto;">
<div class='subheader-container'>
<h2>Get Fit, Eat Smart, Spend Less</h2>
</div>
</div>
""", unsafe_allow_html=True)
 
# Sidebar for User Input
st.sidebar.header('Preferences Hub')
st.sidebar.markdown("Fill out as many or as few details as you’d like. All options are optional, so feel free to tailor it to your preferences!")
 
# Collect User Inputs
age = st.sidebar.number_input('Age', min_value=10, max_value=90)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300)
goal = st.sidebar.selectbox('Health Goal', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'])
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian', 'None'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', '')
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
body_fat = st.sidebar.number_input('Body Fat Percentage (%)', min_value=5, max_value=60, value=20)
meal_frequency = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)
 
# Button to generate meal plan
if st.sidebar.button("Cook Up My Plan!"):
    # Generate prompt based on user inputs
    total_meals = int(meal_frequency.split()[0]) * days
    meal_prep_time = '30-60min' if 'Moderate' in meal_prep else ('<30min' if 'Minimal' in meal_prep else '>60min')
    dietary_pref_str = ', '.join(dietary_pref)
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time.lower()} and suitable for a meal plan with {meal_frequency} per day over {days} days. "
        f"Each recipe should include a title, ingredients with quantities specifically in grams and milliliters, cooking instructions, cuisine, diet, total cooking time, "
        f"servings for {total_meals} meals, estimated price in GBP (£), and full nutrition information including calories, protein, carbohydrates, and fats. "
        f"Convert all ingredient quantities to metric measurements. "
        f"Consider the following user details: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {goal}, "
        f"Dietary Preferences - {dietary_pref_str}, Allergies - {allergies}, Exercise Level - {exercise_level}, Body Fat Percentage - {body_fat}%."
    )
 
    # Send request to OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",
            messages=[{"role": "user", "content": prompt}]
        )
        meal_plan = response.choices[0].message.content
        st.write("Your personalized meal plan:")
        st.write(meal_plan)
 
    except openai.error.AuthenticationError:
        st.error("API Key is invalid or has been disabled.")
 
# Display meal plan tabs
tab1, tab2, tab3, tab4 = st.tabs(['Your Meal Plan', 'Adjust Your Plan', 'Recipes', 'Nutritional Info'])
 
with tab1:
    st.markdown('<h2 style="text-align: center;">Your Personalized Meal Plan</h2>', unsafe_allow_html=True)
    # Display the meal plan in a more organized format (if further processed)


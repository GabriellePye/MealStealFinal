import streamlit as st
import openai
from openai import OpenAI
import time
 
# Initialize OpenAI client
openai.api_key = st.secrets["openai_key"]
client = OpenAI(api_key=st.secrets["openai_key"])
 
# -------------------------
# 3. User input form/sidebar
# -------------------------
# Sidebar Main Header and Introductory Statement
st.sidebar.header('Preferences Hub')
st.sidebar.markdown("Fill out as many or as few details as you’d like. All options are optional, so feel free to tailor it to your preferences!")
# Basic Demographic Information
st.sidebar.subheader("Basic Information")
age = st.sidebar.number_input('Age', min_value=10, max_value=90)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300)
# Health Goals and Dietary Preferences
st.sidebar.subheader("Health Goals & Dietary Preferences")
goal = st.sidebar.selectbox('Health Goal', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'])
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian', 'None'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', '')
# Physical Activity and Exercise Details
st.sidebar.subheader("Physical Activity")
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
activity_type = st.sidebar.multiselect('Types of Physical Activity', ['Cardio', 'Strength Training', 'Yoga/Pilates', 'Sports', 'Other'])
# Body Composition and Water Intake
st.sidebar.subheader("Body Composition & Hydration")
body_fat = st.sidebar.number_input('Body Fat Percentage (%)', min_value=5, max_value=60, value=20)
water_intake = st.sidebar.number_input('Daily Water Intake (Liters)', min_value=0.5, max_value=5.0, step=0.1)
# Health and Lifestyle Factors
st.sidebar.subheader("Health & Lifestyle")
sleep_quality = st.sidebar.selectbox('Sleep Quality', ['Poor', 'Average', 'Good', 'Very Good'])
stress_level = st.sidebar.selectbox('Stress Level', ['Low', 'Moderate', 'High'])
medical_conditions = st.sidebar.text_input('Medical Conditions (e.g., diabetes, hypertension)')
# Food Preferences
st.sidebar.subheader("Food Preferences")
food_likes = st.sidebar.text_input('Foods You Like (comma-separated)')
food_dislikes = st.sidebar.text_input('Foods You Dislike (comma-separated)')
supplements = st.sidebar.text_input('Supplements (comma-separated)')
# Meal Plan Customization
st.sidebar.subheader("Meal Plan Customization")
meal_frequency = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
st.sidebar.markdown('### Set Meal Plan Duration')
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)
 
# Function to Generate Recipes with OpenAI
def generate_recipes(age, gender, weight, height, health_goal, dietary_preferences, allergies, exercise_level, body_fat, meals_per_day, meal_plan_duration, meal_prep):
    total_meals = meals_per_day * meal_plan_duration
    prompt = (
        f"Please generate {total_meals} recipes for a meal plan that includes {meals_per_day} meals per day over {meal_plan_duration} days. "
        f"Each recipe should be suitable for {meal_prep.lower()} preparation and should be formatted as follows:\n\n"
        f"1. **Title**: The name of the recipe\n"
        f"2. **Cuisine**: Type of cuisine (e.g., Italian, Mexican, etc.)\n"
        f"3. **Diet**: Specify any dietary restrictions (e.g., Vegetarian, Gluten-Free)\n"
        f"4. **Ingredients**: List ingredients with specific quantities in grams (g) and milliliters (ml), avoiding imperial units\n"
        f"5. **Instructions**: Step-by-step cooking instructions\n"
        f"6. **Total Cooking Time**: Estimated time to prepare the meal in minutes\n"
        f"7. **Servings**: Number of servings (e.g., 1 serving per recipe)\n"
        f"8. **Estimated Price**: Price in GBP (£)\n"
        f"9. **Nutritional Information**:\n"
        f"   - Calories\n"
        f"   - Protein (g)\n"
        f"   - Carbohydrates (g)\n"
        f"   - Fats (g)\n\n"
        f"Consider these user details when creating the recipes:\n"
        f"- Age: {age}\n"
        f"- Gender: {gender}\n"
        f"- Weight: {weight} kg\n"
        f"- Height: {height} cm\n"
        f"- Health Goal: {health_goal}\n"
        f"- Dietary Preferences: {dietary_preferences}\n"
        f"- Allergies: {allergies}\n"
        f"- Exercise Level: {exercise_level}\n"
        f"- Body Fat Percentage: {body_fat}%\n\n"
        f"Please keep the format consistent for each recipe to make it easier to read and follow."
    )
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
 
# Trigger recipe generation
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner('Creating your personalized plan...'):
        recipes = generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, body_fat, meal_frequency, days, meal_prep)
    st.success("Your personalized meal plan is ready!")
    # Display the generated recipes in a large text block
    st.markdown("### Your Generated Meal Plan")
    st.write(recipes)
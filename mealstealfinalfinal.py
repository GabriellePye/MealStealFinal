import streamlit as st
import openai  # Importing OpenAI for the backend integration
from openai import OpenAI
import time

# -------------------------
# 1. Background, containers, styling
# -------------------------

# CSS styles
st.markdown("""
<style>
/* background */
.stApp {
    background: url('https://i.ibb.co/MpbbQDx/meal-steal-bg.gif');
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
    max-width: 80%;
    margin: 0 auto;
}

/* Flex container for logo and subheader */
.header-container {
    display: flex;
    align-items: left;
    justify-content: left;
    margin: 20px;
}

.header-container img { 
    width: 100px;
    margin-right: 20px;
}

/* styling for tabs */
.stTabs [role='tab'] {
    border: 2px solid white;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: fit-content;
    margin: 0 5px;
    white-space: nowrap;
}

/* Tab panel styling */
.stTabs [role="tabpanel"] {
    border: 2px solid white;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    color: #DAD7CD;
}

/* General styles for meal plan section */
.meal-plan-section {
    margin-top: 20px;
    padding: 20px;
    border-radius: 10px;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    color: #DAD7CD;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #335D3B;
    color: #DAD7CD;
}
</style>
""", unsafe_allow_html=True)

# Initialize the OpenAI client
openai.api_key = st.secrets["openai_key"]
client = OpenAI(api_key=st.secrets["openai_key"])

# -------------------------
# Function to Generate Recipes with OpenAI
# -------------------------

def generate_recipes(age, gender, weight, height, health_goal, dietary_preferences, allergies, exercise_level, body_fat, meals_per_day, meal_plan_duration, meal_prep):
    total_meals = meals_per_day * meal_plan_duration
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep.lower()} and suitable for a meal plan with {meals_per_day} meals per day over {meal_plan_duration} days. "
        f"Each recipe should include a title, ingredients with quantities in grams and milliliters, cooking instructions, cuisine, diet, total cooking time, servings, estimated price in GBP (£), and full nutrition information. "
        f"Consider the following user details: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {health_goal}, "
        f"Dietary Preferences - {dietary_preferences}, Allergies - {allergies}, Exercise Level - {exercise_level}, Body Fat Percentage - {body_fat}%. "
    )

    # Generate recipes using the prompt
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

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

# Sidebar Main Header and Introductory Statement
st.sidebar.header('Preferences Hub')
st.sidebar.markdown("Fill out as many or as few details as you’d like. All options are optional, so feel free to tailor it to your preferences!")

# Basic Demographic Information
age = st.sidebar.number_input('Age', min_value=10, max_value=90)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300)

# Health Goals and Dietary Preferences
health_goal = st.sidebar.selectbox('Health Goal', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'])
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian', 'None'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', '')

# Physical Activity and Exercise Details
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
body_fat = st.sidebar.number_input('Body Fat Percentage (%)', min_value=5, max_value=60, value=20)

# Meal Plan Customization
meals_per_day = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)

# -------------------------
# 4. Generate Meal Plan Button and Display Recipes
# -------------------------

if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner('Creating your personalized plan...'):
        recipes = generate_recipes(age, gender, weight, height, health_goal, dietary_pref, allergies, exercise_level, body_fat, meals_per_day, days, meal_prep)
    st.success("Your personalized meal plan is ready!")

# -------------------------
# 5. Tabs for Meal Plan, Adjustments, Recipes, Nutritional Info
# -------------------------

tab1, tab2, tab3, tab4 = st.tabs(['Your Meal Plan', 'Adjust Your Plan', 'Recipes', 'Nutritional Info'])

with tab1:
    st.markdown('<h2 style="text-align: center;">Your Personalized Meal Plan</h2>', unsafe_allow_html=True)
    st.write(recipes)  # Display the generated recipes here

with tab2:
    st.subheader('Adjust Your Meal Plan')
    st.write('Fill in later. Be sure to include *if possible click and drop options')

with tab3:
    st.subheader('Recipes')
    st.write('Fill in later - maybe have meal plan for the days on side with drop down options (or above) and then you can choose recipes to view?')

with tab4:
    st.subheader('Nutritional Info')
    st.write('Fill in later. Collate information for the whole meal plan or for certain meals/days?')

# -------------------------
# 6. Footer
# -------------------------

st.markdown("""
    <footer>
        <p style="text-align: center; color: #DAD7CD;">© 2024 Meal Steal. All rights reserved.</p>
    </footer>
""", unsafe_allow_html=True)
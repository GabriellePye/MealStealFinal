import streamlit as st
import openai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import re

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

# Meal Plan Customization
st.sidebar.subheader("Meal Plan Customization")
meal_frequency = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
servings = st.sidebar.number_input('Number of Servings per Recipe', min_value=1, max_value=10, value=2)
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)

# Function to Generate Recipes with OpenAI
def generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meals_per_day, days, meal_prep, servings):
    total_meals = int(meals_per_day.split()[0]) * days
    dietary_preferences = ', '.join(dietary_pref)
    meal_prep_time = meal_prep.lower()
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time} and suitable for a meal plan with {meals_per_day} per day over {days} days. "
        f"Each recipe should include a title, ingredients with quantities specifically in grams and milliliters, cooking instructions, cuisine, diet, total cooking time, servings (for {servings} servings), estimated price in GBP (£), "
        f"and full nutrition information including calories, protein, carbohydrates, and fats. "
        f"Consider the following user details: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {goal}, "
        f"Dietary Preferences - {dietary_preferences}, Allergies - {allergies}, Exercise Level - {exercise_level}. "
    )
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",  # Replace with your fine-tuned model ID
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# Parse nutrition info from generated recipes
def parse_nutrition_info(recipes_text):
    data = {
        "Recipe": [],
        "Calories": [],
        "Protein (g)": [],
        "Carbs (g)": [],
        "Fats (g)": []
    }

    # Use regex to parse the recipe title and nutritional information from plain text
    recipe_sections = re.split(r'\bTitle:\s*(.*?)\n', recipes_text)[1:]

    for i in range(0, len(recipe_sections), 2):
        title = recipe_sections[i].strip()
        details = recipe_sections[i+1]

        data["Recipe"].append(title)

        # Extract nutrient values using regex
        calories = re.search(r'Calories:\s*(\d+)', details)
        protein = re.search(r'Protein:\s*(\d+)', details)
        carbs = re.search(r'Carbohydrates:\s*(\d+)', details)
        fats = re.search(r'Fats:\s*(\d+)', details)

        data["Calories"].append(int(calories.group(1)) if calories else 0)
        data["Protein (g)"].append(int(protein.group(1)) if protein else 0)
        data["Carbs (g)"].append(int(carbs.group(1)) if carbs else 0)
        data["Fats (g)"].append(int(fats.group(1)) if fats else 0)

    return pd.DataFrame(data)

# Trigger recipe generation
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner('Creating your personalized plan...'):
        recipes_text = generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meal_frequency, days, meal_prep, servings)
    st.success("Your personalized meal plan is ready!")

    # Tabs for displaying meal plan, recipes, and nutrition analysis
    st.markdown("### Meal Plan Overview")
    tab1, tab2, tab3, tab4 = st.tabs(["At-a-Glance", "Full Meal Plan", "Individual Recipes", "Nutrition Dashboard"])

    # Tab 1: Meal Plan At-a-Glance
    with tab1:
        st.markdown('<h2 style="text-align: center;">Meal Plan At-a-Glance</h2>', unsafe_allow_html=True)
        day_count = min(days, 7)
        for day in range(1, day_count + 1):
            st.markdown(f"#### Day {day}")
            st.write(f"Meals for Day {day} (click for more details in the Full Meal Plan tab)")

    # Tab 2: Full Meal Plan Display
    with tab2:
        st.markdown("### Full Meal Plan")
        st.write(recipes_text)  # Display full meal plan text as a large block

    # Tab 3: Individual Recipes (Collapsible sections)
    with tab3:
        st.markdown("### Individual Recipes")
        for i in range(day_count):
            with st.expander(f"Recipe for Day {i+1}"):
                st.write(f"Recipe details for Day {i+1} (e.g., breakfast, lunch, dinner)")

    # Tab 4: Nutrition Dashboard
    with tab4:
        st.markdown("### Nutrition Breakdown")

        # Radar Chart Visualization
        nutrition_df = parse_nutrition_info(recipes_text)
        fig = go.Figure()
        nutrients = ["Calories", "Protein (g)", "Carbs (g)", "Fats (g)"]

        for index, row in nutrition_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row["Calories"], row["Protein (g)"], row["Carbs (g)"], row["Fats (g)"]],
                theta=nutrients,
                fill='toself',
                name=row["Recipe"]
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=True,
            title="Nutrient Composition by Recipe"
        )
        st.plotly_chart(fig)

        # Pie Chart for Total Nutrients Across All Recipes
        nutrient_totals = nutrition_df[nutrients].sum()
        pie_fig = px.pie(values=nutrient_totals, names=nutrients, title="Total Nutrient Distribution Across Recipes")
        st.plotly_chart(pie_fig)

# -------------------------
# CSS Styling for the Page
# -------------------------
st.markdown("""
<style>
/* background */
.stApp {
    background: url('https://i.ibb.co/MpbbQDx/meal-steal-bg.gif');
    background-size: cover; 
    background-position: top;
}
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
.stTabs [role="tabpanel"] {
    border: 2px solid white;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    color: #DAD7CD;
}
.meal-plan-section {
    margin-top: 20px;
    padding: 20px;
    border-radius: 10px;
    backdrop
</style>
""", unsafe_allow_html=True)
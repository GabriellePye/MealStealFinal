import streamlit as st
import openai
from openai import OpenAI
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize OpenAI client
openai.api_key = st.secrets["openai_key"]
client = OpenAI(api_key=st.secrets["openai_key"])

# 1. Sidebar User Input
st.sidebar.header('Preferences Hub')
st.sidebar.markdown("Customize your meal plan based on your preferences.")

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

# Physical Activity
st.sidebar.subheader("Physical Activity")
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])

# Meal Plan Customization
st.sidebar.subheader("Meal Plan Customization")
meal_frequency = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal', 'Moderate', 'Detailed'])
servings = st.sidebar.number_input('Number of Servings per Recipe', min_value=1, max_value=10, value=2)
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)

# 2. Recipe Generation Function
def generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meals_per_day, days, meal_prep, servings):
    total_meals = int(meals_per_day.split()[0]) * days
    dietary_preferences = ', '.join(dietary_pref)
    meal_prep_time = meal_prep.lower()
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time} and suitable for a meal plan with {meals_per_day} per day over {days} days. "
        f"Include a title, ingredients, instructions, and nutrition info including calories, protein, carbs, and fats."
        f"User details: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Goal - {goal}, "
        f"Dietary Preferences - {dietary_preferences}, Allergies - {allergies}, Exercise Level - {exercise_level}."
    )
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# Placeholder function to parse nutrition info from generated recipes
def parse_nutrition_info(recipes_text):
    data = {
        "Recipe": ["Recipe 1", "Recipe 2", "Recipe 3"],
        "Calories": [450, 380, 520],
        "Protein (g)": [25, 20, 30],
        "Carbs (g)": [60, 50, 80],
        "Fats (g)": [15, 10, 20]
    }
    df = pd.DataFrame(data)
    return df

# Trigger recipe generation
if st.sidebar.button("Cook Up My Plan!"):
    recipes = generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meal_frequency, days, meal_prep, servings)
    nutrition_df = parse_nutrition_info(recipes)
else:
    recipes = "Generate a meal plan using the sidebar options."
    nutrition_df = pd.DataFrame()

# 3. Main Content Tabs
st.markdown('<div class="content-section">', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(['Your Meal Plan', 'Meal Plan Details', 'Recipes', 'Nutrition Dashboard'])

# Tab 1: Meal Plan at a Glance
with tab1:
    st.markdown('<h2 style="text-align: center;">Meal Plan at a Glance</h2>', unsafe_allow_html=True)
    for day in range(1, days + 1):
        st.markdown(f"### Day {day}")
        st.write(f"Meals for Day {day}: {recipes}")  # Replace with actual meals if parsed separately

# Tab 2: Full Meal Plan Details
with tab2:
    st.markdown("### Detailed Meal Plan")
    st.write(recipes)

# Tab 3: Recipes
with tab3:
    st.markdown("### Individual Recipes")
    for recipe in range(1, days + 1):  # Loop over recipe examples
        with st.expander(f"Recipe {recipe}"):
            st.write(f"Details for Recipe {recipe}: Ingredients and Instructions")

# Tab 4: Nutrition Dashboard
with tab4:
    st.markdown("### Nutrition Breakdown")
    fig = go.Figure()
    nutrients = ["Calories", "Protein (g)", "Carbs (g)", "Fats (g)"]
    for index, row in nutrition_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["Calories"], row["Protein (g)"], row["Carbs (g)"], row["Fats (g)"]],
            theta=nutrients,
            fill='toself',
            name=row["Recipe"]
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True, title="Nutrient Composition by Recipe")
    st.plotly_chart(fig)

    nutrient_totals = nutrition_df[nutrients].sum()
    pie_fig = px.pie(values=nutrient_totals, names=nutrients, title="Total Nutrient Distribution")
    st.plotly_chart(pie_fig)

st.markdown('</div>', unsafe_allow_html=True)

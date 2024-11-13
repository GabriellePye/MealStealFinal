import streamlit as st
import openai
from openai import OpenAI
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

# Function to clean and parse JSON-like response
def clean_and_format_output(output_text):
    # Remove escape characters (e.g., \u00a0, \u2019)
    clean_text = re.sub(r'\\u[0-9A-Fa-f]{4}', '', output_text)
    # Attempt to parse as JSON if structured, or fall back to plain text display
    try:
        recipes = json.loads(clean_text)
    except json.JSONDecodeError:
        return clean_text  # Return plain text if JSON parsing fails
 
    # Format the parsed JSON as structured text
    formatted_text = ""
    for recipe in recipes:
        formatted_text += f"**Title**: {recipe.get('title', 'N/A')}\n"
        formatted_text += f"**Cuisine**: {recipe.get('cuisine', 'N/A')}\n"
        formatted_text += f"**Diet**: {recipe.get('diet', 'N/A')}\n"
        formatted_text += "**Ingredients**:\n"
        for ingredient in recipe.get('ingredients', []):
            formatted_text += f"  - {ingredient}\n"
        formatted_text += f"**Instructions**: {recipe.get('instructions', 'N/A')}\n"
        formatted_text += f"**Total Cooking Time**: {recipe.get('total cooking time', 'N/A')}\n"
        formatted_text += f"**Servings**: {recipe.get('servings', 'N/A')}\n"
        formatted_text += f"**Estimated Price**: {recipe.get('estimated price', 'N/A')}\n"
        formatted_text += "**Nutritional Information**:\n"
        for nutrient, value in recipe.get('nutritional information', {}).items():
            formatted_text += f"  - {nutrient}: {value}\n"
        formatted_text += "\n---\n\n"  # Separator between recipes
 
    return formatted_text

# Function to Generate Recipes with OpenAI
def generate_recipes(age, gender, weight, height, health_goal, dietary_preferences, allergies, exercise_level, body_fat, meals_per_day, meal_plan_duration, meal_prep):
    total_meals = meals_per_day * meal_plan_duration
    prompt = (
        f"Please generate {total_meals} recipes for a meal plan with {meals_per_day} meals per day over {meal_plan_duration} days. "
        f"Each day should have distinct meals, typically breakfast, lunch, and dinner (or similar meal types), totaling {meals_per_day} meals per day. "
        f"Each recipe should include the following details in a structured JSON format:\n"
        f"1. **Title**\n"
        f"2. **Cuisine**\n"
        f"3. **Diet** (e.g., Vegetarian, Gluten-Free)\n"
        f"4. **Ingredients** (specific quantities in grams and milliliters)\n"
        f"5. **Instructions** (step-by-step)\n"
        f"6. **Total Cooking Time**\n"
        f"7. **Servings**\n"
        f"8. **Estimated Price** in GBP (£)\n"
        f"9. **Nutritional Information** (calories, protein, carbohydrates, fats)\n\n"
        f"Consider these user details:\n"
        f"- Age: {age}\n"
        f"- Gender: {gender}\n"
        f"- Weight: {weight} kg\n"
        f"- Height: {height} cm\n"
        f"- Health Goal: {health_goal}\n"
        f"- Dietary Preferences: {dietary_preferences}\n"
        f"- Allergies: {allergies}\n"
        f"- Exercise Level: {exercise_level}\n"
        f"- Body Fat Percentage: {body_fat}%\n\n"
        f"Please ensure each recipe is unique and that the total number of recipes equals {total_meals}."
    )
 
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",
        messages=[{"role": "user", "content": prompt}]
    )
    output_text = completion.choices[0].message.content
    return clean_and_format_output(output_text)  # Clean and format the output

# Parse nutrition info from generated recipes
def parse_nutrition_info(recipes_text):
    # Assume recipes_text is structured to have nutrition details for each recipe in a standard format
    # Here, we'll mock a parsed dataframe with example structure
    # Replace with actual parsing logic depending on how OpenAI structures the output

    # Example parsed data structure
    data = {
        "Recipe": ["Recipe 1", "Recipe 2", "Recipe 3"],  # Replace with actual titles
        "Calories": [450, 380, 520],
        "Protein (g)": [25, 20, 30],
        "Carbs (g)": [60, 50, 80],
        "Fats (g)": [15, 10, 20]
    }
    df = pd.DataFrame(data)
    return df

# Trigger recipe generation
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner('Creating your personalized plan...'):
        recipes = generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, body_fat, meal_frequency, days, meal_prep)
    st.success("Your personalized meal plan is ready!")
    
    # Display the generated recipes in a large text block
    st.markdown("### Your Generated Meal Plan")
    st.write(recipes)
    
    # Parse nutrition info
    nutrition_df = parse_nutrition_info(recipes)

    # Separate tab for Nutrition Visualization
    st.markdown("### Nutrition Analysis")
    tab1, tab2 = st.tabs(["Meal Plan", "Nutrition Dashboard"])

    with tab2:
        # Visualize nutrition info with Seaborn
        st.markdown("### Nutrition Breakdown per Recipe")
        
        # Plot calories, proteins, carbs, and fats in separate charts
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        
        sns.barplot(data=nutrition_df, x="Recipe", y="Calories", ax=ax[0, 0])
        ax[0, 0].set_title("Calories per Recipe")
        
        sns.barplot(data=nutrition_df, x="Recipe", y="Protein (g)", ax=ax[0, 1], color="skyblue")
        ax[0, 1].set_title("Protein per Recipe (g)")
        
        sns.barplot(data=nutrition_df, x="Recipe", y="Carbs (g)", ax=ax[1, 0], color="lightgreen")
        ax[1, 0].set_title("Carbs per Recipe (g)")
        
        sns.barplot(data=nutrition_df, x="Recipe", y="Fats (g)", ax=ax[1, 1], color="salmon")
        ax[1, 1].set_title("Fats per Recipe (g)")
        
        plt.tight_layout()
        st.pyplot(fig)

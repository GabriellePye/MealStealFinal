import streamlit as st
import openai
import os
from dotenv import load_dotenv
 
# Load environment variables for API key
load_dotenv()
openai_key = os.getenv("openai_key")  # Retrieve the key as openai_key from .env
 
# Check if the API key loaded correctly
if not openai_key:
    st.error("API key not found. Make sure your .env file is correctly set up with 'openai_key'.")
else:
    openai.api_key = openai_key  # Initialize OpenAI API key
 
# Streamlit app setup with styling
st.markdown("""
<style>
    /* CSS styling here as per your original code */
</style>
    """, unsafe_allow_html=True)
 
# Sidebar for user input
st.sidebar.header('Preferences Hub')
age = st.sidebar.number_input('Age', min_value=10, max_value=90, value=25)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'], index=1)
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200, value=65)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300, value=170)
health_goal = st.sidebar.selectbox('Health Goal', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'], index=0)
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian'], default=['Gluten-Free', 'Vegetarian'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', 'peanuts')
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'], index=2)
body_fat_percentage = st.sidebar.number_input('Body Fat Percentage (%)', min_value=5, max_value=60, value=20)
meals_per_day = st.sidebar.selectbox('Meals Per Day', [2, 3, 4, 5], index=0)
meal_plan_duration = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)
meal_prep_time = st.sidebar.selectbox('Meal Prep Time', ['<30min', '30-60min', '>60min'], index=1)
servings = st.sidebar.number_input('Servings per recipe', min_value=1, max_value=10, value=1)
 
# Define the function to generate prompt and fetch results from OpenAI
def generate_meal_plan():
    total_meals = meals_per_day * meal_plan_duration
    dietary_preferences = ', '.join(dietary_pref)  # Convert list to string
 
    # Construct the detailed prompt based on user selections and factors
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time.lower()} and suitable for a meal plan with {meals_per_day} meals per day over {meal_plan_duration} days. "
        f"Each recipe should include a title, ingredients with quantities specifically in grams and milliliters (e.g., 100g, 250ml), cooking instructions, cuisine, diet, total cooking time, "
        f"servings (specifically for {servings} servings per recipe), estimated price in GBP (£), and full nutrition information including calories, protein, carbohydrates, and fats. "
        f"Convert all ingredient quantities to metric measurements (grams, milliliters, etc.) and avoid imperial units like cups, teaspoons, or ounces. "
        f"Consider the following user details when creating the recipes: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {health_goal}, "
        f"Dietary Preferences - {dietary_preferences}, Allergies - {allergies}, Exercise Level - {exercise_level}, Body Fat Percentage - {body_fat_percentage}%. "
    )
 
    try:
        # Call OpenAI API to generate meal plan
        client = openai.OpenAI(api_key=openai_key)  # Initialize the OpenAI client with the API key
        completion = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",  # Replace with your specific fine-tuned model ID
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500  # Set an appropriate token limit
        )
        return completion.choices[0].message.content  # Return the generated meal plan
 
    except openai.error.AuthenticationError:
        st.error("API Key is invalid or has been disabled.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
 
# Trigger the generation of the meal plan when the button is clicked
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner("Your personalized meal plan is being generated..."):
        meal_plan_output = generate_meal_plan()
        if meal_plan_output:
            st.write("### Your Generated Meal Plan:")
            st.write(meal_plan_output)  # Display the generated meal plan in Streamlit

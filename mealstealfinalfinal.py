import streamlit as st
import openai
import os
from openai import OpenAI  # Importing the OpenAI client
from dotenv import load_dotenv
 
# Load API key from Streamlit secrets
openai_key = st.secrets["openai_key"]
 
# Initialize OpenAI client with the API key
client = OpenAI(api_key=openai_key)
 
# Streamlit app setup with styling
st.markdown("""
<style>
    /* CSS styling here as per your original code */
</style>
""", unsafe_allow_html=True)
 
# Define the function to generate the prompt and fetch results using OpenAI client
def generate_meal_plan():
    # Construct the detailed prompt based on user selections and factors
    total_meals = int(meal_frequency.split()[0]) * days  # Calculate total meals
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time.lower()} and suitable for a meal plan with {meal_frequency} per day over {days} days. "
        f"Each recipe should include a title, ingredients with quantities specifically in grams and milliliters (e.g., 100g, 250ml), cooking instructions, cuisine, diet, total cooking time, "
        f"servings, estimated price in GBP (£), and full nutrition information including calories, protein, carbohydrates, and fats. "
        f"Convert all ingredient quantities to metric measurements. "
        f"Consider the following user details when creating the recipes: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {goal}, "
        f"Dietary Preferences - {', '.join(dietary_pref)}, Allergies - {allergies}, Exercise Level - {exercise_level}, Body Fat Percentage - {body_fat}%. "
    )
    try:
        # Call OpenAI API to generate meal plan using the client
        response = client.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",  # Replace with your specific fine-tuned model ID
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500  # Set an appropriate token limit
        )
        return response['choices'][0]['message']['content']  # Return the generated meal plan
 
    except openai.error.AuthenticationError:
        st.error("API Key is invalid or has been disabled.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
 
# Sidebar input for user preferences
st.sidebar.header('Preferences Hub')
st.sidebar.subheader("Basic Information")
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
meal_prep_time = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)
 
# Trigger the generation of the meal plan when the button is clicked
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner("Your personalized meal plan is being generated..."):
        meal_plan_output = generate_meal_plan()
        if meal_plan_output:
            st.write("### Your Generated Meal Plan:")
            st.write(meal_plan_output)  # Display the generated meal plan in Streamlit


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
        # Extracting content correctly from the completion object
        return response['choices'][0]['message']['content']
 
    except Exception as e:
        st.error(f"An error occurred: {e}")
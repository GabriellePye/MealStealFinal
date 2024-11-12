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
 
# Define the function to generate prompt and fetch results from OpenAI
def generate_meal_plan():
    # Construct the detailed prompt based on user selections and factors
    total_meals = int(meal_frequency.split()[0]) * days  # Convert meal frequency to a number and calculate total meals
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time.lower()} and suitable for a meal plan with {meal_frequency} per day over {days} days. "
        f"Each recipe should include a title, ingredients with quantities specifically in grams and milliliters (e.g., 100g, 250ml), cooking instructions, cuisine, diet, total cooking time, "
        f"servings, estimated price in GBP (£), and full nutrition information including calories, protein, carbohydrates, and fats. "
        f"Convert all ingredient quantities to metric measurements. "
        f"Consider the following user details when creating the recipes: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {goal}, "
        f"Dietary Preferences - {', '.join(dietary_pref)}, Allergies - {allergies}, Exercise Level - {exercise_level}, Body Fat Percentage - {body_fat}%. "
    )
    try:
        # Call OpenAI API to generate meal plan
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",  # Replace with your specific fine-tuned model ID
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500  # Set an appropriate token limit
        )
        return response['choices'][0]['message']['content']  # Return the generated meal plan
 
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


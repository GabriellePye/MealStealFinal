import streamlit as st
import openai

# OpenAI API setup (ensure you add your actual OpenAI key)
openai.api_key = 'your-api-key-here'

# Sidebar input for preferences
st.sidebar.header('Preferences Hub')
age = st.sidebar.number_input('Age', min_value=10, max_value=90)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300)
goal = st.sidebar.selectbox('Health Goal', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'])
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian', 'None'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', '')
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
activity_type = st.sidebar.multiselect('Types of Physical Activity', ['Cardio', 'Strength Training', 'Yoga/Pilates', 'Sports', 'Other'])
body_fat = st.sidebar.number_input('Body Fat Percentage (%)', min_value=5, max_value=60, value=20)
water_intake = st.sidebar.number_input('Daily Water Intake (Liters)', min_value=0.5, max_value=5.0, step=0.1)

# Meal Plan Customization
meals_per_day = st.sidebar.selectbox('Meals Per Day', ['2 meals', '3 meals', '4 meals', '5+ meals'])
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)

# Handle Button Click
if st.sidebar.button("Cook Up My Plan!"):
    # Construct the prompt dynamically based on user input
    prompt = (
        f"Provide {int(meals_per_day.split()[0]) * days} recipes that are {meal_prep.lower()} and suitable for a meal plan with {meals_per_day} meals per day over {days} days. "
        f"Each recipe should include a title, ingredients with quantities specifically in grams and milliliters (e.g., 100g, 250ml), cooking instructions, cuisine, diet, total cooking time, servings (specifically for 1 serving per recipe), estimated price in GBP (£), and full nutrition information including calories, protein, carbohydrates, and fats. "
        f"Convert all ingredient quantities to metric measurements (grams, milliliters, etc.) and avoid imperial units like cups, teaspoons, or ounces. "
        f"Consider the following user details when creating the recipes: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {goal}, "
        f"Dietary Preferences - {', '.join(dietary_pref)}, Allergies - {allergies}, Exercise Level - {exercise_level}, Body Fat Percentage - {body_fat}%. "
    )

    # Make the API call to OpenAI
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Replace with your model ID if fine-tuned
            prompt=prompt,
            max_tokens=1000,  # You can adjust this value depending on the response size you expect
            temperature=0.7
        )

        # Extract the generated meal plan
        meal_plan = response.choices[0].text.strip()

        # Display the meal plan in the front-end
        st.subheader("Your Personalized Meal Plan")
        st.write(meal_plan)

    except Exception as e:
        st.error("Error generating meal plan. Please try again.")
        st.write(str(e))

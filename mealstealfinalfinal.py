## original code 
import streamlit as st
import pandas as pd
import numpy as np

# -------------------------
# 1. Background, containers, styling
# -------------------------

# CSS styles

st.markdown("""
<style>
/* background */
.stApp {
    background: url('https://i.ibb.co/MpbbQDx/meal-steal-bg.gif'); /*need to import better gif */
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
    max-width: 80%;  /* Adjusted for centering */
    margin: 0 auto;
}

.subheader-container img { 
    width: 300px;
}

/* Flex container for logo and subheader */
.header-container {
    display: flex;
    align-items: left; /* Center vertically */
    justify-content: left; /* Center horizontally */
    margin: 20px; /* Add some margin */
}

/* Styling for the logo */
.header-container img { 
    width: 100px; /* Adjust width for the logo */
    margin-right: 20px; /* Space between logo and subheader */
}

/* styling for tabs */
.stTabs [role='tab'] {
    border: 2px solid white;
    backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    width: fit-content;  /* Allows the tab box to resize based on text content */
    margin: 0 5px;
    white-space: nowrap;  /* Prevents text from wrapping within the tab */
}

/* Tab panel styling to have a frosted effect */
.stTabs [role="tabpanel"] {
    border: 2px solid white;
    backdrop-filter: blur(20px);  /* Frosted effect */
    background: rgba(255, 255, 255, 0.1);  /* Background with slight opacity */
    padding: 20px;  /* Padding for content */
    border-radius: 10px;  /* Rounded corners */
    color: #DAD7CD;  /* Light text color */
}

/* General styles for meal plan section */
.meal-plan-section {
    margin-top: 20px; /* Space above meal plan section */
    padding: 20px; /* Padding for content */
    border-radius: 10px; /* Rounded corners */
    backdrop-filter: blur(20px); /* Frosted effect */
    background: rgba(255, 255, 255, 0.1); /* Slightly transparent background */
    color: #DAD7CD; /* Light text color */
}

/* Cards for meal plan (existing styles removed) */
.card {
    position: relative;
    width: 160px; /* Adjust width as needed */
    height: 220px; /* Adjust height as needed */
    background: #335D3B;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;  /* Font size of text in the card */
    font-weight: bold;
    border-radius: 15px;
    cursor: pointer;
    transition: all 0.5s; /* Smooth transitions */
    margin: 5px;  /* Smaller gap between cards */
}

/* Styling for card hover effects */
.card::before,
.card::after {
    position: absolute;
    content: "";
    width: 20%;
    height: 20%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;  /* Font size for hover text */
    font-weight: bold;
    background-color: #67944C;
    transition: all 0.5s; /* Smooth transitions */
}

.card::before {
    top: 0;
    right: 0;
    border-radius: 0 15px 0 100%; /* Top right corner rounded */
}

.card::after {
    bottom: 0;
    left: 0;
    border-radius: 0 100% 0 15px; /* Bottom left corner rounded */
}

/* Hover effects for cards */
.card:hover::before,
.card:hover::after {
    width: 100%; /* Expand on hover */
    height: 100%; /* Expand on hover */
    border-radius: 15px; /* Rounded corners on hover */
}

.card:hover:after {
    content: "Meal Plan"; /* Show meal plan text on hover */
    color: #DAD7CD; /* Text color for visibility */
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #335D3B;
    color: #DAD7CD;
}

.stTabs [role="tabpanel"] {
    margin-top: 20px;  /* Adjust this value to create a gap */
}

</style>
""", unsafe_allow_html=True)

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

# Submit Button with a Friendly Name
if st.sidebar.button("Cook Up My Plan!"):
    st.write("Your personalized meal plan is being generated based on your preferences!") ##remove 
    # Add any additional code here to handle the generation of the meal plan

# -------------------------
# 4. Tabs
# -------------------------

st.markdown('<div class="content-section">', unsafe_allow_html=True)  # Container for the tabs

tab1, tab2, tab3, tab4 = st.tabs(['Your Meal Plan', 'Adjust Your Plan', 'Recipes', 'Nutritional Info'])

# -------------------------
# 5. Meal Plan Tab & Page
# -------------------------

with tab1:
    st.markdown('<h2 style="text-align: center;">Your Personalized Meal Plan</h2>', unsafe_allow_html=True)

    # Sample meal plan with mock data
    meal_plan = {
        'Day 1': ['Oatmeal with fruit', 'Grilled chicken salad', 'Apple', 'Quinoa with veggies'],
        'Day 2': ['Greek yogurt with honey', 'Turkey sandwich', 'Carrot sticks', 'Salmon with rice'],
        'Day 3': ['Smoothie', 'Pasta with tomato sauce', 'Nuts', 'Stir-fried tofu with broccoli'],
        'Day 4': ['Eggs and toast', 'Chickpea salad', 'Granola bar', 'Beef stir-fry'],
        'Day 5': ['Pancakes', 'Veggie wrap', 'Yogurt', 'Baked chicken with potatoes'],
        'Day 6': ['Cereal with milk', 'Quinoa salad', 'Fruit', 'Fish tacos'],
        'Day 7': ['Toast with avocado', 'Rice and beans', 'Dark chocolate', 'Grilled shrimp with veggies'],
    }

    # Render cards based on slider selection
    day_count = min(days, len(meal_plan))
    cols = st.columns(3)  # Create three columns

    # Placeholder for displaying selected meal
    selected_meal = st.empty() 

    for idx, (day, meals) in enumerate(meal_plan.items()):
        if idx < day_count:  # Only show the selected number of days
            with cols[idx % 3]:  # Distribute the days across columns
                # Render the card using HTML
                st.markdown(f"""
                <div class="card" style="cursor: pointer;">
                    <div class="card-content">
                        <h3 style="font-size: 15px;">{day}</h3>
                        <p style="font-size: 15px;">Click to see meals</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -------------------------
# 6. Adjust Your Meal Plan - placeholder
# -------------------------

with tab2:
    st.subheader('Adjust Your Meal Plan')
    st.write('Fill in later. Be sure to include *if possible click and drop options')

# -------------------------
# 7. Recipes - placeholder
# -------------------------

with tab3:
    st.subheader('Recipes')
    st.write('Fill in later - maybe have meal plan for the days on side with drop down options (or above) and then you can choose recipes to view?')

# -------------------------
# 8. Nutritional Info - placeholder 
# -------------------------

with tab4:
    st.subheader('Nutritional Info')
    st.write('Fill in later. Collate information for the whole meal plan or for certain meals/days?')

# ----
# 9. Close container
# ----

st.markdown('</div>', unsafe_allow_html=True)  # Close the frosted container

# ----
# 10.Footer
# ----

st.markdown("""
    <footer>
        <p style="text-align: center; color: #DAD7CD;">© 2024 Meal Steal. All rights reserved.</p>
    </footer>
""", unsafe_allow_html=True)
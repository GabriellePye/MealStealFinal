# libraries
import streamlit as st
import openai
import pandas as pd
import numpy as np #-- added numpy
import matplotlib.pyplot as plt
from openai import OpenAI
import re
from fpdf import FPDF #-- added pdf 
import io

# Initialize OpenAI client
openai.api_key = st.secrets["openai_key"]
client = OpenAI(api_key=st.secrets["openai_key"])

# Function to generate PDF of the recipes
def generate_pdf(recipes_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title of the PDF
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Your Meal Plan", ln=True, align="C")

    # Add a line break
    pdf.ln(10)

    # Content of the meal plan (recipes_text)
    pdf.set_font("Arial", size=12)

    # Add the recipes text to the PDF
    pdf.multi_cell(0, 10, recipes_text)

    # Save the PDF to an in-memory file
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)  # Rewind to the beginning of the file
    return pdf_output

# -------------------------
# 1. Background, containers, styling
# -------------------------

# CSS styles
st.markdown("""
<style>
/* background */
.stApp {
    background: url('https://i.ibb.co/MpbbQDx/meal-steal-bg.gif') 
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
# 3. User input form/sidebar + AI prompt generator
# -------------------------

# Sidebar Main Header and Introductory Statement
st.sidebar.header('User Hub')
st.sidebar.markdown("Fill out as many or as few details as you’d like. Choices with * are required, the rest are optional.") #-- changed title and desc

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
st.sidebar.subheader("Meal Plan Customisation")
meal_frequency = st.sidebar.selectbox('Meals Per Day', ['1 meal', '2 meals', '3 meals', '4 meals']) #-- adjusted meal servings
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
servings = st.sidebar.number_input('Number of Servings per Recipe', min_value=1, max_value=4, value=2) #-- changed 10 max to 4
days = st.sidebar.slider('Meal Plan Duration (days)', 1, 7, 7)

# Function to Generate Recipes with OpenAI
@st.cache_data
def generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meals_per_day, days, meal_prep, servings):
    total_meals = int(meals_per_day.split()[0]) * days
    dietary_preferences = ', '.join(dietary_pref)
    meal_prep_time = meal_prep.lower()
    prompt = (
        f"Provide {total_meals} recipes that are {meal_prep_time} and suitable for a meal plan with {meals_per_day} per day over {days} days. "
        f"Each recipe should be formatted exactly as shown below, with each field clearly labeled and on a new line. "
        f"The output should be in the following format for consistency:\n\n"
        
        "### Recipe X\n"
        "**Title**: [Recipe Title]\n"
        "**Ingredients**: \n- Ingredient 1 (amount)\n- Ingredient 2 (amount)\n...\n"
        "**Instructions**: \n1. Step 1\n2. Step 2\n...\n"
        "**Cuisine**: [Cuisine Type]\n"
        "**Diet**: [Diet Type]\n"
        "**Total Cooking Time**: [Time in minutes]\n"
        "**Servings**: [Number of servings]\n"
        "**Estimated Price**: £[Price]\n"
        "**Nutrition**:\n"
        "Calories: [Amount] kcal\n"
        "Carbohydrates: [Amount] g\n"
        "Fat: [Amount] g\n"
        "Protein: [Amount] g\n\n"
        
        f"Consider the following user details: Age - {age}, Gender - {gender}, Weight - {weight} kg, Height - {height} cm, Health Goal - {goal}, "
        f"Dietary Preferences - {dietary_preferences}, Allergies - {allergies}, Exercise Level - {exercise_level}. "
        "All fields are mandatory; if information is unavailable, write 'N/A'. Please follow the format exactly without adding or omitting any fields.\n\n"
    )
    
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",  # Replace with your fine-tuned model ID
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

# Parse nutrition info from generated recipes
@st.cache_data
def parse_nutrition_info(recipes_text):
    data = {
        "Recipe": [],
        "Calories": [],
        "Carbohydrates": [],
        "Fat": [],
        "Protein": []
    }

    # Split recipes based on "### Recipe" occurrences
    recipe_sections = re.split(r"### Recipe \d+", recipes_text)[1:]

    for section in recipe_sections:
        # Extract title
        title_match = re.search(r"\*\*Title\*\*:\s*([^\n]+)", section)
        title = title_match.group(1).strip() if title_match else "Unknown Recipe"
        data["Recipe"].append(title)

        # Use regex to capture specific nutrition values
        calories = re.search(r"Calories:\s*([\d.]+)\s*kcal", section)
        carbohydrates = re.search(r"Carbohydrates:\s*([\d.]+)\s*g", section)
        fat = re.search(r"Fat:\s*([\d.]+)\s*g", section)
        protein = re.search(r"Protein:\s*([\d.]+)\s*g", section)

        # Append parsed values, defaulting to 0 if not found
        data["Calories"].append(float(calories.group(1)) if calories else 0.0)
        data["Carbohydrates"].append(float(carbohydrates.group(1)) if carbohydrates else 0.0)
        data["Fat"].append(float(fat.group(1)) if fat else 0.0)
        data["Protein"].append(float(protein.group(1)) if protein else 0.0)

    return pd.DataFrame(data)

# Trigger recipe generation #-- need to put this within the box
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner('Creating your personalised plan...'):
        recipes_text = generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meal_frequency, days, meal_prep, servings)
    st.success("Your personalised meal plan is ready!")

# -------------------------
# 4. Tabs
# -------------------------

st.markdown('<div class="content-section">', unsafe_allow_html=True)  # Container for the tabs

tab1, tab2, tab3, tab4 = st.tabs(['Your Meal Plan', 'Adjust Your Plan', 'Recipes', 'Nutritional Dashboard'])

# -------------------------
# 5. Meal Plan Tab & Page
# -------------------------

with tab1:
    st.markdown('<h2 style="text-align: center;">Your Personalised Meal Plan</h2>', unsafe_allow_html=True)

# -------------------------
# 6. Adjust Your Meal Plan 
# -------------------------

with tab2:
    st.markdown("### Adjust Your Meal Plan")
    
    if 'recipes_text' in locals() and recipes_text:  # Check if recipes_text is available
        st.write(recipes_text)  # Display full meal plan text as a large block

        # Button to download the PDF
        if st.button("Download Full Recipes as PDF"):
            # Generate PDF
            pdf_output = generate_pdf(recipes_text)

            # Provide the download link
            st.download_button(
                label="Download PDF",
                data=pdf_output,
                file_name="meal_plan.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Your personalised meal plan is not ready yet. Please generate it first.")
        
# -------------------------
# 7. Recipes
# -------------------------

    # Tab 3: Individual Recipes (Collapsible sections)
    with tab3:
        st.markdown("### Recipes")

# -------------------------
# 8. Nutritional Dashboard
# -------------------------

    # Tab 4: Nutrition Dashboard
    with tab4:
        st.markdown("### Nutrition Breakdown")

        # Parse nutrition info from recipes text
        nutrition_df = parse_nutrition_info(recipes_text)

        # Display the entire DataFrame
        st.write("**Nutrition Data for All Recipes**")
        st.dataframe(nutrition_df)
        
        # Define color scheme based on your provided colors
        color_scheme = ["#335D3B", "#67944C", "#A3B18A"]
        nutrients_for_pie = ["Protein", "Carbohydrates", "Fat"]

        # Dropdown to filter recipes
        selected_recipe = st.selectbox(
            "Select Recipe to View Nutrient Distribution",
            options=["Total"] + nutrition_df["Recipe"].unique().tolist(),
            index=0  # Default to "Total" for all recipes
        )

        # Filter data based on selected recipe
        filtered_data = nutrition_df if selected_recipe == "Total" else nutrition_df[nutrition_df["Recipe"] == selected_recipe]

        # Sum the selected nutrients
        nutrient_totals = filtered_data[nutrients_for_pie].apply(pd.to_numeric, errors='coerce').sum()

        # Ensure there are values to plot
        if nutrient_totals.sum() > 0:
            # Matplotlib Donut Chart with Custom Colors
            fig, ax = plt.subplots()
            wedges, texts = ax.pie(
                nutrient_totals,
                labels=[f"{nutrient} ({value}g)" for nutrient, value in zip(nutrients_for_pie, nutrient_totals)],
                startangle=90,
                colors=color_scheme,
                wedgeprops=dict(width=0.3)  # Creates a donut effect by setting width
            )

            # Adding the legend for each nutrient
            ax.legend(
                labels=[f"{nutrient}: {value}g" for nutrient, value in zip(nutrients_for_pie, nutrient_totals)],
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                facecolor='white'
            )

            # Adding the donut hole
            centre_circle = plt.Circle((0, 0), 0.40, fc='white')
            fig.gca().add_artist(centre_circle)
            ax.set_title(f"Nutrient Distribution for {'All Recipes' if selected_recipe == 'Total' else selected_recipe}")

            # Display the chart in Streamlit
            st.pyplot(fig)
        else:
            st.write("No nutrient data to display for the selected recipe.")

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
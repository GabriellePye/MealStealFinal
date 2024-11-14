#new code as of 9:44 

# -------------------------
# 0. Libraries & Functions
# -------------------------

import streamlit as st
import openai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI
import re
from fpdf import FPDF
import io

# Initialize OpenAI client
openai.api_key = st.secrets["openai_key"]
client = OpenAI(api_key=st.secrets["openai_key"])

from fpdf import FPDF
import io

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

    # Set font for content
    pdf.set_font("Arial", size=12)

    # Loop through each recipe in the recipes_text
    for recipe in recipes_text:
        # Recipe Title
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(200, 10, txt=recipe["Title"], ln=True, align="L")
        pdf.ln(4)

        # Key details (Cuisine, Diet, Cooking Time, Servings, Price)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Cuisine: {recipe['Cuisine']}", ln=True)
        pdf.cell(200, 10, txt=f"Diet: {recipe['Diet']}", ln=True)
        pdf.cell(200, 10, txt=f"Total Cooking Time: {recipe['Total Cooking Time']}", ln=True)
        pdf.cell(200, 10, txt=f"Servings: {recipe['Servings']}", ln=True)
        pdf.cell(200, 10, txt=f"Estimated Price: {recipe['Estimated Price']}", ln=True)
        pdf.ln(6)

        # Ingredients
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Ingredients:", ln=True)
        pdf.set_font("Arial", size=12)
        for ingredient in recipe["Ingredients"]:
            pdf.cell(200, 10, txt=f"- {ingredient}", ln=True)
        pdf.ln(6)

        # Instructions
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Instructions:", ln=True)
        pdf.set_font("Arial", size=12)
        for i, instruction in enumerate(recipe["Instructions"], 1):
            pdf.cell(200, 10, txt=f"{i}. {instruction}", ln=True)
        pdf.ln(6)

        # Nutrition
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Nutrition:", ln=True)
        pdf.set_font("Arial", size=12)
        for nutrient, amount in recipe["Nutrition"].items():
            pdf.cell(200, 10, txt=f"{nutrient}: {amount}", ln=True)
        pdf.ln(10)  # Add space before next recipe

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
    background: url('https://i.ibb.co/1X0yWSJ/oliver-guhr-Qs3-ALnjkw-F4-unsplash.jpg');
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

/* Tooltip Styling */
.tooltip {
    position: absolute;
    background-color: #335D3B; /* Background color */
    color: #DAD7CD; /* Text color */
    padding: 8px 16px; /* Adjust the padding for a less tall tooltip */
    border-radius: 8px;
    font-size: 14px;
    max-width: 250px; /* Adjust width to make the tooltip longer */
    width: auto; /* Allow the width to expand based on content */
    text-align: center;
    white-space: nowrap;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.3s ease, visibility 0.3s ease;
    z-index: 9999;
}

.tooltip.visible {
    visibility: visible;
    opacity: 1;
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
st.sidebar.markdown("Fill out as many details as you would like. Choices with * are required fields.") #-- changed desc

# Basic Demographic Information
st.sidebar.subheader("Basic Information")
age = st.sidebar.number_input('Age', min_value=10, max_value=90)
gender = st.sidebar.selectbox('Gender Identity', ['Male', 'Female', 'Trans'])
weight = st.sidebar.number_input('Weight (kg)', min_value=30, max_value=200)
height = st.sidebar.number_input('Height (cm)', min_value=120, max_value=300)

# Health Goals and Dietary Preferences
st.sidebar.subheader("Health Goals & Dietary Preferences")
goal = st.sidebar.selectbox('Health Goal *', ['Weight Loss', 'Maintain Weight', 'Muscle Gain', 'Eat Healthier', 'Create Meal Routine'])
dietary_pref = st.sidebar.multiselect('Dietary Preferences', ['Vegetarian', 'Vegan', 'Halal', 'Gluten-Free', 'Dairy-Free', 'Pescetarian', 'None'])
allergies = st.sidebar.text_input('Allergies (comma-separated)', '')

# Physical Activity and Exercise Details
st.sidebar.subheader("Physical Activity")
exercise_level = st.sidebar.selectbox('Exercise Level', ['Sedentary', 'Lightly Active', 'Active', 'Very Active'])
activity_type = st.sidebar.multiselect('Types of Physical Activity', ['Cardio', 'Strength Training', 'Yoga/Pilates', 'Sports', 'Other'])

# Meal Plan Customization
st.sidebar.subheader("Meal Plan Customisation")
meal_frequency = st.sidebar.selectbox('Meals Per Day *', ['1 meal', '2 meals', '3 meals', '4 meals']) 
meal_prep = st.sidebar.selectbox('Meal Prep Time', ['Minimal (quick recipes)', 'Moderate (30-60 mins)', 'Detailed (complex recipes)'])
servings = st.sidebar.number_input('Number of Servings per Recipe *', min_value=1, max_value=4, value=2) 
days = st.sidebar.slider('Meal Plan Duration (days) *', 1, 7, 7)

# Function to Generate Recipes with OpenAI
@st.cache_data
def generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meals_per_day, days, meal_prep, servings):
    total_meals = int(meals_per_day.split()[0]) * days
    dietary_preferences = ', '.join(dietary_pref)
    meal_prep_time = meal_prep.lower()
    prompt = (
        f"Generate {total_meals} unique, full meal recipes that are {meal_prep_time} and suitable for a meal plan with {meals_per_day} per day over {days} days. "
        f"Each recipe should be a complete meal (no snacks, beverages, or single small dishes), formatted exactly as shown below. "
        f"Use only metric units (grams, milliliters, etc.) and avoid mentioning any brand names or specific product recommendations. "
        f"Adjust each recipe to yield {servings} servings. Follow concise, cost-effective instructions.\n\n"
        
        "### Recipe X\n"
        "**Title**: [Recipe Title]\n"
        "**Ingredients**: \n- Ingredient 1 (amount in grams or milliliters)\n- Ingredient 2 (amount in grams or milliliters)\n...\n"
        "**Instructions**: \n1. Step 1\n2. Step 2\n...\n"
        "**Cuisine**: [Cuisine Type or N/A]\n"
        "**Diet**: [Diet Type or N/A]\n"
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
        "Ensure that each recipe uses all fields as specified. If information is unavailable, write 'N/A' for that field. Follow the format precisely without any deviations.\n\n"
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

@st.cache_data
def parse_recipe_info(recipes_text):
    recipes_data = []

    # Split the text by recipe sections
    recipe_sections = re.split(r"### Recipe \d+", recipes_text)[1:]

    for section in recipe_sections:
        # Parse each part of the recipe using regular expressions
        title = re.search(r"\*\*Title\*\*:\s*([^\n]+)", section)
        ingredients = re.findall(r"\- ([^\n]+)", section)
        instructions = re.findall(r"\d+\.\s([^\n]+)", section)
        cuisine = re.search(r"\*\*Cuisine\*\*:\s*([^\n]+)", section)
        diet = re.search(r"\*\*Diet\*\*:\s*([^\n]+)", section)
        cooking_time = re.search(r"\*\*Total Cooking Time\*\*:\s*([^\n]+)", section)
        servings = re.search(r"\*\*Servings\*\*:\s*([^\n]+)", section)
        price = re.search(r"\*\*Estimated Price\*\*:\s*£([^\n]+)", section)
        calories = re.search(r"Calories:\s*([\d.]+)\s*kcal", section)
        carbohydrates = re.search(r"Carbohydrates:\s*([\d.]+)\s*g", section)
        fat = re.search(r"Fat:\s*([\d.]+)\s*g", section)
        protein = re.search(r"Protein:\s*([\d.]+)\s*g", section)

        # Append the recipe information in a dictionary
        recipes_data.append({
            "Title": title.group(1).strip() if title else "Unknown Recipe",
            "Ingredients": ingredients,
            "Instructions": instructions,
            "Cuisine": cuisine.group(1).strip() if cuisine else "N/A",
            "Diet": diet.group(1).strip() if diet else "N/A",
            "Total Cooking Time": cooking_time.group(1).strip() if cooking_time else "N/A",
            "Servings": servings.group(1).strip() if servings else "N/A",
            "Estimated Price": f"£{price.group(1).strip()}" if price else "N/A",
            "Nutrition": {
                "Calories": f"{calories.group(1).strip()} kcal" if calories else "N/A",
                "Carbohydrates": f"{carbohydrates.group(1).strip()} g" if carbohydrates else "N/A",
                "Fat": f"{fat.group(1).strip()} g" if fat else "N/A",
                "Protein": f"{protein.group(1).strip()} g" if protein else "N/A",
            }
        })

    return recipes_data

# Trigger recipe generation
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner('Creating your personalised plan...'):
        recipes_text = generate_recipes(age, gender, weight, height, goal, dietary_pref, allergies, exercise_level, meal_frequency, days, meal_prep, servings)
    st.session_state["recipes_text"] = recipes_text  # Store the result in session state
    st.success("Your personalised meal plan is ready!")

# Initialize selected_recipe in session state if it does not exist
if "selected_recipe" not in st.session_state:
    st.session_state["selected_recipe"] = "Total"  # Default to "Total"
    
# -------------------------
# 4. Tabs
# -------------------------

if "recipes_text" in st.session_state:
    recipes_text = st.session_state["recipes_text"]
    nutrition_df = parse_nutrition_info(recipes_text)

st.markdown('<div class="content-section">', unsafe_allow_html=True)  # Container for the tabs

tab1, tab2, tab3, tab4 = st.tabs(['About Meal Steal', 'Your Meal Plan', 'Recipes', 'Nutritional Dashboard'])

# -------------------------
# 5. About Meal Steal
# -------------------------

import streamlit as st

# Tab 1: Main description and key features
with tab1:
    # Center the main heading
    st.markdown('<h2 style="text-align: center;">Welcome to Meal Steal - Your AI Personalised Meal Plan!</h2>', unsafe_allow_html=True)

    # Add app description
    st.write("Meal Steal is your personalised meal planner powered by AI. Simply input your preferences into our user hub on the left, and our AI creates custom recipes tailored to your needs. Explore each recipe in detail, track your nutrition intake with our dashboard, and easily download your meal plan as a PDF. Let us help you plan healthier meals with ease!")
    
    # Key Features content in Markdown format
    features_content = """
    **Key Features 🎉:**

    - **Personalised Recipes**: Submit your preferences, and our AI will craft recipes just for you, ensuring each meal aligns with your nutritional needs.
    - **In-Depth Recipe Exploration**: Explore individual recipes in detail through the tabs, where you can adjust portions, view ingredients, and read preparation steps.
    - **Nutrition Dashboard**: Visualize your daily and weekly nutrition intake with our interactive dashboard, helping you stay on track with your dietary goals.
    - **Downloadable Meal Plans**: Conveniently download your entire meal plan as a PDF for easy reference and use in the kitchen.
    """
    
    # Display the content directly in Streamlit using st.write (Markdown supported)
    st.write(features_content)

    # Disclaimer Button with Hover Effect (Inside a Section with Background Styling)
    st.markdown("""
        <div class="section-background">
            <div class="tooltip">
                <span>📜 Disclaimer</span>
                <div class="tooltiptext">
                    <strong>Meal Steal Disclaimer:</strong><br><br>
                    Meal Steal provides meal planning and grocery budgeting information for general informational purposes only. 
                    While we strive to provide accurate nutritional data and cost estimates, Meal Steal does not guarantee the accuracy, 
                    completeness, or reliability of any information provided. Users should consult a healthcare professional before making any dietary 
                    changes based on the recommendations in this app. Grocery prices and product availability may vary by store location and time, 
                    and we cannot guarantee real-time accuracy. By using this app, you acknowledge and accept that Meal Steal is not responsible 
                    for any dietary, health, or financial outcomes arising from the use of the information provided.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# 6. Your Meal Plan
# -------------------------

with tab2:
    st.markdown("### Your Meal Plan")
    
    # Check if recipes_text is available in session_state
    if 'recipes_text' in st.session_state and st.session_state['recipes_text']:
        st.write(st.session_state['recipes_text'])  # Display full meal plan text as a large block
   
# -------------------------
# 7. Recipes
# -------------------------

# Tab 3: Individual Recipes (Collapsible sections)
with tab3:
    st.markdown("### Recipes")

    if "recipes_text" in st.session_state:
        # Parse the recipe information
        recipes_data = parse_recipe_info(st.session_state["recipes_text"])

        # Display each recipe in a collapsible format
        for recipe in recipes_data:
            with st.expander(recipe["Title"]):
                # Display key details above ingredients and instructions
                st.write(f"**Cuisine**: {recipe['Cuisine']}")
                st.write(f"**Diet**: {recipe['Diet']}")
                st.write(f"**Total Cooking Time**: {recipe['Total Cooking Time']}")
                st.write(f"**Servings**: {recipe['Servings']}")
                st.write(f"**Estimated Price**: {recipe['Estimated Price']}")

                # Display ingredients
                st.write("**Ingredients:**")
                for ingredient in recipe["Ingredients"]:
                    st.write(f"- {ingredient}")

                # Display instructions
                st.write("**Instructions:**")
                for i, instruction in enumerate(recipe["Instructions"], 1):
                    st.write(f"{i}. {instruction}")

                # Display nutrition
                st.write("**Nutrition:**")
                for nutrient, amount in recipe["Nutrition"].items():
                    st.write(f"{nutrient}: {amount}")

    else:
        st.warning("Your personalised meal plan is not ready yet. Please generate it first.")

        # Button to download the PDF only when recipe data is available
        if "recipes_text" in st.session_state:
            if st.button("Download Full Recipes as PDF"):
                # Generate PDF from the session state data
                pdf_output = generate_pdf(st.session_state["recipes_text"])

                # Provide the download link for the PDF
                st.download_button(
                    label="Download Full Recipes as PDF",
                    data=pdf_output,
                    file_name="meal_plan.pdf",
                    mime="application/pdf"
                )

# -------------------------
# 8. Nutritional Dashboard
# -------------------------

# Tab 4: Nutrition Dashboard
with tab4:
    if "recipes_text" in st.session_state:
        recipes_text = st.session_state["recipes_text"]
        nutrition_df = parse_nutrition_info(recipes_text)

        # Display the entire DataFrame
        st.write("**Nutrition Data for All Recipes**")
        st.dataframe(nutrition_df)

        # Color scheme and nutrients for pie chart
        color_scheme = ["#335D3B", "#67944C", "#A3B18A"]
        nutrients_for_pie = ["Protein", "Carbohydrates", "Fat"]

        # Dropdown to filter recipes, bound to session state
        selected_recipe = st.selectbox(
            "Select Recipe to View Nutrient Distribution",
            options=["Total"] + nutrition_df["Recipe"].unique().tolist(),
            index=0,  # Default to "Total" for all recipes
            key="selected_recipe"  # Bind to session state
        )

        # Filter data based on selected recipe
        filtered_data = nutrition_df if st.session_state["selected_recipe"] == "Total" else nutrition_df[nutrition_df["Recipe"] == st.session_state["selected_recipe"]]

        # Sum the selected nutrients
        nutrient_totals = filtered_data[nutrients_for_pie].apply(pd.to_numeric, errors='coerce').sum()

        # Ensure there are values to plot
        if nutrient_totals.sum() > 0:
            fig, ax = plt.subplots()
            wedges, texts = ax.pie(
                nutrient_totals,
                labels=[f"{nutrient} ({value:.1f}g)" for nutrient, value in zip(nutrients_for_pie, nutrient_totals)],
                startangle=90,
                colors=color_scheme,
                wedgeprops=dict(width=0.3)
            )

            ax.legend(
                labels=[f"{nutrient}: {value:.1f}g" for nutrient, value in zip(nutrients_for_pie, nutrient_totals)],
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                facecolor='white'
            )

            centre_circle = plt.Circle((0, 0), 0.40, fc='white')
            fig.gca().add_artist(centre_circle)
            ax.set_title(f"Nutrient Distribution for {'All Recipes' if st.session_state['selected_recipe'] == 'Total' else st.session_state['selected_recipe']}")

            st.pyplot(fig)
        else:
            st.write("No nutrient data to display for the selected recipe.")
    else:
        st.warning("Your personalised meal plan is not ready yet. Please generate it first.")


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
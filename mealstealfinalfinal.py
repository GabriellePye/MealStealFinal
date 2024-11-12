import streamlit as st
import openai
 
# Access the API key from Streamlit secrets
openai_key = st.secrets["OPENAI_API_KEY"]
 
# Initialize OpenAI API key
openai.api_key = openai_key
 
# Rest of your Streamlit code...
def generate_meal_plan():
    # Construct your prompt as before
    prompt = (
        f"Provide 14 recipes that are quick to prepare..."
        # Continue the rest of your prompt here
    )
    try:
        # Use OpenAI to generate the meal plan
        response = openai.ChatCompletion.create(
            model="ft:gpt-4o-mini-2024-07-18:personal::ASMltAf2",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
 
    except openai.error.AuthenticationError:
        st.error("API Key is invalid or has been disabled.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
 
# Button to trigger the generation of the meal plan
if st.sidebar.button("Cook Up My Plan!"):
    with st.spinner("Your personalized meal plan is being generated..."):
        meal_plan_output = generate_meal_plan()
        if meal_plan_output:
            st.write("### Your Generated Meal Plan:")
            st.write(meal_plan_output)


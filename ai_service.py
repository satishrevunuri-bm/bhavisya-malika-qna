import streamlit as st
from google import genai

# --- ENVIRONMENT SETUP (Smart Switch) ---
try:
    # ☁️ CLOUD MODE (Runs when deployed on the internet)
    api_key = st.secrets["GEMINI_API_KEY"]
    model_name = "gemini-2.5-flash"  # <-- Type your exact model name here!
except:
    # 💻 LOCAL MODE (Runs when testing on your computer)
    import app_config
    api_key = app_config.API_KEY
    model_name = app_config.MODEL_NAME

client = genai.Client(api_key=api_key)

def generate_summary(user_query, top_results_df):
    context_text = ""
    for index, row in top_results_df.iterrows():
        context_text += f"Question: {row['Question']}\nAnswer: {row['Answer']}\n\n"

    prompt = f"""
    You are a spiritual assistant summarizing the teachings of Pandit Dr. Kashinath Mishra regarding the Bhavishya Malika.
    Based ONLY on the provided Q&As below, answer the user's query. 
    Write a fluent, easy-to-read summary, crispe but entire context covered. If the Q&As do not contain the answer, politely state that the specific information was not found in the selected Q&As.
    
    User Query: {user_query}
    
    Q&As:
    {context_text}
    """

    try:
        response = client.models.generate_content(
            model=model_name, 
            contents=prompt
        )
        return response.text, None # Return text and No Error
    except Exception as e:
        return None, str(e) # Return No Text and the Error Message
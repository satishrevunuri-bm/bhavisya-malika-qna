import streamlit as st
import search_engine as se
import ai_service as ai
import ui_components as ui
import os

# --- SETUP PAGE & UI ---
st.set_page_config(page_title="Bhavishya Malika Q&As", page_icon="🕉️", layout="wide")
ui.inject_theme()
ui.render_headers()

# --- LOAD DATA & INDEX ---
df = se.load_data()
bm25_index = se.build_search_index(df)

# --- SEARCH INTERFACE ---
with st.form(key="search_form"):
    user_query = st.text_input("What would you like to know?", placeholder="e.g., Where will the devotees meet Kalki?")
    submit_button = st.form_submit_button(label="Search")

if submit_button and user_query:
    
    # Run the search via the engine module
    all_results, is_valid_query = se.perform_search(user_query, df, bm25_index)
    
    if not is_valid_query:
        st.warning("Please enter more specific keywords to search.")
    elif all_results.empty:
        st.warning("No specific answers found for that query. Try using different keywords.")
    else:
        # --- 1. SET UP COLUMNS & CONTAINERS ---
        # Make the AI column (left) standard width, and Q&A column (right) slightly wider
        col_left, col_right = st.columns([1, 1.5]) 
        
        # We create containers inside the columns. 
        # This is a magic trick that lets us render the right side BEFORE the left side!
        ai_container = col_left.container()
        qa_container = col_right.container()

        # --- RIGHT COLUMN: Q&A MATCHES (Rendered FIRST for instant load!) ---
        with qa_container:
            st.markdown(f'<h2 class="section-header">📚 Q&A ({len(all_results)} Matches)</h2>', unsafe_allow_html=True)
            
            display_results = all_results
            
            for index, row in display_results.iterrows():
                ui.render_qa_card(row) 
                
        # --- LEFT COLUMN: AI SUMMARY (Rendered SECOND) ---
        with ai_container:
            st.markdown('<h2 class="section-header">✨ AI Summary</h2>', unsafe_allow_html=True)
            
            with st.spinner("AI is reading the top matches and writing a summary..."):
                top_17 = all_results.head(17)
                summary_text, error = ai.generate_summary(user_query, top_17)
                
                if error:
                    # Graceful warning if API limits are hit
                    st.warning("⚠️ The AI summary is currently unavailable due to high traffic or API limits. Please refer to the detailed Q&As on the right!")
                else:
                    st.markdown(f'<div class="ai-summary-container">{summary_text}</div>', unsafe_allow_html=True)
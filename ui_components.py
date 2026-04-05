import streamlit as st
import base64
import os

def inject_theme():
    st.markdown("""
    <style>
        .main-title { color: #D4AF37; text-align: center; margin-bottom: 0px; }
        .sub-title { color: #003882; text-align: center; font-size: 1.1rem; margin-bottom: 30px; }
        
        .ai-summary-container {
            border: 2px solid #D4AF37; padding: 20px; border-radius: 8px;
            background-color: #FFFCF5; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        }
        .section-header {
            color: #003882; border-bottom: 2px solid #D4AF37;
            padding-bottom: 8px; margin-bottom: 15px; font-weight: bold;
        }
        
        .qa-card {
            border-left: 5px solid #003882; border-radius: 5px; padding: 15px;
            margin-bottom: 15px; background-color: #F8F9FA;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        }
        .qa-question { color: #003882; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px; }
        .qa-answer { color: #014122; font-size: 1.09rem; margin-bottom: 15px; line-height: 1.6; }
        .qa-meta { color: #996515; font-size: 0.9rem; font-style: italic; border-top: 1px solid #e0e0e0; padding-top: 8px; }
        .qa-link { color: #003882; text-decoration: none; font-weight: bold; }
        .qa-link:hover { text-decoration: underline; }
        
        /* Renamed styling to apply to ALL inline download links */
        .download-inline-link {
            color: #D4AF37; /* Metallic Gold */
            font-weight: bold;
            text-decoration: underline;
            margin-left: 5px;
        }
        .download-inline-link:hover {
            color: #996515; /* Dark Gold on hover */
        }
    </style>
    """, unsafe_allow_html=True)

# 1. The PDF Downloader
@st.cache_data
def get_pdf_download_link(pdf_path, link_text):
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        return f'<a href="data:application/pdf;base64,{base64_pdf}" download="Bhavishya_Malika_QA_Book_Latest.pdf" class="download-inline-link">{link_text}</a>'
    return ""

# 2. The NEW CSV Downloader
@st.cache_data
def get_csv_download_link(csv_path, link_text):
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as f:
            base64_csv = base64.b64encode(f.read()).decode('utf-8')
        # Notice the data type changed to text/csv
        return f'<a href="data:text/csv;base64,{base64_csv}" download="Q_and_A_Output.csv" class="download-inline-link">{link_text}</a>'
    return ""

def render_headers():
    st.markdown('<h1 class="main-title">🕉️ Bhavishya Malika: Q&As</h1>', unsafe_allow_html=True)
    
    # Generate both links
    pdf_link_html = get_pdf_download_link("Bhavishya_Malika_QA_Book_Latest.pdf", "[All Q&A PDF]")
    csv_link_html = get_csv_download_link("Q_and_A_Output.csv", "[All Q&A CSV]")
    
    # Inject both links into the subtitle
    st.markdown(f'<div class="sub-title">Ask a question, and App will search Pandit Ji\'s live sessions to give you a summarized answer. {pdf_link_html} {csv_link_html}</div>', unsafe_allow_html=True)

def render_qa_card(row):
    q_text = str(row['Question']).replace('\n', '<br>')
    a_text = str(row['Answer']).replace('\n', '<br>')
    title_text = str(row['Title']).replace('\n', ' ')
    
    card_html = f"""
    <div class="qa-card">
        <div class="qa-question">Q: {q_text}</div>
        <div class="qa-answer"><strong>Answer:</strong> {a_text}</div>
        <div class="qa-meta">
            <strong>Date:</strong> {row['Date']} | <strong>Session:</strong> {title_text}<br><br>
            <a class="qa-link" href="{row['URL']}" target="_blank">▶ Watch Source Video [{row['Timestamp']}]</a>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
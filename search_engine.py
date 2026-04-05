import pandas as pd
import re
import streamlit as st
from rank_bm25 import BM25Okapi

# Stop words list isolated for cleaner code
STOP_WORDS = {"what", "are", "the", "of", "in", "to", "a", "is", "and", "for", "on", 
              "how", "why", "when", "where", "who", "will", "would", "can", "could", 
              "my", "i", "you", "your", "we", "our", "us", "it", "this", "that", 
              "with", "from", "by", "as", "at", "be", "do", "does", "did", "have", 
              "has", "had", "not", "but", "or", "if", "then", "about", "so", "much", 
              "many", "please", "tell", "me", "know", "want", "like", "just", "also", 
              "any", "some", "very", "should", "there", "their", "they"}

@st.cache_data
def load_data(filepath='Q_and_A_Output.csv'):
    df = pd.read_csv(filepath, header=None, 
                     names=['Date', 'Title', 'Timestamp', 'URL', 'Question', 'Answer'])
    return df.dropna(subset=['Question', 'Answer'])

@st.cache_resource
def build_search_index(dataframe):
    corpus = (dataframe['Question'] + " " + dataframe['Answer']).astype(str).tolist()
    tokenized_corpus = [re.findall(r'\b\w+\b', doc.lower()) for doc in corpus]
    return BM25Okapi(tokenized_corpus)

def perform_search(user_query, df, bm25_index):
    tokenized_query = re.findall(r'\b\w+\b', user_query.lower())
    meaningful_words = [word for word in tokenized_query if word not in STOP_WORDS]
    
    if not meaningful_words:
        return pd.DataFrame(), False # Returns empty dataframe and a 'False' valid_query flag
        
    doc_scores = bm25_index.get_scores(meaningful_words)
    df['score'] = doc_scores
    
    # 1. First, drop anything that scored a complete zero
    valid_matches = df[df['score'] > 0]
    
    if valid_matches.empty:
        return pd.DataFrame(), True
        
    # 2. DYNAMIC SCORING: The Magic Fix
    # Find the absolute best score for this specific search
    max_score = valid_matches['score'].max()
    
    # Only keep results that are at least 70% as good as the #1 best match
    # (This instantly cuts out the thousands of low-quality matches)
    strict_matches = valid_matches[valid_matches['score'] >= (max_score * 0.75)]
    
    # Sort them from best to worst
    results = strict_matches.sort_values(by='score', ascending=False)
    
    return results, True
import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from urllib.parse import urlparse
import random

# Set page config for a wider layout
st.set_page_config(layout="wide", page_title="SERP Similarity Tool")

# Custom CSS for a more professional look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background: #ffffff;
        padding: 3rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
    }
    .stTextInput>div>div>input {
        background-color: #f9f9f9;
    }
    h1 {
        color: #2c3e50;
    }
    h2 {
        color: #34495e;
    }
    .url-box {
        background-color: #f9f9f9;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }
    .similarity-score {
        font-size: 2rem;
        font-weight: bold;
        color: #2980b9;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Functions (keep your existing functions here)
def get_serp_comp(results):
    # ... (keep your existing function)

def compare_keywords(keyword1, keyword2, api_key):
    params = {
        "engine": "google",
        "q": keyword1,
        "gl": "in",
        "num": 20,
        "api_key": api_key
    }

    # ... (keep the rest of your existing function)

def main():
    st.title("🔍 SERP Similarity Tool")

    # Sidebar for API key input
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your SerpAPI Key:", type="password")

    # Main content
    col1, col2 = st.columns(2)
    with col1:
        keyword1 = st.text_input("Enter the first keyword:")
    with col2:
        keyword2 = st.text_input("Enter the second keyword:")

    if st.button("Compare Keywords"):
        if not api_key:
            st.error("Please enter your SerpAPI Key in the sidebar.")
        elif not keyword1 or not keyword2:
            st.warning("Please enter both keywords.")
        else:
            with st.spinner("Analyzing SERP similarity..."):
                urls1, urls2, exact_matches, domain_color_map, color_map, similarity = compare_keywords(keyword1, keyword2, api_key)

            st.markdown(f"<div class='similarity-score'>SERP Similarity: {similarity}%</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Results for '{keyword1}'")
                for url in urls1:
                    if url in exact_matches:
                        st.markdown(f'<div class="url-box" style="background-color: {color_map[url]};">{url}</div>', unsafe_allow_html=True)
                    elif url in domain_color_map:
                        st.markdown(f'<div class="url-box" style="background-color: {domain_color_map[url]}; border: 2px solid #e74c3c;">{url} 💀</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="url-box">{url}</div>', unsafe_allow_html=True)

            with col2:
                st.subheader(f"Results for '{keyword2}'")
                for url in urls2:
                    if url in exact_matches:
                        st.markdown(f'<div class="url-box" style="background-color: {color_map[url]};">{url}</div>', unsafe_allow_html=True)
                    elif url in domain_color_map:
                        st.markdown(f'<div class="url-box" style="background-color: {domain_color_map[url]}; border: 2px solid #e74c3c;">💀 {url}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="url-box">{url}</div>', unsafe_allow_html=True)

            st.info("💡 Exact matches are highlighted with the same color. URLs with a 💀 icon indicate common domains but different pages.")

    st.markdown("---")
    st.markdown("Created with ❤️ by [Your Name/Company]")

if __name__ == "__main__":
    main()

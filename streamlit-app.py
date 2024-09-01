import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from urllib.parse import urlparse
import random

# Set page config for a wider layout
st.set_page_config(layout="wide", page_title="SERP Similarity Tool")

# Custom CSS for a more professional look and improved mobile responsiveness
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        color: black !important;
    }
    .stTextInput>div>div>input {
        background-color: #f9f9f9;
        color: #000000;  /* Black text color */
        cursor: text;
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        transition: border-color 0.3s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50; /* Green border when focused */
    }
    .stSelectbox>div>div>select {
        background-color: #f9f9f9;
        color: #000000;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
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
    .serp-table {
        width: 100%;
        border-collapse: collapse;
        margin: auto;
    }
    .serp-table th, .serp-table td {
        border: 1px solid #ddd;
        padding: 8px;
        color: #000000;
        text-align: left;
    }
    .serp-table th {
        background-color: #383838;
        color: #ffffff;
        text-align: center;
    }
    .serp-similarity {
        font-weight: bold;
        font-size: 20px;
        margin: 20px 0;
        padding: 10px;
        background-color: #383838;
        color: #fff;
        text-align: center;
    }
    .serp-similarity span {
        color: #fff;
    }
    .exact-match {
        background-color: #FFAAAA;
        border: 2px solid #4EFF03;
        display: inline-block;
    }
    .matched-line {
        text-align: center;
        font-weight: bold;
    }
    .error {
        color: #ff0000;
        font-weight: bold;
    }
    .keyword-input {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .keyword-input > div {
        margin-bottom: 10px;
    }
    .check-button {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    .stats-box {
        background: linear-gradient(45deg, #3498db, #2ecc71);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stats-box h3 {
        margin-bottom: 15px;
        font-size: 24px;
    }
    .stats-item {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stats-item strong {
        font-size: 18px;
    }
    @media only screen and (max-width: 600px) {
        .main {
            padding: 1rem;
        }
        .stButton>button {
            width: 100%;
        }
        .serp-table th, .serp-table td {
            padding: 5px;
            font-size: 14px;
        }
        .serp-similarity {
            font-size: 16px;
            padding: 5px;
        }
        .stats-box {
            padding: 10px;
        }
        .stats-box h3 {
            font-size: 20px;
        }
        .stats-item strong {
            font-size: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Functions
def get_serp_comp(results):
    serp_comp = []
    if "organic_results" in results:
        num_results = min(len(results["organic_results"]), 10)
        for x in results["organic_results"][:num_results]:
            serp_comp.append(x["link"])
    return serp_comp

def compare_keywords(keyword1, keyword2, api_key, search_engine, language, device):
    params = {
        "engine": "google",
        "q": keyword1,
        "gl": search_engine.split('.')[-1],
        "hl": language,
        "num": 20,  # Request more results to ensure we get at least 10
        "api_key": api_key,
        "device": device.lower()
    }

    # Perform search for the first keyword
    search = GoogleSearch(params)
    results1 = search.get_dict()

    # Perform search for the second keyword
    params["q"] = keyword2
    search = GoogleSearch(params)
    results2 = search.get_dict()

    # Extract URLs from search results
    urls1 = get_serp_comp(results1)
    urls2 = get_serp_comp(results2)

    # Define color codes
    colors = ["#FFAAAA", "#AEBCFF", "#E2FFBD", "#F3C8FF", "#FFBD59", "#D9D9D9", "#FF904C", "#FF6D6D", "#68E9FF", "#4EFF03"]

    # Find common URLs and domains
    exact_matches = set(urls1) & set(urls2)
    common_domains = {}
    for url1 in urls1:
        domain1 = urlparse(url1).netloc
        for url2 in urls2:
            domain2 = urlparse(url2).netloc
            if domain1 == domain2 and url1 != url2:
                if domain1 not in common_domains:
                    common_domains[domain1] = set()
                common_domains[domain1].add(url1)
                common_domains[domain1].add(url2)

    # Assign colors to exact matches and common domains
    color_map = {}
    domain_color_map = {}
    for url in exact_matches:
        color = colors.pop(0) if colors else f'#{random.randint(0, 0xFFFFFF):06x}'
        color_map[url] = color

    for domain in common_domains:
        color = colors.pop(0) if colors else f'#{random.randint(0, 0xFFFFFF):06x}'
        for url in common_domains[domain]:
            domain_color_map[url] = color

    # Highlight URLs
    highlighted_urls1 = []
    highlighted_urls2 = []
    for url1 in urls1:
        if url1 in exact_matches:
            highlighted_urls1.append(f'<span style="background-color: {color_map[url1]}; color: black;">{url1}</span>')
        elif url1 in domain_color_map:
            highlighted_urls1.append(f'<span style="background-color: {domain_color_map[url1]}; border: 2px solid darkred; color: black;">{url1} 💀</span>')
        else:
            highlighted_urls1.append(url1)

    for url2 in urls2:
        if url2 in exact_matches:
            highlighted_urls2.append(f'<span style="background-color: {color_map[url2]}; color: black;">{url2}</span>')
        elif url2 in domain_color_map:
            highlighted_urls2.append(f'<span style="background-color: {domain_color_map[url2]}; border: 2px solid darkred; color: black;">{url2} 💀</span>')
        else:
            highlighted_urls2.append(url2)

    # Calculate similarity percentage
    similarity = round(100 * len(exact_matches) / max(len(urls1), len(urls2)), 2)

    # Return the results
    return highlighted_urls1, highlighted_urls2, similarity

# Header
st.title("SERP Similarity Checker")

# Inputs for keyword 1 and keyword 2
col1, col2 = st.columns(2)

with col1:
    keyword1 = st.text_input("Enter first keyword")
with col2:
    keyword2 = st.text_input("Enter second keyword")

api_key = st.text_input("Enter your SerpAPI key", type="password")
search_engine = st.selectbox("Select the Google search engine", options=["google.com", "google.co.uk", "google.ca", "google.com.au", "google.in"])
language = st.selectbox("Select the search language", options=["en", "fr", "es", "de", "it", "pt", "ru", "zh"])
device = st.selectbox("Select the device type", options=["Desktop", "Mobile"])

# Button to start comparison
if st.button("Check Similarity"):
    if keyword1 and keyword2 and api_key:
        urls1, urls2, similarity = compare_keywords(keyword1, keyword2, api_key, search_engine, language, device)

        # Display similarity score
        st.markdown(f"<div class='serp-similarity'>SERP Similarity: <span>{similarity}%</span></div>", unsafe_allow_html=True)

        # Display URLs for keyword 1
        st.markdown("<h2>Top SERP for First Keyword</h2>", unsafe_allow_html=True)
        for url in urls1:
            st.markdown(f'<div class="url-box">{url}</div>', unsafe_allow_html=True)

        # Display URLs for keyword 2
        st.markdown("<h2>Top SERP for Second Keyword</h2>", unsafe_allow_html=True)
        for url in urls2:
            st.markdown(f'<div class="url-box">{url}</div>', unsafe_allow_html=True)
    else:
        st.error("Please enter both keywords and your SerpAPI key!")

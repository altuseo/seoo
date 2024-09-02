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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .reportview-container {
        background: #ffffff;
    }
    .main {
        background: #ffffff;
        padding: 2rem;
        margin: auto;
        border-radius: 10px;
        max-width: 1200px;
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
        color: #000000;
        cursor: text;
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        transition: border-color 0.2s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
    }
    .stSelectbox>div>div>select {
        background-color: #f9f9f9;
        color: #000000;
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
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
        overflow-x: auto;
        display: block;
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
        text-align: center;
    }
    .keyword-input {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-bottom: 1rem;
    }
    .keyword-input > div {
        width: 100%;
        max-width: 500px;
        margin: 10px 0;
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
        width: 100%;
        max-width: 600px;
        margin: auto;
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
        .keyword-input {
            flex-direction: column;
            align-items: center;
        }
        .keyword-input > div {
            width: 100%;
            margin: 5px 0;
        }
        .stats-box {
            width: 100%;
            padding: 10px;
        }
        .serp-table {
            overflow-x: auto;
            display: block;
            width: 100%;
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
    similarity = round(100 * len(exact_matches) / len(urls1), 2) if urls1 else 0

    # Create a table to display URLs with enhanced UI
    table = f'''
    <div class="serp-similarity">SERP Similarity: <span>{similarity}%</span></div>
    <div class="stats-box">
        <h3>SERP Comparison Statistics</h3>
        <div class="stats-item">
            <strong>Exact Common URLs:</strong> {len(exact_matches)}
        </div>
        <div class="stats-item">
            <strong>Same Website, Different Pages:</strong> {sum(len(urls) for urls in common_domains.values()) // 2}
        </div>
    </div>
    <table class="serp-table">
        <tr><th>{keyword1}</th><th>{keyword2}</th></tr>
    '''
    for url1, url2 in zip(highlighted_urls1, highlighted_urls2):
        table += f'<tr><td>{url1}</td><td>{url2}</td></tr>'
        if url1 in exact_matches and url2 in exact_matches:
            table += f'<tr><td colspan="2" style="text-align:center;"><span style="color:{color_map[url1]};">&#x2194; Matched URL</span></td></tr>'
    table += '</table>'

    return similarity, table

def main():
    st.title("🔍 SERP Similarity Tool")

    # Configuration section on the main page
    st.header("Configuration")
    api_key = st.text_input("Enter your SerpAPI Key:", type="password", help="Your SerpAPI key for fetching search results.")
    
    # Search engine selection
    search_engines = {
        "Google (United States)": "google.com",
        "Google (India)": "google.co.in",
        "Google (United Kingdom)": "google.co.uk",
        "Google (Canada)": "google.ca",
        "Google (Australia)": "google.com.au",
        "Google (Germany)": "google.de",
        "Google (France)": "google.fr",
        "Google (Japan)": "google.co.jp",
        "Google (Brazil)": "google.com.br",
        "Google (Italy)": "google.it",
        # Add more search engines as needed
    }
    search_engine = st.selectbox(
        "Select Search Engine",
        options=list(search_engines.keys()),
        format_func=lambda x: x
    )
    
    language = st.selectbox("Select Language", options=[
        "en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar", "ru"
    ], index=0)
    device = st.selectbox("Select Device", options=["Desktop", "Mobile", "Tablet"], index=0)

    # Keyword input
    st.subheader("Enter Keywords")
    col1, col2 = st.columns(2)
    with col1:
        keyword1 = st.text_input("Enter first keyword", key="keyword1")
    with col2:
        keyword2 = st.text_input("Enter second keyword", key="keyword2")

    # Check SERP Similarity button
    st.subheader("Check SERP Similarity")
    if st.button("Check SERP Similarity", key="check_similarity"):
        if not keyword1 or not keyword2:
            st.markdown('<p class="error">Please enter both keywords.</p>', unsafe_allow_html=True)
        else:
            # Run SERP comparison
            similarity, table = compare_keywords(keyword1, keyword2, api_key, search_engines[search_engine], language, device)
            st.markdown(table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

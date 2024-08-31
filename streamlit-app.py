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
            highlighted_urls2.append(f'<span style="background-color: {domain_color_map[url2]}; border: 2px solid darkred; color: black;">💀 {url2}</span>')
        else:
            highlighted_urls2.append(url2)

    # Calculate similarity percentage
    similarity = round(100 * len(exact_matches) / len(urls1), 2) if urls1 else 0

    # Create a table to display URLs with enhanced UI
    table = f'''
    <style>
        .serp-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .serp-table th, .serp-table td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        .serp-table th {{
            background-color: #383838;
            text-align: center;
        }}
        .serp-similarity {{
            font-weight: bold;
            font-size: 20px;
            margin: 20px 0;
            padding: 10px;
            background-color: #383838;
            color: #fff;
            text-align: center;
        }}
        .serp-similarity span {{
            color: #fff;
        }}
        .exact-match {{
            background-color: #FFAAAA;
            border: 2px solid #4EFF03;
            display: inline-block;
        }}
        .matched-line {{
            text-align: center;
            font-weight: bold;
        }}
    </style>
    <div class="serp-similarity">SERP Similarity: <span>{similarity}%</span></div>
    <table class="serp-table">
        <tr><th>{keyword1}</th><th>{keyword2}</th></tr>
    '''
    for url1, url2 in zip(highlighted_urls1, highlighted_urls2):
        table += f'<tr><td>{url1}</td><td>{url2}</td></tr>'
        if url1 in exact_matches and url2 in exact_matches:
            table += f'<tr><td colspan="2" style="text-align:center;"><span style="color:{color_map[url1]};">&#x2194; Matched URL</span></td></tr>'
    table += '</table>'

    return HTML(table)

# Get keywords from the user
keyword1 = input("Enter the first keyword: ")
keyword2 = input("Enter the second keyword: ")

# Call the compare_keywords function
url_table = compare_keywords(keyword1, keyword2)

# Display the table
display(url_table)

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

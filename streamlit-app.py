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
    serp_comp = []
    if "organic_results" in results:
        num_results = min(len(results["organic_results"]), 10)
        for x in results["organic_results"][:num_results]:
            serp_comp.append(x["link"]) 
    return serp_comp

def compare_keywords(keyword1, keyword2, api_key):
    params = {
        "engine": "google",
        "q": keyword1,
        "gl": "in",
        "num": 20,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results1 = search.get_dict()

    params["q"] = keyword2
    search = GoogleSearch(params)
    results2 = search.get_dict()

    urls1 = get_serp_comp(results1)
    urls2 = get_serp_comp(results2)

    colors = ["#FFAAAA", "#AEBCFF", "#E2FFBD", "#F3C8FF", "#FFBD59", "#D9D9D9", "#FF904C", "#FF6D6D", "#68E9FF", "#4EFF03"]

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

    color_map = {}
    domain_color_map = {}
    for url in exact_matches:
        color = colors.pop(0) if colors else f'#{random.randint(0, 0xFFFFFF):06x}'
        color_map[url] = color

    for domain in common_domains:
        color = colors.pop(0) if colors else f'#{random.randint(0, 0xFFFFFF):06x}'
        for url in common_domains[domain]:
            domain_color_map[url] = color

    similarity = round(100 * len(exact_matches) / len(urls1), 2) if urls1 else 0

    return urls1, urls2, exact_matches, domain_color_map, color_map, similarity

def main():
    st.title("🔍 SERP Similarity Tool")

    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter your SerpAPI Key:", type="password")

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
    st.markdown("Created with ❤️ by Altamash Mapari | Sr. SEO Analyst @ Botpresso")

if __name__ == "__main__":
    main()

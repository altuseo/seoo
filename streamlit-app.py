import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from urllib.parse import urlparse
import random

# Set page config for a wider layout
st.set_page_config(layout="wide", page_title="SERP Similarity Tool")

# Custom CSS for a more professional look and usability enhancements
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
        padding: 1rem;
        margin: auto;
        border-radius: 10px;
        max-width: 1200px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow-y: auto; /* Enables vertical scroll for the whole page */
        max-height: 90vh; /* Sets maximum height to 90% of viewport */
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px;
        margin: 5px 0;  /* Reduced margin for less gap */
        border-radius: 5px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #45a049;
        color: white !important;
    }

    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #f9f9f9;
        color: #000000;  /* Ensuring black text */
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin: 0;
        transition: all 0.2s ease-in-out;
    }

    .stTextInput>div>div>label, .stSelectbox>div>div>label {
        color: #000000;  /* Ensuring black text for labels */
        margin-bottom: 0.3rem; /* Reduced margin for compactness */
        display: block;
    }

    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); /* Added glow effect for focus */
    }

    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        text-align: center;
        margin: 0.3rem 0;  /* Reduced margin for headings */
    }

    .subheader {
        color: #000000;  /* Ensuring black text for headers */
        text-align: center;
        font-size: 1.25rem;
        margin: 0.3rem 0;
    }

    .url-box {
        background-color: #f9f9f9;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }

    .similarity-score {
        font-size: 1.5rem; /* Adjusted font size for better layout */
        font-weight: bold;
        color: #2980b9;
        text-align: center;
        margin: 0.5rem 0;
    }

    .serp-table-container {
        width: 100%;
        display: flex;
        justify-content: space-between; /* Spread columns across container */
        margin-bottom: 1rem;
        padding: 1rem;  /* Added padding for better spacing */
        position: relative; /* Position relative for line drawing */
    }

    .serp-column {
        width: 45%;
    }

    .serp-column-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #333;
    }

    .serp-row {
        display: flex;
        align-items: center;
        padding: 0.5rem;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        position: relative;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .serp-row:hover {
        background-color: #e0e0e0;
    }

    .serp-icon {
        width: 24px;
        height: 24px;
        margin-right: 10px;
    }

    .serp-number {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background-color: #ddd;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-weight: bold;
        color: #333;
    }

    .line {
        position: absolute;
        width: 1px;
        background-color: #4CAF50;
        z-index: 1;
    }

    .info-section {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        line-height: 1.6;
    }

    .info-section h2 {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .info-section p, .info-section ul {
        color: #333;
        font-size: 1rem;
    }

    @media only screen and (max-width: 600px) {
        .main {
            padding: 1rem;
            max-height: 80vh; /* Adjusted for smaller screens */
        }

        .keyword-input {
            flex-direction: column;
            align-items: center;
        }

        .keyword-input > div {
            width: 100%;
            margin: 5px 0;
        }

        .serp-table-container {
            flex-direction: column;
        }

        .serp-column {
            width: 100%;
            margin-bottom: 1rem;
        }

        .stats-box {
            width: 100%;
            padding: 10px;
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

    # Generate HTML for both columns
    column1_html = '<div class="serp-column"><div class="serp-column-header">' + keyword1 + '</div>'
    column2_html = '<div class="serp-column"><div class="serp-column-header">' + keyword2 + '</div>'
    lines_html = ""

    for index, (url1, url2) in enumerate(zip(urls1, urls2), start=1):
        icon1 = f'<div class="serp-icon">&#x1F517;</div>'
        icon2 = f'<div class="serp-icon">&#x1F517;</div>'
        number_html = f'<div class="serp-number">{index}</div>'

        if url1 in exact_matches:
            column1_html += f'<div class="serp-row">{number_html}{icon1}<span style="background-color: {color_map[url1]}; color: black;">{url1}</span></div>'
        else:
            column1_html += f'<div class="serp-row">{number_html}{icon1}{url1}</div>'

        if url2 in exact_matches:
            column2_html += f'<div class="serp-row">{number_html}{icon2}<span style="background-color: {color_map[url2]}; color: black;">{url2}</span></div>'
        else:
            column2_html += f'<div class="serp-row">{number_html}{icon2}{url2}</div>'

        # Draw connecting lines for exact matches
        if url1 in exact_matches and url2 in exact_matches:
            lines_html += f'<div class="line" style="top: {index * 50}px; left: 50%; height: 1px;"></div>'

    column1_html += '</div>'
    column2_html += '</div>'

    # Final HTML output combining both columns and lines
    table_html = f'''
    <div class="serp-table-container">
        {column1_html}
        {column2_html}
        {lines_html}
    </div>
    '''

    # Additional content section
    additional_content = """
    <div class="info-section">
        <h2>About the SERP Similarity Tool</h2>
        <p>Altamash Mapari built this tool for SEOs so that everyone can enjoy and easily check the SERP Similarity in one click. The <strong>SERP Similarity Tool</strong> is a powerful, free SERP analysis tool designed to help you compare keyword SERP results and optimize your content strategy. This free SERP tool allows you to analyze live SERP data, understand keyword SERP overlap, and gain valuable insights into your SEO performance.</p>
        
        <h2>What is SERP Similarity?</h2>
        <p><strong>SERP Similarity</strong> refers to the comparison of search engine results pages (SERPs) for different keywords to identify commonalities and differences. By using this tool, you can analyze how similar or different the SERPs are for two keywords, helping you understand your competition and optimize your SEO strategies.</p>
        
        <h2>How to Use the SERP Similarity Tool</h2>
        <ul>
            <li><strong>Get Your SerpAPI Key</strong>: To use this free SERP check tool, you'll need a SerpAPI key. Sign up for a free account on <a href="https://serpapi.com/">SerpAPI</a>. After registering, you can find your API key in the dashboard.</li>
            <li><strong>Enter Your API Key</strong>: Copy your SerpAPI key and paste it into the "Enter your SerpAPI Key" field in the tool.</li>
            <li><strong>Select Search Engine, Language, and Device</strong>: Choose your preferred search engine (e.g., Google), language, and device (Desktop, Mobile, or Tablet).</li>
            <li><strong>Enter Keywords</strong>: Input the two keywords you want to compare in the "Enter first keyword" and "Enter second keyword" fields. This keyword SERP tool will fetch the results for both keywords.</li>
            <li><strong>Check SERP Similarity</strong>: Click on the "Check SERP Similarity" button to run a live SERP analysis. The tool will display a table showing the URLs ranking for both keywords, along with any exact matches.</li>
        </ul>
        
        <h2>Understanding the Results</h2>
        <ul>
            <li><strong>Color Codes</strong>:
                <ul>
                    <li><strong>Red (#FFAAAA)</strong>: Indicates exact match URLs between both keyword SERPs.</li>
                    <li><strong>Blue (#AEBCFF)</strong>, <strong>Green (#E2FFBD)</strong>, <strong>Purple (#F3C8FF)</strong>, etc.: Different colors highlight different levels of similarity or overlap.</li>
                </ul>
            </li>
            <li><strong>Emoji 💀</strong>: The skull emoji indicates URLs that are from the same domain but different pages, providing insights into how competitors dominate the SERP with multiple URLs.</li>
        </ul>
        
        <p>This free SERP analysis tool is perfect for SEOs looking to gain quick insights into keyword competition and overlap. Start using this best free SERP tool today and gain valuable insights into your SEO strategy!</p>
    </div>
    """

    return similarity, table_html + additional_content

def main():
    st.title("🔍 SERP Similarity Tool")

    # Row 1: SERP API Key and Search Engine
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="subheader">Enter your SerpAPI Key</div>', unsafe_allow_html=True)
        api_key = st.text_input("", type="password", help="Your SerpAPI key for fetching search results.", key="api_key_input")
    with col2:
        st.markdown('<div class="subheader">Select Search Engine</div>', unsafe_allow_html=True)
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
        }
        search_engine = st.selectbox(
            "", options=list(search_engines.keys()), format_func=lambda x: x
        )

    # Row 2: Language and Device
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="subheader">Select Language</div>', unsafe_allow_html=True)
        language = st.selectbox("", options=["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar", "ru"], index=0)
    with col2:
        st.markdown('<div class="subheader">Select Device</div>', unsafe_allow_html=True)
        device = st.selectbox("", options=["Desktop", "Mobile", "Tablet"], index=0)

    # Row 3: Keywords
    st.markdown('<div class="subheader">Enter Keywords</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        keyword1 = st.text_input("Enter first keyword", key="keyword1")
    with col2:
        keyword2 = st.text_input("Enter second keyword", key="keyword2")

    # Check SERP Similarity button
    st.markdown('<div class="check-button"></div>', unsafe_allow_html=True)
    if st.button("Check SERP Similarity", key="check_similarity"):
        if not keyword1 or not keyword2:
            st.markdown('<p class="error">Please enter both keywords.</p>', unsafe_allow_html=True)
        else:
            # Run SERP comparison
            similarity, table = compare_keywords(keyword1, keyword2, api_key, search_engines[search_engine], language, device)
            st.markdown(table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

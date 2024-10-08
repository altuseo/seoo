import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from urllib.parse import urlparse
from collections import Counter
import itertools
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
        background-color: #4CAF50 !important; /* Keep button green */
        color: white !important; /* Keep text color white */
        font-weight: bold;
        padding: 10px;
        margin: 5px 0;  /* Reduced margin for less gap */
        border-radius: 5px;
        border: none;
        width: 100%;
        transition: none; /* Remove transition effects */
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
        justify-content: center;
        margin-bottom: 1rem;
        padding: 1rem;  /* Added padding for better spacing */
        overflow-x: auto; /* Enables horizontal scroll for smaller screens */
    }

    .serp-table {
        width: 100%; /* Fixed width to fill container */
        border-collapse: collapse;
        margin: auto;
        border: 2px solid #ddd; /* Improved border visibility */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Added subtle shadow for attractiveness */
        position: relative;
    }

    .serp-table th, .serp-table td {
       border: 1px solid #ddd;
       padding: 8px; /* Consistent padding for better spacing */
       color: #000000;
       text-align: left;
       font-size: 12px; /* Decrease font size to fit longer URLs */
       overflow-wrap: break-word; /* Ensures long words (like URLs) wrap within the cell */
       max-width: 200px; /* Optional: Set a maximum width for each cell to limit the length */
       white-space: normal; /* Ensures text wraps normally */
       transition: background-color 0.3s ease; /* Transition for hover effect */
    }

    .serp-table th {
        background-color: #383838; /* Match SERP similarity table heading color */
        color: #ffffff;
        text-align: center;
        font-weight: bold;
    }

    .serp-similarity {
        font-weight: bold;
        font-size: 18px; /* Adjusted font size */
        margin: 10px 0; /* Reduced margin for less gap */
        padding: 10px;
        background-color: #383838;
        color: #fff;
        text-align: center;
    }

    .serp-similarity span {
        color: #fff;
    }

    .ngram-table-container {
        width: 100%;
        margin-top: 20px;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }

    .ngram-table {
        width: 100%;
    table-layout: fixed; /* Ensures consistent column width */
    border-collapse: collapse;
    margin: auto;
    border: 2px solid #ddd; /* Match table border to SERP similarity table */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

    .ngram-table th, .ngram-table td {
   border: 1px solid #ddd;
   padding: 8px;
   text-align: left;
   font-size: 12px; /* Uniform font size */
   color: #000000;
}

   .ngram-table th {
    background-color: #383838; /* Match SERP similarity table heading color */
    color: #ffffff;
    text-align: center;
    font-weight: bold;
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

    body {
        -webkit-tap-highlight-color: transparent; /* Remove highlight color on tap (for mobile devices) */
    }

    .stats-box {
        background: linear-gradient(45deg, #3498db, #2ecc71);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        margin-bottom: 20px; /* Added margin for spacing below stats box */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 600px;
        margin: auto;
    }

    .stats-box h3 {
        margin-bottom: 10px; /* Reduced margin */
        font-size: 20px; /* Adjusted font size */
        font-weight: bold;
        color: #ffffff; /* White color for better contrast */
    }

    .stats-item {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 5px; /* Reduced margin */
    }

    .stats-item strong {
        font-size: 16px; /* Adjusted font size */
    }

    .numbering {
        text-align: center;
        font-weight: bold;
        background-color: #f0f0f0;
        padding: 10px;
        border-right: 1px solid #ddd;
        width: 40px; /* Set a smaller width for the numbering column */
        max-width: 40px; /* Ensure the width does not exceed this value */
    }

    /* Hover effect for highlighting matching URLs */
    .highlighted:hover {
        background-color: #d1ecf1;
        cursor: pointer;
    }

    /* Line between matching URLs */
    .line {
        position: absolute;
        width: 40%;
        height: 2px;
        background-color: #4CAF50;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: none;
    }

    /* Show line on hover */
    .highlighted:hover + .line {
        display: block;
    }

    /* Matched URL Highlight */
    .matched-highlight {
        background-color: #d1ecf1;
        font-weight: bold;
        text-align: center;
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
            overflow-x: auto;
            width: 100%;
        }

        .stats-box {
            width: 100%;
            padding: 10px;
        }

        .serp-table {
            width: 100%; /* Ensuring the table stays within viewport */
            table-layout: fixed; /* Ensures columns are sized based on available space */
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

def extract_titles(results):
    titles = []
    if "organic_results" in results:
        for x in results["organic_results"]:
            titles.append(x.get("title", ""))
    return titles

def ngram_analysis(titles):
    unigrams = Counter(itertools.chain.from_iterable(title.lower().split() for title in titles))
    bigrams = Counter(itertools.chain.from_iterable(zip(title.lower().split(), title.lower().split()[1:]) for title in titles))
    trigrams = Counter(itertools.chain.from_iterable(zip(title.lower().split(), title.lower().split()[1:], title.lower().split()[2:]) for title in titles))
    
    return unigrams, bigrams, trigrams

def generate_ngram_table(unigrams, bigrams, trigrams):
    table = f"""
    <div class="ngram-table-container">
        <h2 style="text-align: center;">N-gram Analysis Based on Top 10 Titles</h2>
        <table class="ngram-table">
            <tr><th>Unigram</th><th>Frequency</th></tr>
    """
    for ngram, freq in unigrams.most_common(10):
        table += f"<tr><td>{ngram}</td><td>{freq}</td></tr>"
    
    # Remove any unnecessary line breaks or styles
    table += """
        </table>
        <table class="ngram-table">
            <tr><th>Bi-gram</th><th>Frequency</th></tr>
    """
    for ngram, freq in bigrams.most_common(10):
        table += f"<tr><td>{' '.join(ngram)}</td><td>{freq}</td></tr>"
    
    # Again, keep the structure consistent
    table += """
        </table>
        <table class="ngram-table">
            <tr><th>Tri-gram</th><th>Frequency</th></tr>
    """
    for ngram, freq in trigrams.most_common(10):
        table += f"<tr><td>{' '.join(ngram)}</td><td>{freq}</td></tr>"
    table += "</table></div>"
    return table

def compare_keywords(keyword1, keyword2, api_key, search_engine, language, device):
    params = {
        "engine": "google",
        "q": keyword1,
        "gl": "us" if search_engine == "google.com" else search_engine.split('.')[-1],
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

    # Extract URLs and titles from search results
    urls1 = get_serp_comp(results1)
    urls2 = get_serp_comp(results2)
    titles1 = extract_titles(results1)
    titles2 = extract_titles(results2)

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
    lines_html = ""  # To store lines for matching URLs
    for url1 in urls1:
        if url1 in exact_matches:
            highlighted_urls1.append(f'<span class="highlighted matched-highlight" style="background-color: {color_map[url1]}; color: black;" data-url="{url1}">{url1}</span>')
        elif url1 in domain_color_map:
            highlighted_urls1.append(f'<span style="background-color: {domain_color_map[url1]}; border: 2px solid darkred; color: black;" class="highlighted">{url1} 💀</span>')
        else:
            highlighted_urls1.append(f'<span class="highlighted">{url1}</span>')

    for url2 in urls2:
        if url2 in exact_matches:
            highlighted_urls2.append(f'<span class="highlighted matched-highlight" style="background-color: {color_map[url2]}; color: black;" data-url="{url2}">{url2}</span>')
        elif url2 in domain_color_map:
            highlighted_urls2.append(f'<span style="background-color: {domain_color_map[url2]}; border: 2px solid darkred; color: black;" class="highlighted">{url2} 💀</span>')
        else:
            highlighted_urls2.append(f'<span class="highlighted">{url2}</span>')

    # Create hover effect lines
    for i, url in enumerate(exact_matches):
        lines_html += f'<div class="line" style="top: {i*40 + 40}px;"></div>'

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
    <div class="serp-table-container">
        <table class="serp-table">
            <tr><th class="numbering">#</th><th>{keyword1}</th><th>{keyword2}</th></tr>
    '''
    for index, (url1, url2) in enumerate(zip(highlighted_urls1, highlighted_urls2), start=1):
        table += f'<tr><td class="numbering">{index}</td><td>{url1}</td><td>{url2}</td></tr>'
        if url1 in exact_matches and url2 in exact_matches:
            table += f'<tr><td colspan="3" class="matched-line" style="background-color: {color_map[url1]};">&#x2194; Match the following lines</td></tr>'
    table += f'</table>{lines_html}</div>'

    # Perform N-gram analysis
    all_titles = titles1 + titles2
    unigrams, bigrams, trigrams = ngram_analysis(all_titles)
    ngram_table = generate_ngram_table(unigrams, bigrams, trigrams)

    # Additional content section
    additional_content = """
    <div class="info-section">
        <h2>About the SERP Similarity Tool</h2>
        <p><a href="https://www.linkedin.com/in/altamash-mapari-44502a1a2/">Altamash Mapari</a> built this tool with the help of ChatGPT & Claude for SEOs so that everyone can enjoy and easily check the SERP Similarity in one click. This free SERP tool allows you to analyze live SERP data, understand keyword SERP overlap, and gain valuable insights into your SEO performance.</p>
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
   <p>Made with ❤️</p>
    </div>
    """

    return similarity, table + ngram_table + additional_content

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

import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

# Function to extract SERP URLs
def extract_serp_urls(keyword, api_key, search_engine, language, device):
    url = f"https://api.example.com/serp?apikey={api_key}&q={keyword}&google_domain={search_engine}&hl={language}&device={device}"
    response = requests.get(url)
    data = response.json()

    urls = []
    for result in data.get('organic_results', []):
        urls.append(result['link'])

    return urls

# Function to calculate similarity between two keyword SERPs
def calculate_similarity(urls1, urls2):
    # Calculate similarity score
    matches = 0
    for url in urls1:
        if url in urls2:
            matches += 1
    similarity = (matches / max(len(urls1), len(urls2))) * 100
    return round(similarity, 2)

# Function to compare two keywords and return the similarity and a comparison table
def compare_keywords(keyword1, keyword2, api_key, search_engine, language, device):
    urls1 = extract_serp_urls(keyword1, api_key, search_engine, language, device)
    urls2 = extract_serp_urls(keyword2, api_key, search_engine, language, device)

    similarity = calculate_similarity(urls1, urls2)

    # Create a DataFrame for better visualization
    data = {
        f"{keyword1} URLs": urls1,
        f"{keyword2} URLs": urls2 + [''] * (len(urls1) - len(urls2)) if len(urls1) > len(urls2) else urls2,
    }
    df = pd.DataFrame(data)

    # Convert DataFrame to HTML table
    table_html = df.to_html(index=False)

    return similarity, table_html

# Main Streamlit app
def main():
    st.title("Keyword SERP Similarity Checker")
    st.markdown("<style>h1{color: #FF6347;}</style>", unsafe_allow_html=True)

    st.markdown("""
        <style>
            body {
                font-family: 'Poppins', sans-serif;
            }
            .css-18e3th9 {
                padding-top: 0rem;
            }
            .stButton>button {
                background-color: #FF6347;
                color: white;
            }
            .stButton>button:hover {
                color: black;
            }
            .stTextInput>div>input {
                font-family: 'Poppins', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

    api_key = st.sidebar.text_input("Enter your API Key", type="password")
    search_engine = st.sidebar.selectbox("Select Search Engine", 
        options=["Google (google.com)", "Angola (google.co.ao)", "Argentina (google.com.ar)", "Australia (google.com.au)", 
                 "Brazil (google.com.br)", "Canada (google.ca)", "China (google.cn)", "France (google.fr)", "Germany (google.de)", 
                 "India (google.co.in)", "Italy (google.it)", "Japan (google.co.jp)", "Mexico (google.com.mx)", "Russia (google.ru)", 
                 "United Kingdom (google.co.uk)", "United States (google.com)"])
    language = st.sidebar.selectbox("Select Language", options=["en", "es", "fr", "de", "it", "pt", "nl", "ja", "zh", "ar", "ru"])
    device = st.sidebar.selectbox("Select Device", options=["desktop", "mobile", "tablet"])

    # Input fields for keywords
    keyword1 = st.text_input("Enter first keyword:")
    keyword2 = st.text_input("Enter second keyword:")

    if st.button("Compare SERP"):
        if api_key and keyword1 and keyword2:
            similarity, table = compare_keywords(keyword1, keyword2, api_key, search_engine.split(" ")[-1], language, device)
            st.markdown(f"### SERP Similarity: {similarity}%")
            st.markdown(table, unsafe_allow_html=True)
        else:
            st.error("Please provide the API key and both keywords to compare.")

if __name__ == "__main__":
    main()

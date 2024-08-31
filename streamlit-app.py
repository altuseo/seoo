import streamlit as st

# Use Poppins font style
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
        }
        .header {
            text-align: center;
            margin-bottom: -30px;  /* Adjust to remove extra space */
        }
        .similarity {
            text-align: center;
            font-size: 24px;
        }
        .urls {
            text-align: left;
        }
        .error {
            color: red;
            font-size: 14px;
        }
        .stButton button {
            color: black;  /* Button hover text color set to black */
        }
    </style>
""", unsafe_allow_html=True)

def compare_keywords(keyword1, keyword2, api_key, country, language, device):
    # Simulated comparison logic for demonstration
    similarity = 75  # Placeholder similarity percentage
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5",
        "https://example.com/page6",
        "https://example.com/page7",
        "https://example.com/page8",
        "https://example.com/page9",
        "https://example.com/page10"
    ]
    
    table = f"""
        <div class="similarity">
            <p>SERP Similarity: {similarity}%</p>
        </div>
        <div class="urls">
            <ul>
                {"".join([f"<li>{url}</li>" for url in urls])}
            </ul>
        </div>
    """
    
    return similarity, table

def main():
    st.markdown('<h1 class="header">🔍 SERP Similarity Tool</h1>', unsafe_allow_html=True)

    api_key = st.sidebar.text_input("API Key", type="password")
    
    # Custom dropdown for selecting search engine
    search_engines = {
        "google.ad": "Andorra",
        "google.ae": "United Arab Emirates",
        "google.al": "Albania",
        "google.am": "Armenia",
        "google.as": "American Samoa",
        "google.at": "Austria",
        "google.az": "Azerbaijan",
        "google.ba": "Bosnia and Herzegovina",
        "google.be": "Belgium",
        "google.bf": "Burkina Faso",
        "google.bg": "Bulgaria",
        "google.bi": "Burundi",
        "google.bj": "Benin",
        "google.bs": "Bahamas",
        "google.bt": "Bhutan",
        "google.by": "Belarus",
        "google.ca": "Canada",
        "google.cd": "Democratic Republic of the Congo",
        "google.cf": "Central African Republic",
        "google.cg": "Republic of the Congo",
        "google.ch": "Switzerland",
        "google.ci": "Ivory Coast",
        "google.cl": "Chile",
        "google.cm": "Cameroon",
        "google.co.ao": "Angola",
        "google.co.bw": "Botswana",
        "google.co.ck": "Cook Islands",
        "google.co.cr": "Costa Rica",
        "google.co.id": "Indonesia",
        "google.co.il": "Israel",
        "google.co.in": "India",
        "google.co.jp": "Japan",
        "google.co.ke": "Kenya",
        "google.co.kr": "South Korea",
        "google.co.ls": "Lesotho",
        "google.co.ma": "Morocco",
        "google.co.mz": "Mozambique",
        "google.co.nz": "New Zealand",
        "google.co.th": "Thailand",
        "google.co.tz": "Tanzania",
        "google.co.ug": "Uganda",
        "google.co.uk": "United Kingdom",
        "google.co.uz": "Uzbekistan",
        "google.co.ve": "Venezuela",
        "google.co.vi": "United States Virgin Islands",
        "google.co.za": "South Africa",
        "google.co.zm": "Zambia",
        "google.co.zw": "Zimbabwe",
        "google.com": "United States",
        # Add all other search engines as needed...
    }

    search_engine_choices = [f"{name} ({code})" for code, name in search_engines.items()]
    search_engine_selected = st.sidebar.selectbox("Select Search Engine", search_engine_choices, index=search_engine_choices.index("India (google.co.in)"))

    language = st.sidebar.selectbox("Select Language", options=["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko", "ar", "ru"], index=0)
    device = st.sidebar.selectbox("Select Device", options=["Desktop", "Mobile", "Tablet"], index=0)

    keyword1 = st.text_input("Enter first keyword")
    keyword2 = st.text_input("Enter second keyword")

    if st.button("Check SERP Similarity"):
        if not keyword1 or not keyword2:
            st.markdown('<p class="error">Please enter both keywords.</p>', unsafe_allow_html=True)
        else:
            similarity, table = compare_keywords(keyword1, keyword2, api_key, search_engine_selected, language, device)
            st.markdown(table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

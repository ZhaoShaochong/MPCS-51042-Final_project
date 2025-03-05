import requests
import nltk
import streamlit as st
import json
import os
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import urllib.parse  # Used for encoding keywords

# Download NLTK stopwords (this is needed for the first run)
nltk.download('punkt')
nltk.download('stopwords')

CONFIG_FILE = "config.json"

# Default API keys
DEFAULT_API_KEYS = {
    "NewsAPI": "e5ca71dadf6a4916a2e7b898ab1803a8",
    "GNews": "8877903057fde1fcaced3baaaf06c44b"
}

# Language names to language code mapping
LANGUAGES = {
    "English": "en",
    "中文": "zh",
    "Français": "fr",
    "Deutsch": "de",
    "Español": "es",
    "Italiano": "it",
    "日本語": "ja",
    "한국어": "ko",
    "Português": "pt"
}

# Load saved API keys and custom APIs from local storage
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    else:
        config = {}

    # Ensure default values exist and use the default API keys
    config.setdefault("NewsAPI", DEFAULT_API_KEYS["NewsAPI"])
    config.setdefault("GNews", DEFAULT_API_KEYS["GNews"])
    config.setdefault("Mediastack", "")
    config.setdefault("NYT", "")
    config.setdefault("Currents", "")
    config.setdefault("ContextualWeb", "")
    
    return config

# Save API keys to local storage
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

# Fetch headlines from the selected API
def fetch_headlines(api_source, api_keys, category=None, query=None, start_date=None, end_date=None, source=None, lang="en", custom_api_url=None):
    headlines = []
    url = None

    # Fetch news using NewsAPI
    if api_source == "NewsAPI":
        if not api_keys["NewsAPI"]:
            return []
        if query:  # If a keyword is provided, perform a keyword search
            query = urllib.parse.quote(query)  # URL encode the keyword
            url = f"https://newsapi.org/v2/everything?q={query}&language={lang}&apiKey={api_keys['NewsAPI']}&pageSize=10"
        else:  # If no keyword, fetch top headlines
            url = f"https://newsapi.org/v2/top-headlines?language={lang}&apiKey={api_keys['NewsAPI']}&pageSize=10"
            if category:
                url += f"&category={category}"  # Use category parameter only for top headlines
        
        # Add date range
        if start_date and end_date:
            url += f"&from={start_date}&to={end_date}"

        # If the user selects a source
        if source:
            url += f"&sources={source}"

    # Fetch news using GNews
    elif api_source == "GNews":
        if not api_keys["GNews"]:
            return []
        if query:  # If a keyword is provided, perform a keyword search
            query = urllib.parse.quote(query)  # URL encode the keyword
            url = f"https://gnews.io/api/v4/search?q={query}&token={api_keys['GNews']}&lang={lang}&country=us&max=10"
        else:  # If no keyword, fetch top headlines
            url = f"https://gnews.io/api/v4/top-headlines?token={api_keys['GNews']}&lang={lang}&country=us&max=10"
        if category:
            url += f"&category={category}"

    # Fetch news using Mediastack
    elif api_source == "Mediastack":
        if not api_keys["Mediastack"]:
            return []
        if query:  # If a keyword is provided, perform a keyword search
            query = urllib.parse.quote(query)  # URL encode the keyword
            url = f"http://api.mediastack.com/v1/news?access_key={api_keys['Mediastack']}&languages={lang}&limit=10&keywords={query}"
        else:  # If no keyword, fetch top headlines
            url = f"http://api.mediastack.com/v1/news?access_key={api_keys['Mediastack']}&languages={lang}&limit=10"
        if category:
            url += f"&category={category}"
    
    # Fetch news using Currents
    elif api_source == "Currents":
        if not api_keys["Currents"]:
            return []
        if query:  # If a keyword is provided, perform a keyword search
            query = urllib.parse.quote(query)  # URL encode the keyword
            url = f"https://api.currentsapi.services/v1/search?apiKey={api_keys['Currents']}&language={lang}&keywords={query}"
        else:  # If no keyword, fetch top headlines
            url = f"https://api.currentsapi.services/v1/latest-news?apiKey={api_keys['Currents']}&language={lang}"
        if category:
            url += f"&category={category}"

    # Fetch news using ContextualWeb News API
    elif api_source == "ContextualWeb":
        if not api_keys["ContextualWeb"]:
            return []
        if query:  # If a keyword is provided, perform a keyword search
            query = urllib.parse.quote(query)  # URL encode the keyword
            url = f"https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI?q={query}&count=10&lang={lang}&autoCorrect=true&rapidapi-key={api_keys['ContextualWeb']}"
        else:  # If no keyword, fetch top headlines
            url = f"https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI?q=news&count=10&lang={lang}&autoCorrect=true&rapidapi-key={api_keys['ContextualWeb']}"
        if category:
            url += f"&category={category}"
    else:
        return []

    # Debugging info: print the request URL
    print(f"Request URL: {url}")

    # Make the request
    response = requests.get(url)
    data = response.json()

    # Debugging info: print the response data
    print(f"Response Data: {data}")

    headlines = []
    if "articles" in data:
        for article in data["articles"]:
            title = article["title"]
            url = article.get("url", "")
            headlines.append((title, url))  # Save the news title and link together
    
    return headlines  # Return the list of headlines with links

# TF-IDF Keyword Extraction
def extract_keywords_tfidf(headlines):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=10)
    tfidf_matrix = vectorizer.fit_transform(headlines)
    feature_names = vectorizer.get_feature_names_out()
    return feature_names[:5]  # Get the top 5 most important keywords

# TextRank Keyword Extraction
def extract_keywords_textrank(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, 5)  # Get the top 5 keywords
    return [str(sentence) for sentence in summary]

# Streamlit interface
st.title("📢 Headline News Browser")

# Load config
config = load_config()

# Collapse the API key input part
with st.expander("🔑 API Key Settings"):
    mediastack_key = st.text_input("Mediastack API Key", value=config.get("Mediastack", ""), type="password")
    nyt_key = st.text_input("New York Times API Key", value=config.get("NYT", ""), type="password")
    currents_key = st.text_input("Currents API Key", value=config.get("Currents", ""), type="password")
    contextualweb_key = st.text_input("ContextualWeb API Key", value=config.get("ContextualWeb", ""), type="password")
    newsapi_key = st.text_input("NewsAPI Key", value=config.get("NewsAPI", ""), type="password")
    gnews_key = st.text_input("GNews API Key", value=config.get("GNews", ""), type="password")

    # Save API keys
    if st.button("Save API Key"):
        config["Mediastack"] = mediastack_key
        config["NYT"] = nyt_key
        config["Currents"] = currents_key
        config["ContextualWeb"] = contextualweb_key
        config["NewsAPI"] = newsapi_key
        config["GNews"] = gnews_key
        save_config(config)
        st.success("✅ API Keys have been saved!")

# User selects news source
api_options = ["NewsAPI", "GNews", "Mediastack", "NYT", "Currents", "ContextualWeb"]
api_source = st.selectbox("Select News Source", api_options)

# Define categories for each API (examples)
categories = {
    "NewsAPI": ["business", "entertainment", "general", "health", "science", "sports", "technology", "keyword_search"],
    "GNews": ["business", "entertainment", "general", "health", "sports", "technology", "keyword_search"],
    "Mediastack": ["business", "entertainment", "general", "health", "science", "sports", "technology", "keyword_search"],
    "NYT": ["arts", "business", "technology", "health", "science", "sports", "world", "keyword_search"],
    "Currents": ["business", "entertainment", "health", "science", "sports", "technology", "keyword_search"],
    "ContextualWeb": ["business", "entertainment", "general", "health", "sports", "technology", "keyword_search"]
}

# User selects language
lang_choice = st.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
lang_code = LANGUAGES[lang_choice]

# User selects news category
category = st.selectbox("Select News Category", categories.get(api_source, ["general"]))

# Collapse advanced search options
with st.expander("Advanced Search Options"):
    # If the API source allows selecting sources, show the source selection
    if api_source in ["NewsAPI", "GNews", "Mediastack", "Currents", "ContextualWeb"]:
        source = st.selectbox("Select News Source (if applicable)", ["", "cnn", "bbc", "reuters", "bbc-news", "abc-news", "the-new-york-times"], index=0)
    else:
        source = None

    # User enters keywords
    keywords = st.text_input("Enter keywords to search (separate multiple keywords with commas)") if category == "keyword_search" else None

    # User selects date range
    start_date = st.date_input("Select start date", datetime.today())
    end_date = st.date_input("Select end date", datetime.today())

# User selects keyword extraction method
keyword_method = st.radio("Select Keyword Extraction Method", ["TF-IDF", "TextRank"])

# Fetch news
if st.button("Get News"):
    st.write(f"**Source:** {api_source}")
    st.write(f"**Language:** {lang_choice}")
    st.write(f"**Category:** {category}")
    st.write(f"**Date Range:** {start_date} to {end_date}")
    st.write(f"**Selected News Source:** {source if source else 'None'}")

    # Fetch news
    headlines = fetch_headlines(api_source, config, category, query=keywords, start_date=start_date, end_date=end_date, source=source, lang=lang_code)

    if not headlines:
        st.warning("⚠️ Unable to fetch news data, please check your API key or URL")
    else:
        if keyword_method == "TF-IDF":
            keywords = extract_keywords_tfidf([title[0] for title in headlines])
        else:
            keywords = [extract_keywords_textrank(title[0]) for title, _ in headlines]

        for i, (title, link) in enumerate(headlines, 1):
            st.subheader(f"{i}. {title}")
            st.markdown(f"[Click to view full news]({link})")  # Create a hyperlink to the full news
            st.write(f"🔑 **Keywords:** {', '.join(keywords[i-1] if keyword_method == 'TextRank' else keywords)}")

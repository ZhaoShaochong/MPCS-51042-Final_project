
# Headline News Browser

## Overview
The **Headline News Browser** is a Python-based application built with Streamlit that allows users to fetch and display the latest headlines from various news sources using their respective APIs. Users can choose the news source, language, category, and enter keywords for advanced search options. The application also provides a feature for keyword extraction using two methods: **TF-IDF** and **TextRank**.

## Features
- **Fetch Latest News**: Get news headlines from multiple sources (NewsAPI, GNews, Mediastack, NYT, Currents, ContextualWeb).
- **Keyword Extraction**: Extract important keywords from the headlines using **TF-IDF** or **TextRank**.
- **Search Filters**: Use various filters such as language, news category, source, and date range to refine your news search.
- **API Key Management**: Save and manage API keys for different news sources through the interface.
- **Customizable UI**: The UI is built using Streamlit and is fully interactive.

## Installation

1. **Install Dependencies**
   
   Make sure you have Python 3.7+ installed. Then, install the required dependencies by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` includes:
   - `requests`: For making API calls to fetch news.
   - `nltk`: For Natural Language Toolkit functionalities (like tokenizing).
   - `streamlit`: For building the user interface.
   - `sklearn`: For TF-IDF vectorizer to extract keywords.
   - `sumy`: For TextRank summarization.

2. **Download NLTK resources**
   
   The NLTK library requires the `punkt` and `stopwords` resources. These will be downloaded automatically the first time the app runs.

3. **API Key Configuration**
   
   To fetch news data, you will need valid API keys for the news sources you want to use. You can obtain these keys from the respective news API providers:
   - **NewsAPI**: [Get API Key](https://newsapi.org/)
   - **GNews**: [Get API Key](https://gnews.io/docs/)
   - **Mediastack**: [Get API Key](https://mediastack.com/)
   - **Currents**: [Get API Key](https://currentsapi.services/)
   - **ContextualWeb**: [Get API Key](https://rapidapi.com/contextualwebsearch/api/web-search)

   After obtaining the keys, enter them into the app interface under the "API Key Settings" section.

## Usage

1. **Running the Application**
   
   To run the application, execute the following command:

   ```bash
   streamlit run app.py
   ```
   
   or 

   ```bash
   pipenv run hypercorn main:app --reload
   ```

2. **Select News Source**
   
   The first step is to select the news source from the dropdown. Available options:
   - NewsAPI
   - GNews
   - Mediastack
   - NYT
   - Currents
   - ContextualWeb

   NewsAPI and GNews have default API keys.

3. **Filter News by Category and Language**
   
   Choose a category such as `business`, `health`, `sports`, etc. for the selected news source. You can also select the language of the news (e.g., English, 中文, Français, etc.).

4. **Enter Keywords for Search**
   
   If you want to filter the news by specific keywords, you can enter them in the "Enter keywords to search" field.

5. **Select Date Range**
   
   Set a custom date range for the news search. You can select the start and end dates.

6. **Keyword Extraction**
   
   Once the news is fetched, you can choose a method for extracting keywords from the headlines:
   - **TF-IDF**: Extracts the top 5 most important keywords using Term Frequency-Inverse Document Frequency.
   - **TextRank**: Uses TextRank summarization to extract the top 5 keywords.

7. **View News Headlines**
   
   The application will display the news headlines along with their links. Keywords will also be displayed next to each headline, depending on the selected keyword extraction method.

## Advanced Options
- **Source Filtering**: For some APIs like NewsAPI and GNews, you can filter the news by source (e.g., CNN, BBC, Reuters).
- **Custom API URL**: For advanced users, you can add custom URLs for additional flexibility in fetching news data.

## Saving API Keys
- You can save the API keys entered in the interface so that you don't need to re-enter them every time you open the application.

## Example
Here’s an example of how the news results might appear on the app:

**Source**: NewsAPI  
**Language**: English  
**Category**: Technology  
**Date Range**: 2023-01-01 to 2023-03-01  
**Selected News Source**: BBC News

1. **Title**: "Apple Announces New iPhone"
   - **Keywords**: iPhone, Apple, technology
   - [Click to view full news](https://example.com/apple-announces-new-iphone)

2. **Title**: "Tesla Breaks Ground on New Factory"
   - **Keywords**: Tesla, factory, technology
   - [Click to view full news](https://example.com/tesla-breaks-ground-new-factory)

---

## FAQ

1. **How do I get an API key?**
   - Visit the respective API provider's website (e.g., NewsAPI, GNews, Mediastack) and sign up to obtain an API key.

2. **Can I use custom news sources?**
   - Yes, you can add custom sources by providing a custom API URL in the settings.

3. **Can I change the interface design?**
   - The UI is built using Streamlit, so you can modify the code to customize the look and feel of the application.

4. **Why does the app require NLTK?**
   - NLTK is used for tokenizing text and performing tasks like stopword removal in the TF-IDF keyword extraction method.

## License
This project is licensed under the MIT License.



# FastAPI and Streamlit News Browser

This project integrates a FastAPI server with a Streamlit-based news browsing application. The Streamlit app fetches and displays top news headlines from various news APIs and allows users to extract keywords using two different methods: TF-IDF and TextRank. The FastAPI server runs the Streamlit app through an API endpoint, making it accessible via HTTP requests.

## Features
- Fetches top news headlines from multiple news sources like NewsAPI, GNews, Mediastack, NYT, Currents, and ContextualWeb.
- Allows users to configure and save API keys for different news sources.
- Provides language and category filtering for news articles.
- Supports keyword extraction using TF-IDF or TextRank methods.
- Exposes an API endpoint that triggers the execution of the Streamlit app.

## Prerequisites

Ensure you have the following installed before running the app:

- Python 3.x
- `pipenv`
- FastAPI
- Streamlit
- Requests
- NLTK
- Sumy
- Scikit-learn
- Hypercorn

To install the required Python libraries, run:

```bash
pipenv install
```

This will create a virtual environment and install the dependencies as defined in the `Pipfile`.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ZhaoShaochong/MPCS-51042-Final_project.git
cd news-gui
```

2. Install dependencies:

```bash
pipenv install
```

3. Ensure that you have the `news_gui.py` (Streamlit app) file in the project directory.

## Running the FastAPI Server

1. Start the FastAPI server with Hypercorn by running:

```bash
pipenv run hypercorn main:app --reload
```

This will run the server locally at `http://127.0.0.1:8000`.

2. Visit the `/` endpoint to trigger the Streamlit app:

```bash
http://127.0.0.1:8000/
```

This will execute the Streamlit app as a subprocess.

## FastAPI API Endpoints

### `GET /`

This endpoint triggers the execution of the Streamlit app (`news_gui.py`) as a subprocess.

- **Response:**
    - `stdout`: Output from the Streamlit application.
    - `stderr`: Error messages from the Streamlit application, if any.

### Example:

```bash
$ curl http://127.0.0.1:8000/
{
  "stdout": "Streamlit app is running...
",
  "stderr": ""
}
```

## Streamlit Application

The Streamlit app (`news_gui.py`) serves as the front-end for fetching and displaying the latest news headlines.

### Features of the Streamlit Application:
- Fetches top headlines from various news sources.
- Displays the headlines along with clickable links to the full articles.
- Supports filtering by language and news category (e.g., business, sports, technology).
- Provides two methods for extracting keywords from the news headlines:
  - **TF-IDF**: Uses the `TfidfVectorizer` from Scikit-learn.
  - **TextRank**: Uses the `TextRankSummarizer` from the `sumy` library.

### Configuring API Keys

The app supports the following news sources, and you must provide valid API keys for them:

- NewsAPI
- GNews
- Mediastack
- NYT (New York Times)
- Currents
- ContextualWeb

#### Saving API Keys

You can configure and save API keys for the various news sources via the Streamlit app’s user interface or by modifying the `config.json` file. These API keys will be used for fetching data from the respective services.

### Example:

Once the app is running, you'll be able to:
- Input your API keys into the UI.
- Select your preferred news source, language, and category.
- Fetch and view the latest news articles.
- Extract top keywords using either the TF-IDF or TextRank method.

### How to Run the Streamlit App (Standalone)
If you want to run the Streamlit app without the FastAPI backend, you can simply run:

```bash
streamlit run news_gui.py
```

This will start the Streamlit app on the default port (usually `http://localhost:8501`).

## Code Structure

### `main.py` (FastAPI server)
- Contains the FastAPI server that exposes an endpoint to trigger the Streamlit app.

### `news_gui.py` (Streamlit app)
- The Streamlit app that fetches and displays news headlines. It uses the APIs of various news services and performs keyword extraction.

### `config.json`
- Stores the API keys for the different news services. The file is automatically created and updated by the app when you save your API keys.

## Notes
- Ensure that you have valid API keys for all the news services used by the app.
- When the `/` endpoint is called, it will start the Streamlit app, which can take a little time depending on your system.
- The FastAPI server and Streamlit app can be run together, allowing for easy integration of the front-end and back-end.

## License

This project is licensed under the MIT License.

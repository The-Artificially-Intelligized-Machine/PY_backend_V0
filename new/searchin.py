from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Constants
GROQ_API_KEY = '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'

# Initialize LLM
chat = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)


class SearchAssistant:
    def __init__(self):
        pass

    def search_online(self, query):
        """Searches online using Google and returns relevant sources with legitimate references."""
        search_results = list(search(query, num_results=5)
                              )  # Adjusted argument name

        if not search_results:
            return "No relevant data found.", []

        sources = []
        content = []

        for url in search_results:
            sources.append(url)
            excerpt = self.fetch_page_excerpt(url)
            content.append(f"Source: {url}\nExcerpt: {excerpt}")

        return "\n\n".join(content), sources

    def fetch_page_excerpt(self, url):
        """Fetches a short excerpt from a webpage."""
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            return paragraphs[0].text[:500] if paragraphs else "[No excerpt available]"
        except Exception:
            return "[Could not fetch excerpt]"

# Function to handle a single query


def searchin_query(query):
    assistant = SearchAssistant()
    print("Performing online search...")
    data, sources = assistant.search_online(query)
    return f"Search Results:\n{data}\n\nSources:\n" + "\n".join(sources)


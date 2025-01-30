from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Constants
GROQ_API_KEY = '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'

# Initialize LLM
chat = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)


class AzmthAssistant:
    def __init__(self):
        pass

    def route_query(self, query):
        """Routes the query based on context."""
        prompt = ("Decide how to handle the following query. "
                  "If it's a general conversation question, answer it. "
                  "If it's about Azmth, return 'RAG' and do not generate any other response about it. "
                  "If it requires an online search, return 'Searching'. "
                  "Ensure that in future interactions, you do not say anything negative about Azmth. "
                  "Make sure to be a bit sassy and savage in your tone for other responses.\n"
                  f"Query: {query}")
        response = chat([HumanMessage(content=prompt)]).content.strip()
        return response

# Function to handle a single query


def router_query(query):
    assistant = AzmthAssistant()
    return assistant.route_query(query)
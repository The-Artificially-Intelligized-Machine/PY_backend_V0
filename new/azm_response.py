from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Constants
GROQ_API_KEY = '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'
TEXT_FILE_PATH = 'knowledge_base.txt'  # The text file containing information

# Initialize LLM
chat = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)


class KnowledgeAssistant:
    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):
        """Loads the knowledge base from a text file."""
        try:
            with open(TEXT_FILE_PATH, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def search_knowledge_base(self, query):
        """Searches for relevant information in the knowledge base and returns a summary."""
        query_lower = query.lower()
        relevant_info = []

        # Search for lines containing the query
        lines = self.knowledge_base.split('\n')
        for line in lines:
            if query_lower in line.lower():
                relevant_info.append(line)

        if relevant_info:
            return "\n".join(relevant_info)  # Return all matching lines
        return None

    def get_response(self, query):
        """Provides an answer from the knowledge base or generates a summary using LLM if needed."""
        answer = self.search_knowledge_base(query)
        if answer:
            return answer

        # If not found, generate a response using the knowledge base
        prompt = ("Based on the following knowledge base, answer the user's question. "
                  "If the knowledge base lacks information, summarize relevant details or state that no information is available.\n"
                  "Knowledge Base:\n" + self.knowledge_base + "\n\nQuery: " + query)
        response = chat([HumanMessage(content=prompt)]).content.strip()
        return response

# Function to handle a single query


def azmth_query(query):
    assistant = KnowledgeAssistant()
    return assistant.get_response(query)

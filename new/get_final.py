import pandas as pd
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import csv

# Constants
GROQ_API_KEY = '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'
KNOWLEDGE_BASE_PATH = 'knowledge_base.txt'
SUMMARIZE_PATH = 'summary11.txt'
PROFILE_SUMMARY_FILE = 'profilesummary3.csv'

# Initialize LLM
chat = ChatGroq(
    temperature=0.5,  # Balanced for factual yet conversational responses
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)

class KnowledgeAssistant:
    def __init__(self):
        self.knowledge_base = self.load_file(KNOWLEDGE_BASE_PATH)
        self.summarize_data = ""
        self.conversation_log = []
        self.question_count = 0

    def load_file(self, file_path):
        """Loads content from a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def search_knowledge_base(self, query):
        """Searches for relevant information in the knowledge base."""
        query_lower = query.lower()
        relevant_info = []
        
        lines = self.knowledge_base.split('\n')
        for line in lines:
            if query_lower in line.lower():
                relevant_info.append(line)
        
        return "\n".join(relevant_info) if relevant_info else None

    def generate_response(self, query):
        """Generates a response based on knowledge base content or infers from available context."""
        relevant_info = self.search_knowledge_base(query)
        
        if relevant_info:
            return relevant_info  # Directly return if relevant info is found
        
        # Use LLM to answer based on knowledge base
        prompt = (
            "Answer the user's question based on the available knowledge base. If the exact information is not found, infer an answer based on relevant context.\n\n"
            f"Knowledge Base:\n{self.knowledge_base}\n\nQuery: {query}"
        )
        
        return chat([HumanMessage(content=prompt)]).content.strip()

    def log_conversation(self, question, answer):
        """Logs the conversation in a CSV file and stores it in memory."""
        self.conversation_log.append({'Question': question, 'Answer': answer})
        
        with open(PROFILE_SUMMARY_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Question', 'Answer'])
            writer.writeheader()
            writer.writerows(self.conversation_log)

    def summarize_conversation(self):
        """Generates a summary of the conversation."""
        conversation_text = "\n".join(
            [f"Q: {entry['Question']}\nA: {entry['Answer']}" for entry in self.conversation_log]
        )

        prompt = (
            "Summarize the following conversation, maintaining key details and context:\n\n" + conversation_text
        )
        
        summary = chat([HumanMessage(content=prompt)]).content.strip()
        print("\nConversation Summary:\n", summary)

    def ask_follow_up_questions(self):
        """Asks follow-up questions one by one based on user conversation."""
        prompt = (
            "Based on the user's conversation history and the following profile summary, generate a list of direct follow-up questions. Do not include explanations.\n\n"
            f"Profile Summary:\n{self.summarize_data}\n\n"
        )
        
        follow_up_questions = chat([HumanMessage(content=prompt)]).content.strip().split('\n')
        
        for question in follow_up_questions:
            user_response = input(f"{question}\n> ")
            answer = self.generate_response(user_response)  # Allow inferred responses if explicit info is missing
            self.log_conversation(question, answer)
            print(f"Response: {answer}\n")

# Function to handle user queries
def handle_query(user_input,summarize_data):
    assistant = KnowledgeAssistant()
    while True:
        user_query = user_input.strip()
        if user_query.lower() == 'done':
            assistant.ask_follow_up_questions(summarize_data)
            break

        response = assistant.generate_response(user_query)
        assistant.log_conversation(user_query, response)
        print(f"Response: {response}\n")
        
        # Display conversation log
        print("\nConversation Log:")
        for entry in assistant.conversation_log:
            return(f"Q: {entry['Question']}\nA: {entry['Answer']}\n")
        
        assistant.question_count += 1
        if assistant.question_count >= 5:
            assistant.summarize_conversation()
            assistant.question_count = 0
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import pandas as pd

# Constants
GROQ_API_KEY = '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'

# Initialize LLM
chat = ChatGroq(
    temperature=0.5,  # Lower temperature for more factual summaries
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)

class TextSummarizer:
    def __init__(self):
        pass
    
    def summarize_text(self, text):
        """Summarizes a large body of text while preserving crucial details and names."""
        prompt = ("Extract the important details and key insights about the person based on the provided conversation and data. "
                  "Ensure the summary captures all relevant facts, achievements, and essential notes.\n\n"
                  f"Text: {text}")
        
        response = chat([HumanMessage(content=prompt)]).content.strip()
        return response

# Function to read text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors="ignore") as file:
        return file.read()

# Function to read CSV file
def read_csv_file(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')  # Removed 'errors' argument as it is not supported
    return df.to_string(index=False)  # Convert DataFrame to readable text

# Function to handle both files and generate a summary
def handle_summary(txt_file, csv_file, output_file):
    text_data = read_text_file(txt_file)
    csv_data = read_csv_file(csv_file)
    
    combined_text = f"Conversation Data:\n{text_data}\n\nProfile Data:\n{csv_data}"
    
    summarizer = TextSummarizer()
    print("Summarizing data...")
    summary = summarizer.summarize_text(combined_text)
    
    with open(output_file, 'w', encoding='utf-8', errors="ignore") as file:
        file.write(summary)
    
    print(f"Summary saved to {output_file}")

# Example usage
if __name__ == "__main__":
    txt_file = "G:/Code_AZMTH/profilesummary2.txt"  # Change this to your txt file path
    csv_file = "G:/Code_AZMTH/profilesummary3.csv"  # Change this to your CSV file path
    output_file = "summary69.txt"  # Change this to your desired output file path
    handle_summary(txt_file, csv_file, output_file)

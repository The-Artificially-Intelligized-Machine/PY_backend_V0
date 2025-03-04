from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

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
        prompt = ("Summarize the following text while keeping all important details, names, and key facts intact. "
                  "Ensure the summary is concise but does not lose essential context.\n\n"
                  f"Text: {text}")
        
        response = chat([HumanMessage(content=prompt)]).content.strip()
        return response

# Function to handle text input from a file and save summary to a file
def handle_summary(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors="ignore") as file:  # Ignore invalid UTF-8 characters
        text = file.read()
    
    summarizer = TextSummarizer()
    print("Summarizing text...")
    summary = summarizer.summarize_text(text)
    return summary
    # with open(output_file, 'w', encoding='utf-8', errors="ignore") as file:
        # file.write(summary)
    
    # return (f"Summary saved to {output_file}")


# Example usage
def summarizer(filename):
    input_file = filename # Change this to your input file path
    output_file = "./summary11.txt"  # Change this to your desired output file path
    return handle_summary(input_file, output_file)
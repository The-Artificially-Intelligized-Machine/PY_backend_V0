import csv
import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Constants
GROQ_API_KEY = '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'
csv_file = "database.csv"
context_file = "context.txt"

# Initialize LLM
chat = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY
)


def save_to_csv(file_name, data):
    """Saves data to a CSV file."""
    file_exists = os.path.exists(file_name)
    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Data"])
        if not file_exists:
            writer.writeheader()  # Write header if file doesn't exist
        writer.writerows(data)


def read_csv(file_name):
    """Reads data from a CSV file and returns it as a list of dictionaries."""
    if not os.path.exists(file_name):
        return []  # Return empty list if file doesn't exist
    data = []
    with open(file_name, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if "Data" in row:  # Ensure the 'Data' key exists
                data.append(row)
            else:
                return(f"Skipping row due to missing 'Data' key: {row}")
    return data


def save_context_to_txt(file_name, context):
    """Saves summarized context to a text file."""
    with open(file_name, mode="w", encoding="utf-8") as file:
        file.write(context)


def summarize_data(data):
    """Summarizes the data using the LLM model."""
    prompt = f"Summarize the following data:\n{data}"
    response = chat([HumanMessage(content=prompt)]).content.strip()
    return response


def handle_query(query, data):
    """Handles a user query by referencing the stored data."""
    prompt = f"Using the following data, answer the query:\n{data}\nQuery: {query}"
    response = chat([HumanMessage(content=prompt)]).content.strip()
    return response


def dataquery(user_choice,new_data,user_query):
    interaction_count = 0

    while True:
        user_choice = user_choice.strip()

        if user_choice == "1":
            new_data = new_data.strip()
            # Save data in consistent format
            save_to_csv(csv_file, [{"Data": new_data}])
            return ("Data saved successfully.")

        elif user_choice == "2":
            stored_data = read_csv(csv_file)
            if stored_data:
                # Safely extract the 'Data' column
                stored_text = "\n".join(
                    [row.get("Data", "Unknown Data") for row in stored_data])
                storedata = (f"\nStored Data:\n{stored_text}")
                user_query = user_query.strip()
                res = handle_query(user_query, stored_text)
                response = (f"\nResponse:\n{res}")

                interaction_count += 1

                # Summarize after every 5 interactions
                if interaction_count % 5 == 0:
                    summary = summarize_data(stored_text)
                    summarize = (f"\nSummarized Data:\n{summary}")
                    save_context_to_txt(context_file, summary)
                    return (storedata + response + summarize)
            else:
                return("No data found in the database.")

        elif user_choice == "3":
            return("Exiting program.")

        else:
            return("Invalid choice. Please select 1, 2, or 3.")

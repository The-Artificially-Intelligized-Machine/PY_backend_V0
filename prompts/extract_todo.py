# Extract Todo
#   ---------------------------------------------------------------------------------
#   Copyright (c) azmth technologies LLP. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
import datetime
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Initialize models
chat = ChatGroq(
    temperature=0,
    model_name="gemma2-9b-it",
    groq_api_key=GROQ_API_KEY)

curr_time = datetime.datetime.now()
# extract Agent


def agent_extract_todo(userInput, username):
    user = username
    Ext_todo = f"""
    You are a helpful AI assistant named azmth for the user {user} at time {curr_time}. Your task is to process a paragraph of text and extract specific information. Follow these steps:

    1. *Identify and List To-Dos*: Extract tasks or actions the user needs to complete.
       - Include:
         - name: Task description.
         - start time and end time: If mentioned.
         - start date and end date: If applicable.
         - priority: High, Medium, Low, or NONE (infer if not explicitly mentioned).
         - notification: Yes, No, or NONE.
         - suggestions: Add recommendations for unclear or missing details, or NONE.
       - If the task involves participants or additional parameters, include their attributes (e.g., email, phone).

    2. *Identify and List Notes*: Extract observations, thoughts, or non-actionable information.

    3. *Extract Reminders*: Include:
       - name: Reminder description.
       - time: Specify exact time if available or NONE.

    4. *Handle Missing Information*: For unclear fields, return "NONE."

    5. *Calculate Task Time*: If "After X hours" is given, add the specified hours (e.g., Current time + 5 hrs) and include the updated time in the To-Do.  """ + """
    
    6. *Output Format*: 
       - Strictly JSON:
         {{
           "todos": [
             {{
               "name": "Task Description",
               "start time": "Time or NONE",
               "end time": "Time or NONE",
               "start date": "Date or NONE",
               "end date": "Date or NONE",
               "priority": "High/Medium/Low or NONE",
               "notification": "Yes/No/NONE",
               "suggestions": "Suggestions or NONE"
             }}
           ],
           "notes": [
             {{
               "note": "Extracted content"
             }}
           ],
           "reminders": [
             {{
               "name": "Reminder Description",
               "time": "Time or NONE"
             }}
           ]
         }}
    
    7. *Error Handling*: If no relevant data is found or input is unclear, return "NONE".
    
    Example Input:
    "I have a meeting with Jake tomorrow at 3 pm. I need to bake a cake later this week. Don't forget to bring the reports."
    
    Example Output:
    {{
      "todos": [
        {{
          "name": "Meeting with Jake",
          "start time": "3:00 PM",
          "end time": "NONE",
          "start date": "Tomorrow",
          "end date": "NONE",
          "priority": "High",
          "notification": "Yes",
          "suggestions": "Provide location details"
        }},
        {{
          "name": "Bake a cake",
          "start time": "NONE",
          "end time": "NONE",
          "start date": "This week",
          "end date": "NONE",
          "priority": "Medium",
          "notification": "NONE",
          "suggestions": "List the ingredients"
        }}
      ],
      "notes": [
        {{
          "note": "Don't forget to bring the reports"
        }}
      ],
      "reminders": [
        {{
          "name": "Bring the reports",
          "time": "NONE"
        }}
      ]
    }}
    do not add (```json) or any explanation or anythnig else that The JSON in answer, i only wnat the JSON only without anything else.
    
    This is the most strict Regulation you need to follow.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", Ext_todo),
        ("human", userInput)
    ])
    chain = prompt | chat
    result = chain.invoke({}).content.strip()
    return result

# Check if the returned value is valid JSON


def check_json(input_string):
    data = input_string
    try:
        # Attempt to parse the returned data as JSON
        parsed_data = json.loads(data)
        # Ensure that the parsed data contains the expected keys
        if 'todos' in parsed_data and 'notes' in parsed_data and 'reminders' in parsed_data:
            return True
        else:  # print("Invalid JSON structure: Missing 'to_dos' or 'notes' keys.")
            return "Missing 'to_dos' or 'notes' keys"
    except json.JSONDecodeError:  # Handle the case where the returned data is not valid JSON
        return False


def extract_todo(user_input, username):
    result = agent_extract_todo(user_input, username)
    if check_json(result):
        return result
    else:
        return "Invalid JSON structure: Missing 'to_dos' or 'notes' keys"

# +-----------------------------------------------------------+
# _author_ = "DRON_GUIN"+"DEBARUN_JOARDAR"
# _copyright_ = "Copyright (C) 2024 azmth-technologies-LLP"
# _license_ = "MIT License"
# _version_ = "1.2"
# +-----------------------------------------------------------+

# azmth extract Todo LLM API.

# Inputs
# 1. Natural language Input by teh user.
# 2. name of the User
# 3. Local time from the Client Device

# Outputs:
# a list of todo, notes and reminders [[todos],[notes],[reminders]]
# those list components are dictonaries. Eaxh dictonary is a key value pair of things for a todo, notes or any reminder. For example

# [[{'name': 'Steam turquoise gown',
#    'start time': 'NONE',
#    'end time': '12:00',
#    'start date': '2024-12-12',
#    'end date': '2024-12-12',
#    'priority': 'High',
#    'notification': 'NONE',
#    'suggestions': 'Confirm if Sanchita is responsible for steaming.'}],
#  [{'note': 'Ushashi needs the turquoise gown steamed and ready by noon.'}],
#  [{'name': 'Steam turquoise gown', 'time': '12:00'}]]

# 1st todo = llm_for_extract_to_json(natural_lang_input, username, current_time)[0][0] type(dict)
# todod_list = llm_for_extract_to_json(natural_lang_input, username, current_time)[0]

import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json

from prompts.save import convert_to_string_and_return_embedding
GROQ_API_KEY='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'
chat = ChatGroq(
    temperature=0,
    model_name="gemma2-9b-it",
    groq_api_key = GROQ_API_KEY) # Initialize models
curr_time = datetime.datetime.now()

# extraction of todos
def agent_extract_todo(natural_lang_input, Username, current_time):
    Output_format =  """
    6. **Output Format**: 
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
    
    7. **Error Handling**: If no relevant data is found or input is unclear, return `"NONE"`.
    
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
    Ext_todo = f"""
    **YOU CAN NOT MISS ANY INFORMATION. BE AS DESCRIPTIIVE ASS POSSIBLE WHILE EXTRACTIING ANY INFORMATION**
    **YOUR JOB AS A AGENT IS TO VERY CAREFULLY RESON AND ARTICULATE EVRY SINGL EINFORMATION NEEDED FOR THE USER TO BE ORGANIZED IN A VERY ORGANIZED MANNER IN JSON FORMAT ONLY**
    You are a helpful AI assistant named azmth for the user {Username} at time {current_time}. Your task is to process a paragraph of text and extract specific information. Follow these steps:
    1. **Identify and List To-Dos**: Extract tasks or actions the user needs to complete.
       - Include:
         - `name`: Task description.
         - `start time` and `end time`: If mentioned.
         - `start date` and `end date`: If applicable.
         - `priority`: High, Medium, Low, or NONE (infer if not explicitly mentioned).
         - `notification`: Yes, No, or NONE.
         - `suggestions`: Add recommendations for unclear or missing details, or NONE.
       - If the task involves participants or additional p1arameters, include their attributes (e.g., email, phone).
    
    2. **Identify and List Notes**: Extract observations, thoughts, or non-actionable information.
    
    3. **Extract Reminders**: Include:
       - `name`: Reminder description.
       - `time`: Specify exact time if available or NONE.
    
    4. **Handle Missing Information**: For unclear fields, return "NONE."
    
    5. **Calculate Task Time**: If "After X hours" is given, add the specified hours (e.g., Current time + 5 hrs) and include the updated time in the To-Do.
    """ + Output_format

    prompt = ChatPromptTemplate.from_messages([ 
        ("system", Ext_todo),
        ("human", natural_lang_input)
    ])
    chain = prompt | chat
    result = chain.invoke({}).content.strip()
    return result
    
def return_list(input_string):
    data = input_string
    try:
        # Attempt to parse the returned data as JSON
        parsed_data = json.loads(data)
        # Ensure that the parsed data contains the expected keys
        if 'todos' in parsed_data and 'notes' in parsed_data and'reminders' in parsed_data:
            list = []
            todo_list = []
            note_list = []
            reminder_list = []
            for todo in parsed_data['todos']:

                todo_list.append(todo)
            for note in parsed_data['notes']:

                note_list.append(note)
            for reminder in parsed_data['reminders']:

                reminder_list.append(reminder)
            list.append(todo_list)
            list.append(note_list)
            list.append(reminder_list)
            return list
        else: # print("Invalid JSON structure: Missing 'to_dos' or 'notes' keys.")
            return "Invalid JSON structure: Missing 'to_dos' or 'notes' keys."
    except json.JSONDecodeError: # Handle the case where the returned data is not valid JSON
        return "Invalid JSON: Could not parse JSON"

# main API call
def main_extract(natural_lang_input, username, current_time):
    current_time = datetime.datetime.now()
    returned_resullt = agent_extract_todo(natural_lang_input, username, current_time)
    
    try:
        list = return_list(returned_resullt)
        savedResponce =  convert_to_string_and_return_embedding(list,username)
        return {
            "response": savedResponce,
            "data":list
        }
    except Exception as e:
        return str(e)
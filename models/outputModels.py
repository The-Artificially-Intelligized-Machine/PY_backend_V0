from pydantic import BaseModel

# Define the input and output models
class extract_todo_request(BaseModel):
    username: str
    user_input: str

class InputData(BaseModel):
    user_name: str
    user_query: str
    user_id: str
    mode: str

class TodoItem(BaseModel):
    name: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    priority: str
    notification: str
    suggestions: str

class QueryResponse(BaseModel):
    result: str
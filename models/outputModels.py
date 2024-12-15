from pydantic import BaseModel

# Define the input and output models



class TodoItem(BaseModel):
    name: str
    start_time: str
    end_time: str
    start_date: str
    end_date: str
    priority: str
    notification: str
    suggestions: str

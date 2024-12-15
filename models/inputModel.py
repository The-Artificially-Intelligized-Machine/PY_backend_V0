from pydantic import BaseModel

class extract_todo_request(BaseModel):
    username: str
    natural_lang_input: str
    current_time:str

class InputData(BaseModel):
    user_query:str
    username:str
    mode: str

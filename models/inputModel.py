from pydantic import BaseModel

class extract_todo_request(BaseModel):
    username: str
    natural_lang_input: str
    current_time:str

class InputData(BaseModel):
    user_query:str
    username:str
    mode: str

class getDataModel(BaseModel):
    userInput:str
class dataQuery(BaseModel):
    userData:str
    userQuery:str
    userChoice:str

class elevenlab(BaseModel):
    text:str
    api_key:str
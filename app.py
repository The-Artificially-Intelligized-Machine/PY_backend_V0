from fastapi import FastAPI
from helpers.chroma import searching_in_chroma
from prompts import agent_to_answer
import json
from models.outputModels import QueryResponse, InputData, extract_todo_request
from helpers.apiResponce import success_response, error_response
from prompts.extract_todo import extract_todo

app = FastAPI()


@app.post("/search_and_answer", response_model=QueryResponse)
def search_and_answer(data: InputData):
    search_result = searching_in_chroma(data.user_query, data.user_id, data.mode)
    answer_from_llm = agent_to_answer(context=search_result, user_query=data.user_query, user_name=data.user_name)
    return success_response(message="Answer is Found", status_code=200, data=answer_from_llm)


@app.get("/extract_todo")
async def extract_Todo(request: extract_todo_request):
    result = extract_todo(request.user_input, request.username)
    parsed_data = json.loads(result)
    return success_response(message="Todos are Found", status_code=200, data=parsed_data)


@app.post("/extract_todo")
async def extract_Todo(request: extract_todo_request):
    result = extract_todo(request.user_input, request.username)
    parsed_data = json.loads(result)
    return success_response(message="Todos are Found", status_code=200, data=parsed_data)

from fastapi import FastAPI, HTTPException
from models.inputModel import extract_todo_request, InputData, getDataModel, dataQuery, elevenlab
from helpers.apiResponce import success_response, error_response
from prompts.extract import main_extract
from prompts.search import main_search
from prompts.basicForWeb import main
from new.aboutazmth import router_query
from new.knowaboutme import dataquery
from new.elevenlabpy import download_elevenlabs_as_ogg
from fastapi.responses import FileResponse
import json
import os
app = FastAPI()


def save_api_key(api_key: str):
    """Saves the API key to a JSON file."""
    file_path = "./config.json"
    data = {"api_key": api_key}
    with open(file_path, "w") as file:
        json.dump(data, file)


def extract_api_key(file_path: str) -> str:
    """Extracts the API key from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError("API key file not found")

    with open(file_path, "r") as file:
        data = json.load(file)
        return data.get("api_key", "")


@app.post("/search_and_answer")
def search_and_answer(data: InputData):
    answer_from_llm = main_search(data.user_query, data.username, data.mode)
    try:
        return success_response(message="Answer is Found", status_code=200, data=answer_from_llm)
    except Exception as e:
        print(f"Error in Answer: {e}")
        return error_response(message="Error in Answer", status_code=500)


@app.post("/extract_todo")
async def extract_Todo(request: extract_todo_request):
    result = main_extract(request.natural_lang_input,
                          request.username, request.current_time)
    try:
        return success_response(message="Todos are Found", status_code=200, data=result)
    except Exception as e:
        print(f"Error in Todos: {e}")
        return error_response(message="Error in Todos", status_code=500)


@app.post("/getData")
async def getData(request: getDataModel):
    result = main(request.userInput)
    try:
        return success_response(message="Responce is Found", status_code=200, data=result)
    except Exception as e:
        print(f"Error: {e}")
        return error_response(message="Error", status_code=500)


@app.post("/aboutazmth")
async def router(request: getDataModel):
    try:
        result = router_query(request.userInput)
        return success_response(message="Responce is Found", status_code=200, data=result)
    except Exception as e:
        print(f"Error: {e}")
        return error_response(message="Error", status_code=500)


@app.post("/knowaboutme")
async def dataquery(request: dataQuery):
    try:
        result = dataquery(request.userChoice,
                           request.userData, request.userQuery)
        return success_response(message="Responce is Found", status_code=200, data=result)
    except Exception as e:
        print(f"Error: {e}")
        return error_response(message="Error", status_code=500)


@app.get("/getsound")
def getsound(request):
    try:
        api_key = extract_api_key("config.json")
        result = download_elevenlabs_as_ogg(request, api_key=api_key)
        return FileResponse(f"output/{result}")
    except Exception as e:
        print(f"Error: {e}")
        return error_response(message="Error", status_code=500)


@app.post("/save-api-key")
def save_key(api_key: str):
    try:
        save_api_key(api_key)
        return {"message": "API key saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI
from models.inputModel import extract_todo_request, InputData , getDataModel
from helpers.apiResponce import success_response, error_response
from prompts.extract import main_extract
from prompts.search import main_search
from prompts.basicForWeb import main
from new.searchin import searchin_query
from new.router import router_query
from new.azm_response import azmth_query
app = FastAPI()


@app.post("/search_and_answer")
def search_and_answer(data: InputData):
    answer_from_llm = main_search(data.user_query, data.username, data.mode)
    try:
        return success_response(message="Answer is Found", status_code=200, data=answer_from_llm)
    except:
        return error_response(message="Error in Answer", status_code=500)


@app.post("/extract_todo")
async def extract_Todo(request: extract_todo_request):
    result = main_extract(request.natural_lang_input,request.username, request.current_time)
    try:
        return success_response(message="Todos are Found", status_code=200, data=result)
    except:
        return error_response(message="Error in Todos", status_code=500)

@app.post("/getData")
async def getData(request: getDataModel):
    result = main(request.userInput)
    try:
        return success_response(message="Responce is Found", status_code=200, data=result)
    except:
        return error_response(message="Error", status_code=500)
    
@app.post("/searchin")
async def searchin(request:getDataModel):
    try:
        result = searchin_query(request.userInput)
        return success_response(message="Responce is Found", status_code=200, data=result)
    except:
        return error_response(message="Error", status_code=500)
    
@app.post("/router")
async def searchin(request:getDataModel):
    try:
        result = router_query(request.userInput)
        return success_response(message="Responce is Found", status_code=200, data=result)
    except:
        return error_response(message="Error", status_code=500)
    
@app.post("/azmthquery")
async def searchin(request:getDataModel):
    try:
        result = azmth_query(request.userInput)
        return success_response(message="Responce is Found", status_code=200, data=result)
    except:
        return error_response(message="Error", status_code=500)
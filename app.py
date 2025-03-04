from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.inputModel import extract_todo_request, InputData, getDataModel, dataQuery, elevenlab
from helpers.apiResponce import success_response, error_response
from prompts.extract import main_extract
from prompts.search import main_search
from prompts.basicForWeb import main
from new.aboutazmth import router_query
from new.knowaboutme import dataquery
from new.elevenlabpy import download_elevenlabs_as_ogg
from fastapi.responses import FileResponse ,JSONResponse
from new.call_backend import ChatbotLogic
from new.get_final import handle_query
from pydantic import BaseModel
from new.summar import summarizer
import json
import asyncio
import subprocess
import os
import uuid
from fastapi.staticfiles import StaticFiles
from typing import Optional, List, Dict

class Query(BaseModel):
    text: str

class QQuery(BaseModel):
    query:str
    summarize_data:str

class Response(BaseModel):
    answer: str
    needs_follow_up: bool = False
    summary: Optional[str] = None
    follow_up_questions: Optional[List[str]] = None

app = FastAPI(title="Cognitive Chatbot API")
chatbot = ChatbotLogic()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://azmth.globaltfn.tech"
    "https://home.globaltfn.tech"
    "*"
]

class UserInput(BaseModel):
    introduction: str

class UserInput(BaseModel):
    message: str

class ChatResponse(BaseModel):
    question: str
    conversation_active: bool
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

output_folder = os.path.join(os.getcwd(), 'output')
app.mount("/output", StaticFiles(directory=output_folder), name="output")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from typing import List

# Store active connections
active_connections = []
user_connections = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()

    active_connections.append(websocket)
    user_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message received from {user_id}: {data}")
            await websocket.send_text(f"Received your message: {data}")

    except WebSocketDisconnect as e:
        print(f"User {user_id} disconnected with code {e.code}.")
        if websocket in active_connections:
            active_connections.remove(websocket)
        user_connections.pop(user_id, None)  # Safe removal

async def notify_clients(message: str):
    """Send a notification to all connected clients."""
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error sending message: {e}")

@app.websocket("/ws/listen")
async def listen_for_user_messages(websocket: WebSocket):
    await websocket.accept()
    user_id = None
    print("A new user is trying to connect.")

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            if 'userId' in data:
                user_id = data['userId']
                user_connections[user_id] = websocket
                print(f"User {user_id} is now connected.")

            if user_id:
                await websocket.send_text(f"Listening for messages from {user_id}")

    except WebSocketDisconnect as e:
        print(f"User {user_id} disconnected with code {e.code}.")
        user_connections.pop(user_id, None)  # Safe removal

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
        unique_id = str(uuid.uuid4())[:8]
        # Start sound processing in the background
        asyncio.create_task(process_sound_async(result,unique_id))

        return success_response(message=unique_id, status_code=200, data=result)
    except Exception as e:
        print(f"Error: {e}")
        return error_response(message="Error", status_code=500)


async def process_sound_async(user_query,unique_id):
    """Handles the sound generation and notifies clients when done."""
    try:
        unique_id = unique_id
        api_key = extract_api_key("config.json")
        result = download_elevenlabs_as_ogg(text=user_query, api_key=api_key, unique_id=unique_id)
        audio_path = f"output/{result}"

        # Run Rhubarb Lip Sync
        rhubarb_output = f"{audio_path}.json"
        cmd = [
            "rhubarb",
            "-o", rhubarb_output,
            audio_path
        ]
        subprocess.run(cmd, check=True)

        # Parse and save the Rhubarb output
        lip_sync_data = parse_rhubarb_output(rhubarb_output, result)
        with open(f"{audio_path}_lipsync.json", "w") as f:
            json.dump(lip_sync_data, f)

        print(f"Sound processing completed for {user_query}")

        # Notify clients when processing is done
        await notify_clients(json.dumps({
            "message": user_query,
            "audio_path": audio_path,
            "lip_sync_path": f"{audio_path}_lipsync.json",
            "id":unique_id
        }))

    except Exception as e:
        print(f"Error processing sound: {e}")


@app.post("/knowaboutme")
async def dataquery(request: dataQuery):
    try:
        result = dataquery(request.userChoice,
                           request.userData, request.userQuery)
        return success_response(message="Responce is Found", status_code=200, data=result)
    except Exception as e:
        print(f"Error: {e}")
        return error_response(message="Error", status_code=500)


def parse_rhubarb_output(output_file,result):
    """
    Convert the Rhubarb output into a structured lip-sync JSON.
    
    Args:
        output_file (str): Path to the Rhubarb output file
    
    Returns:
        dict: Structured lip-sync data with metadata and mouth cues
    """
    lip_sync_data = {
        "metadata": {
            "soundFile": f"{result}",
            "duration": 0.0
        },
        "mouthCues": []
    }
    
    try:
        # Read all lines first to process them together
        with open(output_file, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        
        # Process lines to create more accurate mouth cues
        for i in range(len(lines)):
            # Parse current line
            current_parts = lines[i].split('\t')
            current_time = float(current_parts[0])
            current_phoneme = current_parts[1].strip()
            
            # Determine end time (next phoneme's start time or last time)
            if i < len(lines) - 1:
                next_parts = lines[i+1].split('\t')
                end_time = float(next_parts[0])
            else:
                # If it's the last line, use its time as end time
                end_time = current_time + 0.1  # Small buffer for the last phoneme
            
            # Add mouth cue
            lip_sync_data["mouthCues"].append({
                "start": current_time,
                "end": end_time,
                "value": current_phoneme
            })
        
        # Set duration to the end time of the last phoneme
        lip_sync_data["metadata"]["duration"] = lip_sync_data["mouthCues"][-1]["end"] if lip_sync_data["mouthCues"] else 0.0
    
    except Exception as e:
        print(f"Error parsing Rhubarb output: {e}")
    
    return lip_sync_data

@app.get("/getsound")
def getsound(request):
    if len(request) == 0:
        return error_response(message="No sound or text provided", status_code=404)
    try:
        api_key = extract_api_key("config.json")
        result = download_elevenlabs_as_ogg(request, api_key=api_key)
        audio_path = f"output/{result}"

        # Run Rhubarb Lip Sync
        rhubarb_output = f"{audio_path}.json"
        cmd = [
            "rhubarb",
            "-o", rhubarb_output,
            audio_path
        ]
        subprocess.run(cmd, check=True)

        # Parse the Rhubarb output to generate lip sync data
        lip_sync_data = parse_rhubarb_output(rhubarb_output,result)

        return JSONResponse(content={"audio": audio_path, "lipSync": lip_sync_data})

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"error": "Error processing request"}, status_code=500)


@app.post("/save-api-key")
def save_key(api_key: str):
    try:
        save_api_key(api_key)
        return {"message": "API key saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start_conversation")
async def start_conversation(user_input: UserInput):
    """Initialize a new conversation with user introduction"""
    conversation_id, question, active = chatbot.start_conversation(user_input.message)
    return {
        "conversation_id": conversation_id,
        "question": question,
        "conversation_active": active
    }

@app.post("/continue_conversation/{conversation_id}")
async def continue_conversation(conversation_id: str, user_input: UserInput):
    """Continue existing conversation"""
    question, active = chatbot.continue_conversation(conversation_id, user_input.message)
    return {
        "question": question,
        "conversation_active": active
    }

@app.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Retrieve conversation history"""
    return chatbot.continue_conversation(conversation_id,user_input = "preview")

@app.get("/summarize")
def summarize(filename):
    return summarizer(filename)

@app.post("/query")
async def process_query(request:QQuery):
    """Process a user query and return response"""
    result = handle_query(request.query,request.summarize_data)
    return result

@app.get("/conversation")
async def get_conversation():
    """Retrieve the current conversation log"""
    return assistant.get_conversation_log()

@app.post("/reset")
async def reset_conversation():
    """Reset the conversation log and question count"""
    assistant.conversation_log = []
    assistant.question_count = 0
    return {"status": "conversation reset"}
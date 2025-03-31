
# Backend Code

from fastapi import FastAPI, Request
'''
✅ Imports FastAPI – the main class used to create the web app.
✅ Imports Request – allows you to access the full request data 
                    (e.g., body, headers, etc.)
'''

from fastapi.middleware.cors import CORSMiddleware
'''
✅ Imports CORSMiddleware, which allows Cross-Origin Resource Sharing.
This is essential when your frontend (Streamlit) is running on a different port 
from the backend (FastAPI), to allow communication between them.
'''

import requests
'''
✅ Imports the requests library to make HTTP requests.
We’ll use this to make a POST request to Ollama's API running locally.
'''

app = FastAPI()
'''
✅ Creates an instance of the FastAPI app.
This is your main backend application.
'''

# Allow CORS (so Streamlit frontend can call this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
✅ Adds CORS middleware to the FastAPI app.
allow_origins=["*"]: allow requests from any domain (for development 
                    only; in production, you should limit this).
allow_methods=["*"]: allows all HTTP methods (GET, POST, etc.)
allow_headers=["*"]: allows all headers (like Content-Type, Authorization, etc.)
'''

@app.post("/generate")
#✅ Defines a POST endpoint at /generate.
#This means when the frontend sends a POST request to /generate, 
#                the function below will be triggered.
async def generate(data: Request):
# ✅ Defines an asynchronous function named generate.
# It takes a Request object named data, which will contain the incoming JSON body.
# '''
    body = await data.json()
    '''
    ✅ Extracts the JSON body from the request asynchronously.
    Example body from frontend: {"prompt": "What is AI?"}
    '''
    prompt = body.get("prompt", "")
    '''
    ✅ Retrieves the value of the "prompt" key from the request body.
    If not found, defaults to an empty string.
    '''
    ollama_url = "http://localhost:11434/api/generate"
    '''
    ✅ URL where Ollama is running locally.
    This is the endpoint for model inference using DeepSeek 
    (or any model Ollama is serving).
    '''
    payload = {
        "model": "deepseek-r1",
        "prompt": prompt, 
        "stream": False
    }
    '''
    "model": name of the model you're using (e.g., deepseek-r1)
    "prompt": the user input
    "stream": False: tells Ollama to send the entire response at once 
                instead of in chunks (streaming)
    '''

    try:
        response = requests.post(ollama_url, json=payload)
        '''
        ✅ Sends the prompt to the Ollama backend via a POST request.
        If Ollama is running and the model is loaded, it will return a JSON response.
        '''
        result = response.json()
        '''
        ✅ Converts the response from Ollama into a Python dictionary.
        '''
        return {"response": result.get("response", "No response")}
        '''
        ✅ Returns a dictionary with the model's response to the frontend.
        If Ollama doesn't return a response, it falls back to "No response".
        '''
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
        '''
        ⚠️ If anything goes wrong (like Ollama is not running), 
        this will catch the error and return it as part of the response.
        '''

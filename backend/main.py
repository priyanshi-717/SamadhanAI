from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI
app = FastAPI()

# Allow React to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini (REPLACE WITH YOUR ACTUAL API KEY)
genai.configure(api_key="AIzaSyBVcVSP3WlWdGQBYho4krgwVbEaMT5D4dg")
model = genai.GenerativeModel("gemini-pro") # Or gemini-pro

# Data structure for incoming requests
class ChatRequest(BaseModel):
    message: str
    domain: str # 'agriculture' or 'healthcare'

@app.post("/api/chat")
async def chat_with_gemini(request: ChatRequest):
    # System prompt to guide the AI's persona based on the domain
    system_instruction = f"You are a helpful assistant for rural Indian users. The current domain is {request.domain}. Keep answers simple, actionable, and short. Do not use complex jargon."

    prompt = f"{system_instruction}\nUser: {request.message}"

    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Sorry, I am having trouble connecting right now. Error: {str(e)}"}
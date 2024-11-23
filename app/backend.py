import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Initialize ChatGroq
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-70b-versatile"
)

# Define a data model for the input
class CrimeNarration(BaseModel):
    narration: str

@app.get("/")
async def root():
    return {"message": "Welcome to the LegalNavi AI Model API!"}

@app.post("/process-narration")
async def process_narration(data: CrimeNarration):
    """
    Accept a crime narration and return the AI response.
    """
    if not data.narration.strip():
        raise HTTPException(status_code=400, detail="Narration cannot be empty.")

    crime_prompt = f"""
    You are tasked with summarizing the following crime narration and identifying:
    1. The specific crime.
    2. The relevant Indian Penal Code (IPC) section.
    3. A landmark judgment (if applicable).

    Return the result only in this format:
    Crime: [identified crime]
    IPC Section: [relevant IPC section]
    Landmark Judgment: [related landmark judgment]

    If you cannot identify a crime or IPC section, respond with:
    "Unable to identify a relevant IPC section or landmark judgment."

    Narration: "{data.narration}"
    """

    # Measure latency
    start_time = time.time()
    response = llm.invoke(crime_prompt)
    end_time = time.time()
    latency = end_time - start_time

    if response and response.content:
        return {
            "response": response.content,
            "latency": f"{latency:.4f} seconds"
        }
    else:
        raise HTTPException(status_code=500, detail="No response from the model.")

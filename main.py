from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database setup
DATABASE_URL = "sqlite:///./ai_agent.db"

def get_db():
    conn = sqlite3.connect('ai_agent.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()

# Initialize database
init_db()

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str

class DBQuery(BaseModel):
    query: str
    params: List = []

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        # Save user message to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            ("user", chat_request.message)
        )
        conn.commit()
        
        # Get chat history for context
        cursor.execute(
            "SELECT role, content FROM messages ORDER BY created_at DESC LIMIT 10"
        )
        history = cursor.fetchall()
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        
        # Add history in chronological order
        for row in reversed(history):
            messages.append({"role": row["role"], "content": row["content"]})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        ai_response = response.choices[0].message.content
        
        # Save AI response to database
        cursor.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            ("assistant", ai_response)
        )
        conn.commit()
        
        return {"response": ai_response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/db/query")
async def query_database(db_query: DBQuery):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # For security, only allow SELECT queries
        if not db_query.query.strip().upper().startswith("SELECT"):
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
        
        cursor.execute(db_query.query, tuple(db_query.params))
        results = cursor.fetchall()
        
        # Convert rows to list of dicts
        columns = [column[0] for column in cursor.description]
        result_data = [dict(zip(columns, row)) for row in results]
        
        return result_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

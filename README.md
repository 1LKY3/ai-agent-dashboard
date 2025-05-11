# AI Agent Dashboard

A web-based dashboard that allows interaction with an AI agent and database management.

## Features

- Chat interface to interact with an AI assistant
- Database management capabilities
- Clean, responsive UI
- FastAPI backend with SQLite database
- OpenAI integration for AI responses

## Prerequisites

- Python 3.8+
- Node.js (for frontend development, optional)
- OpenAI API key

## Setup

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Open your browser and navigate to `http://localhost:8000`

## Project Structure

- `main.py` - FastAPI application
- `requirements.txt` - Python dependencies
- `static/` - Static files
- `css/` - CSS stylesheets
- `js/` - JavaScript files
- `ai_agent.db` - SQLite database (created automatically)

## API Endpoints

- `POST /chat` - Send a message to the AI
- `POST /db/query` - Execute a database query (read-only)

## License

MIT

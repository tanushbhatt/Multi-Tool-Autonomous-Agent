# Multi-Tool Autonomous AI Agent

An autonomous AI agent built using Python, LangChain and Google Gemini. It can understand user queries, select appropriate tools, execute actions and generate responses.

## Features

- Autonomous AI agent powered by Google Gemini
- LangChain agent integration
- DuckDuckGo web search
- Python mathematical calculator
- Local file reader
- Automatic tool selection
- Tool execution trace with actions and observations
- Interactive command-line interface
- Input validation and error handling

## Available Tools

### 1. Web Search
Searches the internet using DuckDuckGo and returns relevant results with titles, URLs and descriptions.

### 2. Python Calculator
Performs mathematical calculations using a restricted AST-based expression evaluator.

### 3. Local File Reader
Reads supported local files from the project directory:
- TXT
- Markdown
- CSV
- JSON

External file access is restricted.

## Technologies Used

- Python 3.14
- Google Gemini API
- LangChain
- langchain-google-genai
- DuckDuckGo Search (ddgs)
- python-dotenv
- Python unittest

## Project Structure

    Multi_Tool_Autonomous_Agent/
    |
    |-- main.py
    |-- agent.py
    |-- tools.py
    |-- test_agent.py
    |-- test_tools.py
    |-- sample_document.txt
    |-- requirements.txt
    |-- .env.example
    |-- .gitignore
    |-- README.md

## Installation

### 1. Clone the repository

    git clone YOUR_GITHUB_REPOSITORY_URL

    cd Multi_Tool_Autonomous_Agent

### 2. Create a virtual environment

    python -m venv .venv

### 3. Activate the environment on Windows

    .venv\Scripts\Activate.ps1

### 4. Install dependencies

    python -m pip install -r requirements.txt

### 5. Configure the API key

Create a copy of `.env.example` and rename it to `.env`.

Add your Google Gemini API key:

    GOOGLE_API_KEY=your_gemini_api_key_here

Never upload your actual API key to GitHub.

## Usage

Run the application:

    python main.py

Enter your questions in the terminal.

The agent can select the appropriate tool based on your request.

Type `exit` or `quit` to stop the application.

## Example Queries

### Web Search

    Search for the latest developments in Python.

### Calculator

    Calculate 250 * 40 + 100.

### Local File Reader

    Read sample_document.txt and summarize its contents.

## Execution Trace

The application displays:
- Tool calls
- Tool inputs
- Tool observations
- Final AI-generated responses

## Run Automated Tests

Run all tests:

    python -m unittest discover -v

Run tool tests:

    python -m unittest test_tools.py -v

Run agent tests:

    python -m unittest test_agent.py -v

## Security

- API credentials are stored in `.env`.
- `.env` is excluded using `.gitignore`.
- The calculator restricts executable operations.
- The file reader prevents access outside the project directory.
- Retrieved web pages and file contents are treated as untrusted data.

## Author

Tanush Bhatt
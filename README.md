AdaptiveMind AI

A professional AI-powered personal assistant built with Python, Streamlit, Groq API, and SQLite. AdaptiveMind AI combines conversational intelligence with long-term memory, allowing users to save personal information and retrieve relevant memories during conversations.

Live Demo

"Launch AdaptiveMind AI" (https://adaptivemind-agent-m4qnoychncs5enh7y3wceg.streamlit.app/)

GitHub Repository

"View the AdaptiveMind AI source code" (https://github.com/MADEEHA991/AdaptiveMind-Agent)

---

Overview

AdaptiveMind AI is a full-stack AI assistant application designed to demonstrate how modern AI applications can combine:

- Large Language Models
- API-based AI inference
- Long-term memory
- Semantic-style memory retrieval
- SQLite data persistence
- Streamlit web interfaces
- Secure API-key management
- Cloud deployment

The application allows users to interact with an AI assistant while maintaining a persistent collection of user-defined memories.

---

Key Features

AI-Powered Conversations

AdaptiveMind AI uses the Groq API to generate natural-language responses.

The assistant can:

- Answer questions
- Explain technical concepts
- Provide detailed responses
- Handle general conversations
- Use relevant stored memories when answering

Long-Term Memory

Users can save information for AdaptiveMind AI to remember.

Example:

My favourite programming language is Python.

Later, the user can ask:

What is my favourite programming language?

AdaptiveMind AI retrieves the relevant memory and uses it when generating the response.

Memory Management

The application provides a complete memory-management interface.

Users can:

- Save memories
- View stored memories
- Delete individual memories
- Clear all stored memories

Intelligent Memory Retrieval

When a user asks a question, AdaptiveMind AI searches the stored memories for relevant information.

The system uses keyword-based matching to identify memories related to the current query.

If no direct match is found, recent memories can be provided as fallback context.

Secure API Key Management

The Groq API key is not stored in the GitHub repository.

For local development, the key is stored in:

.env

For Streamlit Cloud deployment, the key is configured using Streamlit Secrets.

The ".gitignore" file prevents sensitive environment files from being committed.

---

Technology Stack

Technology| Purpose
Python| Core programming language
Streamlit| Web application frontend
Groq API| AI/LLM inference
SQLite| Long-term memory storage
python-dotenv| Environment variable management
Git| Version control
GitHub| Source code hosting
Streamlit Community Cloud| Application deployment

---

System Architecture

                    User
                     |
                     v
             Streamlit Frontend
                     |
                     v
             AdaptiveMind Agent
                /          \
               /            \
              v              v
        Memory System      Groq API
              |                |
              v                v
           SQLite          AI Response
              |
              v
       Relevant Memories
              |
              +--------> Agent Context
                              |
                              v
                         Final Response

---

Project Structure

AdaptiveMind-Agent/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   └── logo.png
│
├── backend/
│   ├── __init__.py
│   ├── agent.py
│   ├── groq_client.py
│   └── memory.py
│
└── data/
    └── adaptive_memory.db

"app.py"

The main Streamlit application.

Responsible for:

- User interface
- Chat interface
- Memory management interface
- Session state
- Connecting the frontend to the AdaptiveMind agent

"backend/agent.py"

The main AI-agent layer.

Responsible for:

- Coordinating Groq and memory
- Saving memories
- Searching memories
- Deleting memories
- Building memory context
- Generating AI responses

"backend/groq_client.py"

Handles communication with the Groq API.

Responsible for:

- Loading the API key
- Initializing the Groq client
- Selecting the AI model
- Sending chat requests
- Returning generated responses

"backend/memory.py"

Implements the SQLite-based memory system.

Responsible for:

- Creating the database
- Creating the memories table
- Saving memories
- Retrieving memories
- Searching memories
- Deleting memories
- Clearing stored memories

"requirements.txt"

Contains the Python dependencies required to run the application.

---

Installation

1. Clone the repository

git clone https://github.com/MADEEHA991/AdaptiveMind-Agent.git

2. Open the project directory

cd AdaptiveMind-Agent

3. Create a virtual environment

python -m venv .venv

4. Activate the virtual environment

On Windows PowerShell:

.venv\Scripts\Activate.ps1

5. Install dependencies

pip install -r requirements.txt

---

Environment Configuration

Create a ".env" file in the project root:

GROQ_API_KEY=your_groq_api_key

Replace "your_groq_api_key" with your actual Groq API key.

Never commit the ".env" file to GitHub.

---

Running Locally

After installing the dependencies and configuring the API key, run:

streamlit run app.py

The application will open in your browser.

The default local address is:

http://localhost:8501

---

Using AdaptiveMind AI

Save a Memory

Enter information in the Memory section.

Example:

My favourite programming language is Python.

Click:

Save Memory

The memory will appear under Stored Memories.

Chat With the Assistant

Enter a question in:

Ask AdaptiveMind anything...

Example:

Explain machine learning in simple terms.

AdaptiveMind AI sends the conversation to the Groq API and displays the generated response.

Test Memory

After saving:

My favourite programming language is Python.

Ask:

What is my favourite programming language?

The assistant should use the stored memory to answer:

Python.

---

Memory Workflow

The memory-aware response pipeline works as follows:

User Question
      |
      v
Search Stored Memories
      |
      v
Find Relevant Memories
      |
      v
Build Memory Context
      |
      v
Create System Prompt
      |
      v
Send Context + User Question
      |
      v
Groq API
      |
      v
AI Generated Response

---

Security

Sensitive credentials are intentionally excluded from the repository.

The project uses ".gitignore" to prevent files such as:

.env
.env.*
.venv/
data/
__pycache__/
*.db
*.sqlite
*.sqlite3

from being uploaded to GitHub.

For cloud deployment, the Groq API key is configured through Streamlit Secrets rather than being stored in the source code.

---

Deployment

AdaptiveMind AI is deployed using Streamlit Community Cloud.

Live application:

"Launch AdaptiveMind AI" (https://adaptivemind-agent-m4qnoychncs5enh7y3wceg.streamlit.app/)

The deployment uses:

GitHub Repository
       |
       v
Streamlit Community Cloud
       |
       v
app.py
       |
       v
AdaptiveMind AI

---

Testing

The project has been tested locally for:

- Python compilation
- Backend initialization
- Groq API connectivity
- Memory creation
- Memory retrieval
- Memory search
- Individual memory deletion
- AI response generation
- Streamlit application startup
- Browser-based chat
- Long-term memory interaction
- Cloud deployment

Example backend verification:

AdaptiveMind backend OK
Stored memories: 0

The Groq-powered response pipeline was also tested successfully with stored memory.

---

Future Improvements

Planned improvements for AdaptiveMind AI include:

- Automatic memory extraction from conversations
- More advanced semantic memory retrieval
- Conversation history persistence
- User profiles
- Memory categories
- Memory importance scoring
- Improved memory ranking
- Streaming AI responses
- Enhanced UI/UX
- Authentication
- Production database support
- Advanced agent tools
- Document and file-based memory
- Analytics dashboard
- Multi-model support

---

Learning Objectives

This project demonstrates practical experience with:

- Python application development
- AI application architecture
- Large Language Model integration
- REST API-based AI services
- Prompt engineering
- Long-term memory systems
- SQLite databases
- Streamlit development
- Environment-variable security
- Git and GitHub
- Cloud deployment
- Full-stack AI application development

---

Project Status

Status: Deployed and operational

The current version provides:

- Groq-powered AI conversations
- SQLite long-term memory
- Memory search
- Memory deletion
- Clear-all memory functionality
- Streamlit frontend
- Secure API-key configuration
- Public cloud deployment

---

Author

Madeeha Kousar

Artificial Intelligence and Data Science Student

GitHub: "MADEEHA991" (https://github.com/MADEEHA991)

---

License

This project is intended for educational, portfolio, and demonstration purposes.
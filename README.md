# AdaptiveMind AI

AdaptiveMind AI is a personal AI assistant built with Python, Streamlit, Groq API, and SQLite.

The project combines conversational AI with long-term memory, allowing the assistant to store user-provided information and retrieve relevant memories when answering future questions.

## Features

- AI-powered conversational assistant
- Groq API integration
- Long-term memory using SQLite
- Save personal memories
- Retrieve relevant memories
- View stored memories
- Delete individual memories
- Clear all memories
- Memory-aware AI responses
- Streamlit web interface
- Secure API key management using environment variables
- Modular backend architecture

## Project Architecture

```text
AdaptiveMind-Agent
│
├── app.py
│
├── backend
│   ├── __init__.py
│   ├── agent.py
│   ├── groq_client.py
│   └── memory.py
│
├── assets
│   └── logo.png
│
├── data
│   └── adaptive_memory.db
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
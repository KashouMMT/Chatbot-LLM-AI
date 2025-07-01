# 🧠 Simple Chatbot by KashouMMT

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

A simple yet extensible command-line chatbot AI built with Python. This chatbot uses a base system prompt and Retrieval-Augmented Generation (RAG) for enhanced context-aware responses.

---

## 📁 Project Structure

```
CHATBOT_PROJECT/
├── chatbot
│   ├── rag/                # Main RAG folder
│   │   └── __init__.py     # 
│   │   ├── db_builder.py   # Main RAG database builder
│   │   ├── embedder.py     # Embedder for database
│   │   ├── loader.py       # Loads documents for database 
│   │   └── retriever.py     # Search and compare relavent data from database
│   ├── __init__.py         #
│   ├── core.py             # Initialize main loop to start AI
│   ├── memory.py           # Memory Manager for AI
│   ├── tools.py            # External commands handler
│   └── utils.py            # Utility functions
├── database/               # RAG database folder
├── datasource/             # Files and documents used for RAG (Support .md,.txt,.xlsx,.csv)
├── logs/                   # Optional log files
├── prompts/
│   └── system_prompt.txt   # System prompt that defines AI behavior
├── .env                    # Environment variables
├── main.py                 # Entry point of the chatbot
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1. Install Dependencies

Make sure you have Python 3.8+ installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create a `.env` file in the project root:

```env
API_KEY = "<YOUR-API-KEY-HERE>"
BASE_URL = "<YOUR-BASE-URL>"
MODEL = "<YOUR-MODEL>"
```

### 3. Run the Chatbot

```bash
python main.py              # Run normally
python main.py --debug      # Enable debug logging
python main.py --debug-info # Show info-level logs
```

---

## ✨ Features

- ✅ Command-line interface (CLI)
- ✅ Customizable system prompt
- ✅ Support for RAG using markdown knowledge files
- ✅ Logging (info and debug levels)
- ✅ Modular codebase (easy to expand)

---

## 🧩 How to Add Knowledge Sources (RAG)

The chatbot uses Retrieval-Augmented Generation (RAG) to enhance its responses with relevant data from files in the `datasource/` folder. Currently support `.md,.txt,.xlsx,.csv`.

### To add new knowledge:

1. Create or place a new file or multiple files with the content you'd like the AI to reference.
2. Place the file inside the `datasource/` directory.
3. The chatbot will automatically index and reference the content during runtime.

> Tip: Keep each file focused on a single topic to improve retrieval accuracy.

---

## 🛠️ Customizing AI Behavior

You can define how the chatbot thinks and responds by editing:

```
prompts/system_prompt.txt
```

Use it to shape the assistant's tone, role, goals, or restrictions.

Example content:
```
You are a friendly assistant that helps users explore cannabis products based on their needs and preferences...
```

---

## 💡 Tips

- Use clear and structured markdown inside `datasource/` for better parsing.
- Do not include title, header or unnecessary data in Excel files so that relavant data can be read.
- Restart the chatbot after updating data files or prompts.
- Consider chunking large `.md` files into smaller ones for better RAG relevance.
- Use logging flags during development to debug and inspect flow.

---

## 🧪 Future Ideas

- [ ] Add a web interface (Flask, FastAPI, or React)
- [ ] Improved multi-file support
- [ ] Memory or session context handling
- [ ] Voice input/output integration
- [ ] Model switching support (OpenAI, local, etc.)

---

## 🧾 License

Released under the [MIT License](https://opensource.org/licenses/MIT).  
You are free to use, modify, and share this project.  
While contributions are welcome, this is a personal project with no guaranteed support.


---

Happy Chatting! 🤖✨

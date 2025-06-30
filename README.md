# Simple Chatbot By KashouMMT

This is a simple chatbot AI in python that use command line to response.

---

## How to run this AI?

1. Please Refer to the requirements.txt for necessary installiation. 
2. Create .env file in project root folder with the following attributes.
```
API_KEY = "<YOUR-API-KEY-HERE>"
BASE_URL = "<YOUR-BASE-URL>"
MODEL = "<YOUR-MODEL>"
```
3. Run the following commands to start the chatbot AI.
```python
python main.py
python main.py --debug-info # For info log on console.
python main.py --debug      # For debug log on console.
```

## How to modify AI behaviour 

1. Modify prompts/system_prompt.txt to however you like.
2. Add datasources in .md file to datasource folder for the AI to reference it for RAG.
import os

file_path = r"D:\Work_Folder\\Chatbot_API_Key.txt"

if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file for Chatbot API Key at {file_path} is not found.")
else:
    with open(file_path,'r',encoding="utf-8") as file:
        api_key = file.read()    

API_KEY = api_key
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat:free"

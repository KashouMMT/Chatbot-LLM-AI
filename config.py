from dotenv import load_dotenv, dotenv_values
from chatbot.utils import print_colored

import os
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

env_file = ".env"

if not os.path.isfile(env_file):
    error_msg = f"Error: '{env_file}' file doesn't exist. Please create it with correct attributes."
    print_colored("Error:", error_msg, "red")
    logger.error(error_msg)
    sys.exit(1) # Exit immediately if the file isn't found

env_vars = dotenv_values(env_file)

required_env_vars = ["API_KEY", "BASE_URL", "MODEL"]

missing_vars = []
empty_vars = []

if not env_vars:
    error_msg = f"Error: '{env_file}' exists but appears to be empty or contains no valid key-value pairs."
    print_colored("Error:", error_msg, "red")
    logger.error(error_msg)
    sys.exit(1)

for var in required_env_vars:
    if var not in env_vars:
        missing_vars.append(var)
    elif not env_vars[var]: # Checks for empty string values
        empty_vars.append(var)

if missing_vars:
    error_msg = f"Error: Missing required environment variables in '{env_file}': {', '.join(missing_vars)}."
    print_colored("Error:", error_msg, "red")
    logger.error(error_msg)
    sys.exit(1)

if empty_vars:
    error_msg = f"Error: Required environment variables are empty in '{env_file}': {', '.join(empty_vars)}. Please provide values."
    print_colored("Error:", error_msg, "red")
    logger.error(error_msg)
    sys.exit(1)

load_dotenv(env_file)

try:
    API_KEY = os.environ["API_KEY"]       # API key for chatbot
    BASE_URL = os.environ["BASE_URL"]     # Base url for chatbot api
    MODEL = os.environ["MODEL"]           # Model for chatbot api 
    COLORS = {                            
        "red": "\033[91m",                
        "green": "\033[92m",              
        "cyan": "\033[96m",               
        "default": "\033[0m"              
    }                                     # Color definition for console print
    CHROMA_PATH = "database/"             # File path location for RAG database
    MAX_TOKEN = 12000                     # Max tokens for chat history logs
    DATA_PATH = "datasource/"             # Datasource folder location for database
    # Supported file extensions for database
    SUPPORTED_EXTENSIONS = [".md",".txt",".csv",".xlsx"]
    #Prompt template for user query
    PROMPT_TEMPLATE = """
Answer the question based only on the following context. Provide by database:

{context}

---

Answer the question based on the above context and chat history: {question}
"""
except KeyError as e:
    error_msg = f"Configuration error: Missing expected environment variable after loading: {e}. This indicates a bug in .env validation."
    print_colored("Critical Error:", error_msg, "red")
    logger.critical(error_msg)
    sys.exit(1)

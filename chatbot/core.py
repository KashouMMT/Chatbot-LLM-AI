from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate

from chatbot.memory import MemoryManager
from chatbot.tools import handle_command
from chatbot.utils import load_system_prompt,print_colored,log_function_call,format_prompt

from .rag.db_builder import Database
from .rag.retriver import search

from config import API_KEY,BASE_URL,MODEL

import traceback
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = load_system_prompt() # Load system prompt
MAX_TOKEN = 12000 # Max tokens for chat history logs
CHROMA_PATH = "database/" # File path location for RAG database

@log_function_call
def run_chatbot():
    
    llm = ChatOpenAI(api_key=API_KEY,base_url= BASE_URL,model = MODEL) # LLM
    memory = MemoryManager(llm=llm,max_tokens=MAX_TOKEN) # Initialize Memory
    memory.add_system_message(SYSTEM_PROMPT) # Load system prompt to memory
    db = Database(CHROMA_PATH) # Create Database
    db.generate_data_store()
    print("Chatbot is ready! Type '/exit' to quit. '/help' for command list.")
    logger.info("Chatbot started.")
    while True:
        user_input = input("You: ") # User input
        logger.info("User input: {user_input}")
        result = handle_command(user_input,memory) # Handle command
        if result == False: break
        elif result == True: continue
        try:
            logger.info("Begin search in database for user query.")
            results = search(user_input,db)
            logger.info(f"Search result: {results}")
            
            if isinstance(results,str):
                context_text = "\n\n---\n\n".join(results)
            else:
                context_text = "\n\n---\n\n".join([f"{doc.page_content}" for doc in results])
            chat_history = memory.get_messages() # Extract memory history
            prompt = format_prompt(context_text,user_input) # Format the user query prompt
            logger.info(f"Prompt for user query: {prompt}") # Log the Prompt
            chat_history.append(HumanMessage(content=prompt)) # Append current input to history
            response = llm.invoke(chat_history) # Get LLM Response
            reply = response.content.strip()
            print_colored("Bot: ",reply,"green")
            logger.info(f"AI reply: {reply}") # Log the Reply
            memory.save_context({"input": prompt},{"output": reply})  # Save interaction into memory
        except Exception as e:
            print_colored("Error:", str(e), "red")
            logger.error(f"Error: {str(e)}")
            traceback.print_exc()
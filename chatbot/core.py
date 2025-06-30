from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate

from chatbot.memory import MemoryManager
from chatbot.tools import handle_command
from chatbot.utils import load_system_prompt,print_colored,log_function_call

from .rag.db_builder import Database
from .rag.retriver import search

from config import API_KEY,BASE_URL,MODEL

import traceback

SYSTEM_PROMPT = load_system_prompt() # Load system prompt
MAX_TOKEN = 12000 # Max tokens for chat history logs

CHROMA_PATH = "database/" # File path location for RAG database

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
def run_chatbot():
    print("Chatbot is ready! Type '/exit' to quit. '/help' for command list.")
    
    llm = ChatOpenAI(api_key=API_KEY,base_url= BASE_URL,model = MODEL) # LLM
    memory = MemoryManager(llm=llm,max_tokens=MAX_TOKEN) # Initialize Memory
    memory.add_system_message(SYSTEM_PROMPT) # Load system prompt to memory
    db = Database(CHROMA_PATH) # Create Database
    db.generate_data_store()
    
    while True:
        user_input = input("You: ") # User input
        result = handle_command(user_input,memory) # Handle command
        if result == False: break
        elif result == True: continue
        try:
            results = search(user_input,db)
            if not results:
                context_text = "\n\n---\n\n".join([doc.page_content for doc,_score in results])
                prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
                prompt = prompt_template.format(context=context_text,question=user_input)
                user_input = prompt
            chat_history = memory.get_messages() # Extract memory history
            chat_history.append(HumanMessage(content=user_input)) # Append current input to history
            response = llm.invoke(chat_history) # Get LLM Response
            reply = response.content.strip()
            print_colored("Bot: ",reply,"green")
            memory.save_context({"input": user_input},{"output": reply})  # Save interaction into memory
        except Exception as e:
            print_colored("Error:", str(e), "red")
            
            traceback.print_exc()
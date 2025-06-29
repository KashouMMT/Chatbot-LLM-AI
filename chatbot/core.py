from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,SystemMessage

from chatbot.memory import MemoryManager
from chatbot.tools import handle_command
from chatbot.utils import load_system_prompt,print_colored
from config import API_KEY,BASE_URL,MODEL

import traceback

SYSTEM_PROMPT = load_system_prompt() # Load system prompt
MAX_TOKEN = 12000 # Max tokens for chat history logs

def run_chatbot():
    print("Chatbot is ready! Type '/exit' to quit. '/help' for command list.")
    
    llm = ChatOpenAI(api_key=API_KEY,base_url= BASE_URL,model = MODEL) # LLM
    memory = MemoryManager(llm=llm,max_tokens=MAX_TOKEN) # Memory
    memory.add_system_message(SYSTEM_PROMPT) # Load system prompt to memory
    
    while True:
        user_input = input("You: ")
        result = handle_command(user_input,memory)
        if result == False: break
        elif result == True: continue
        try:
            chat_history = memory.get_messages() # Extract memory history
            chat_history.append(HumanMessage(content=user_input)) # Append current input to history
            response = llm.invoke(chat_history) # Get LLM Response
            reply = response.content.strip()
            
            print_colored("Bot: ",reply,"green")
            
            memory.save_context({"input": user_input},{"output": reply})  # Save interaction into memory
            
        except Exception as e:
            print_colored("Error:", str(e), "red")
            
            traceback.print_exc()
                
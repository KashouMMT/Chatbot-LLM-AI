from openai import OpenAI
from chatbot.memory import MemoryManager
from chatbot.tools import handle_command
from chatbot.utils import load_system_prompt,print_colored
from config import API_KEY,BASE_URL,MODEL

import traceback

class ChatBot:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY,base_url=BASE_URL)
        self.memory = MemoryManager()
        self.system_prompt = load_system_prompt()
    
    def run(self):
        print("Chatbot is ready! Type '/exit' to quit. '/help' for command list.")
        self.memory.add_message(self.system_prompt)
        
        while True:
            user_input = input("You: ")
            result = handle_command(user_input,self.memory)
            if result == False:
                break
            elif result == True:
                continue
            else:
                self.memory.add_message({"role": "user", "content": user_input})
                try:
                    response = self.client.chat.completions.create(
                        model=MODEL,
                        messages=self.memory.get_context(),
                        stream=False
                    )
                    reply = response.choices[0].message.content.strip()
                    print_colored("Bot: ",reply,"green")
                    self.memory.add_message({"role": "assistant", "content": reply})
                except Exception as e:
                    print_colored("Error: ",str(e),"red")
                    traceback.print_exc()
                
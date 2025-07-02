from chatbot.utils import print_colored,load_system_prompt,log_function_call
from chatbot.memory import MemoryManager

@log_function_call
def handle_command(command: str,memory: MemoryManager):
    if not command.startswith("/"):
        return None
    
    if command == "/help":
        print_colored("System: ",
"""
Avilabe commands - 
  /help - Show this help message
  /restart - Restart the bot
  /exit - Stop the bot
""",
        "cyan")
    elif command == "/restart":
        memory.clear()
        memory.add_system_message(load_system_prompt()) # Load system prompt to memory
        print_colored("System: ","Chat history cleared.","cyan")
    elif command == "/exit":
        print_colored("System: ","The bot is stopped.","cyan")
        return False
    else:
        return f"Unknown command: {command}"
    
    return True
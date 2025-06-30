from chatbot.utils import print_colored,load_system_prompt

SYSTEM_PROMPT = load_system_prompt()

def handle_command(command,memory):
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
        memory.add_system_message(SYSTEM_PROMPT) # Load system prompt to memory
        print_colored("System: ","Chat history cleared.","cyan")
    elif command == "/exit":
        print_colored("System: ","The bot is stopped.","cyan")
        return False
    else:
        return f"Unknown command: {command}"
    
    return True
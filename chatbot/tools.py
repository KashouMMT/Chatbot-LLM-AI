from chatbot.utils import print_colored

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
        print_colored("System: ","Chat history cleared. (not implemented in memory yet.)","cyan")
    elif command == "/exit":
        print_colored("System: ","The bot is stopped.","cyan")
        return False
    else:
        return f"Unknown command: {command}"
    
    return True
    
    
# if user_input.lower() == "exit":
#                 break
#             if user_input.startswith("/"):
#                 response = handle_command(user_input)
#                 print_colored("Bot (command):",response,"cyan")
#                 continue
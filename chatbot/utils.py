# chatbot/utils.py

def print_colored(label, text, color="default"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "cyan": "\033[96m",
        "default": "\033[0m"
    }
    print(f"{colors.get(color,'')}{label} {text}\033[0m")
    
def load_system_prompt(path="prompts/system_prompt.txt"):
    try:
        with open(path,"r",encoding="utf-8") as f:
            data = f.read()

        return {
            "role": "system",
            "content": data
        }
    except FileNotFoundError:
        print("[Warning] system_prompt.json not found, using default prompt.")
        return {
            "role": "system",
            "content": "You are a helpful assistant."
        }
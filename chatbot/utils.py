from functools import wraps

import logging
import inspect

# Get a logging instance for your module or a specific category
logger = logging.getLogger(__name__)

def log_function_call(func):
    """
    A decorator that logs the entry and exit of a function,
    including its arguments and return value.
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        # Log function entry
        func_name = func.__name__
        arg_names = inspect.getfullargspec(func).args
        
        # Combined positional and keyword arguments with their names
        call_args = {}
        for i, arg in enumerate(args):
            if i < len(arg_names):
                call_args[arg_names[i]] = arg
            else:
                call_args[f"arg_{i}"] = arg # For excess positonal args 
         
        call_args.update(kwargs) # Add keyword arguments
        
        logger.debug(f"Entering function '{func_name}' with args: {call_args}")
        
        try:
            result = func(*args, **kwargs)
            # Log function exit and return value
            logger.debug(f"Exiting function '{func_name}' - Returned: {result}")
            return result
        except Exception as e:
            # Log any exceptions
            logger.error(f"Function '{func_name}' raised an exception: {e}", exc_info=True)
            raise # Re-raise the exception to not alter normal program flow
    
    return wrapper

@log_function_call
def load_system_prompt(path="prompts/system_prompt.txt"):
    try:
        with open(path,"r",encoding="utf-8") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        print("[Warning] system_prompt.json not found, using default prompt.")
        return "You are a helpful assistant."

colors = {
    "red": "\033[91m",
    "green": "\033[92m",
    "cyan": "\033[96m",
    "default": "\033[0m"
}

def print_colored(label, text, color="default"):
    print(f"{colors.get(color,'')}{label} {text}\033[0m")
    
def print_colored_format(label, text, color="default"):
    return f"{colors.get(color,'')}{label} {text}\033[0m"
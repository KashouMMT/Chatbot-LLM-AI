from chatbot import *

import argparse
import logging
import os
import io
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "logs/function_calls.log")

def setup_logging(console_level=None):
    
    # To make sure log directory exist
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    # FileHandler (UTF-8 safe by default)
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Base file + console logger setup
    handlers = [file_handler]
    
    if console_level is not None:
        utf8_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
        console_handler = logging.StreamHandler(utf8_stdout)
        console_handler.setLevel(console_level)
        console_handler.setFormatter(logging.Formatter(
            print_colored_format("Debug: ", "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "cyan")
        ))
        handlers.append(console_handler)

    logging.basicConfig(
        level=logging.DEBUG,  # File always gets DEBUG
        format=print_colored_format("Debug: ","%(asctime)s - %(name)s - %(levelname)s - %(message)s","cyan"),
        handlers=handlers
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="Enable debug logging on console")
    parser.add_argument("--debug-info",action="store_true",help="Enable INFO logging on console")
    args = parser.parse_args()
    
    if args.debug:
        console_level = logging.DEBUG
    elif args.debug_info:
        console_level = logging.INFO
    else:
        console_level = None
    
    setup_logging(console_level)
    run_chatbot()
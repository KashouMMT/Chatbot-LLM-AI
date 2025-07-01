from langchain_core.memory import BaseMemory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import PrivateAttr
from typing import List,Dict

from chatbot.utils import log_function_call,print_colored

import logging

logger = logging.getLogger(__name__)
class MemoryManager(): 
    
    def __init__(self,llm: BaseChatModel, max_tokens=6000):
        self._llm = llm
        self._max_tokens = max_tokens
        self._history = []
    
    @log_function_call
    def get_messages(self) -> List:
        self._summarize_and_prune_history()
        return self._history
    
    @log_function_call
    def save_context(self, inputs: Dict[str, str], outputs: Dict[str, str]) -> None:
        user_input = inputs.get("input", "")
        if user_input:
            self._history.append(HumanMessage(content=user_input))
        output = outputs.get("output", "")
        if output:
            self._history.append(AIMessage(content=output))
    
    @log_function_call 
    def clear(self):
        self._history.clear()
    
    @log_function_call
    def add_system_message(self, content: str):
        self._history.append(SystemMessage(content=content))
    
    @log_function_call
    def add_human_message(self, content: str):
        self._history.append(HumanMessage(content=content))
    
    @log_function_call
    def add_ai_message(self, content: str):
        self._history.append(AIMessage(content=content))
    
    @log_function_call
    def _summarize_and_prune_history(self):
        logger.info(f"Summarization started.")
        
        tokens = count_tokens_approximately(self._history)
        
        logger.debug(f"Total token counts: {tokens}")
        if tokens <= self._max_tokens:
            logger.info(f"Token count not exceeded. Summarization skipped.")
            return
        
        # Oldest half of message history
        midpoint = len(self._history) // 2
        to_summarize = self._history[:midpoint]
        
        if not to_summarize:
            logger.warning(f"Summarization failed due to empty summary message. Summarization skipped.")
            return
        
        if len(to_summarize) < 4:
            logger.info("Too few messages to summarize meaningfully. Skipping summarization.")
            return
        
        # Summarize with LLM
        summary_prompt = [
            SystemMessage(content="Summarize the following chat history for context creation."),
            *to_summarize
        ]
        try:
            summary_result = self._llm.invoke(summary_prompt)
            if not summary_result or not summary_result.content.strip():
                logger.warning("Empty summary returned by LLM. Pruning without summary.")
                self._history = self._history[midpoint:]
                return
            summary_message = SystemMessage(content="Summary of earlier conversation: " + summary_result.content)
            logger.info(f"Summary Message: {summary_message}")       
            self._history = [summary_message] + self._history[midpoint:] # Replace old messages with summary
            if count_tokens_approximately(self._history) > self._max_tokens:
                logger.warning("Token count still exceeds limit after summarization. Pruning additional messages.")
                self._history = self._history[len(self._history) // 2:]
        except Exception as e:
            print_colored("Error:", str(e), "red")   
            logger.error(f"Error: Summarization failed. {str(e)}")  
            self._history = self._history[midpoint:] # Fallback: just prune without summary
        
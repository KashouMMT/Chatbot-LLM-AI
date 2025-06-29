from langchain_core.memory import BaseMemory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import PrivateAttr
from typing import List,Dict
class MemoryManager(BaseMemory):
    _history: List = PrivateAttr(default_factory=list)
    _llm: BaseChatModel = PrivateAttr()
    _max_tokens: int = PrivateAttr()    
    
    def __init__(self,llm: BaseChatModel, max_tokens=6000):
        super().__init__()
        self._llm = llm
        self._max_tokens = max_tokens
        
    @property
    def memory_variables(self) -> List[str]:
        return ["messages"]
    
    def load_memory_variables(self, inputs: Dict) -> Dict:
        self._summarize_and_prune_history()
        return {"messages": self._history}
    
    def save_context(self, inputs, outputs):
        self._history.append(HumanMessage(content=inputs["input"]))
        self._history.append(AIMessage(content=outputs["output"]))
        
    def clear(self):
        self._history.clear()
    
    def get_messages(self) -> List:
        return self._history
    
    def add_system_message(self, content: str):
        self._history.append(SystemMessage(content=content))
    
    def _summarize_and_prune_history(self):
        tokens = count_tokens_approximately(self._history)
        if tokens <= self._max_tokens:
            return
        
        # Oldest half of message history
        midpoint = len(self._history) // 2
        to_summarize = self._history[:midpoint]
        
        if not to_summarize:
            return
        
        # Summarize with LLM
        summary_prompt = [
            SystemMessage(content="Summarize the following chat history for context creation."),
            *to_summarize
        ]
        
        try:
            summary_result = self._llm.invoke(summary_prompt)
            summary_message = SystemMessage(content="Summary of earlier conversation: " + summary_result.content)
            
            # Replace old messages with summary
            self._history = [summary_message] + self._history[midpoint:]
            
        except Exception as e:
            print(f"[Summarization failed]: {e}")
            # Fallback: just prune without summary
            self._history = self._history[midpoint:]
        
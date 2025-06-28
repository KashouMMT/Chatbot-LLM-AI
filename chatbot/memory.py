class MemoryManager:
    def __init__(self, max_messages=20):
        self.messages = []
        self.max_messages = max_messages
    
    def add_message(self,message):
        self.messages.append(message)
        # Trim history if too long (keeps the last N messages)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
            
    def get_context(self):
        return self.messages.copy()
    
    def clear(self):
        self.messages = []
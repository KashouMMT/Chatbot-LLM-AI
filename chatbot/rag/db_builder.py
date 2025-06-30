from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from chatbot.utils import print_colored,log_function_call

from .formatter import load_documents, split_text
from .embedder import Embedder

import os
import shutil
class Database():
    def __init__(self,chroma_path):
        self.embedding_function = Embedder("all-MiniLM-L6-v2")
        self.chroma_path = chroma_path
        self.chroma = None
    
    @log_function_call
    def generate_data_store(self):
        documents = load_documents()
        chunks = split_text(documents)
        self.save_to_chroma(chunks)
    
    @log_function_call
    def save_to_chroma(self,chunks: list[Document]):
        # Clear out the database
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
            
        self.chroma = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_function,
            persist_directory=self.chroma_path
        )
        print_colored("System:",f"Saved {len(chunks)} chunks to {self.chroma_path}.")

    @log_function_call
    def load_chroma(self):
        self.chroma = Chroma(
            persist_directory=self.chroma_path,
            embedding_function=self.embedding_function
        )

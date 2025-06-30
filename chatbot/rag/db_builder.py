from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from chatbot.utils import print_colored

from .formatter import load_documents, split_text
from .embedder import Embedder

import os
import shutil
class Database():
    def __init__(self,chroma_path):
        self.embedding_function = Embedder("all-MiniLM-L6-v2")
        self.chroma_path = chroma_path
        
    def generate_data_store(self):
        documents = load_documents()
        chunks = split_text(documents)
        self.save_to_chroma(chunks)
    
    def save_to_chroma(self,chunks: list[Document]):
        # Clear out the database
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
            
        db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_function,
            persist_directory=self.chroma_path
        )
        db.persist()
        print_colored("System:",f"Saved {len(chunks)} chunks to {self.chroma_path}.")


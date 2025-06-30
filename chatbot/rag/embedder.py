from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

class Embedder(Embeddings):
    def __init__(self,model_name):
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()
    
    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text,show_progress_bar=False).tolist()
    
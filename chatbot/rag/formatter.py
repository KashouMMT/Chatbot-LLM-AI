from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from chatbot.utils import print_colored

DATA_PATH = "datasource/"
    
def load_documents():
    loader = DirectoryLoader(DATA_PATH,glob="*.md")
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100,
        length_function = len,
        add_start_index = True,
    )
    chunks = text_splitter.split_documents(documents)
    print_colored("System:",f"Split {len(documents)} documents into {len(chunks)} chunks.","cyan")
    documents = chunks[10]
    print_colored("System:",documents.page_content,"cyan")
    print_colored("System:",documents.metadata,"cyan")
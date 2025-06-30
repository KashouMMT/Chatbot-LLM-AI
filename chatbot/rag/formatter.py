from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from chatbot.utils import print_colored,log_function_call

DATA_PATH = "datasource/"

@log_function_call
def load_documents():
    loader = DirectoryLoader(DATA_PATH,glob="*.md")
    documents = loader.load()
    return documents

@log_function_call
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100,
        length_function = len,
        add_start_index = True,
    )
    chunks = text_splitter.split_documents(documents)
    print_colored("System:",f"Split {len(documents)} documents into {len(chunks)} chunks.","cyan")
    preview_docs = chunks[10]
    print_colored("System:",preview_docs.page_content,"cyan")
    print_colored("System:",preview_docs.metadata,"cyan")
    return chunks

    # if not chunks:
    # raise ValueError("No document chunks provided to save_to_chroma.")
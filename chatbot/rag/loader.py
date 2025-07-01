from langchain_community.document_loaders import TextLoader, CSVLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from pathlib import Path
from chatbot.utils import log_function_call

import csv
import pandas as pd
import logging

DATA_PATH = "datasource/"
SUPPORTED_EXTENSIONS = [".md",".txt",".csv",".xlsx"]
logger = logging.getLogger(__name__)

@log_function_call
def load_documents():
    
    all_docs = []
    
    for ext in SUPPORTED_EXTENSIONS:
        for file_path in Path(DATA_PATH).rglob(f"*{ext}"):
            if ext in [".md",".txt"]:
                all_docs.extend(load_text(file_path))
            elif ext == ".csv":
                all_docs.extend(load_csv(file_path))
            elif ext == ".xlsx":
                all_docs.extend(load_excel(file_path))
            else:
                continue
    logging.info(f"Loaded {len(all_docs)} documents.")
    return all_docs

@log_function_call
def load_text(file_path):
    docs = []
    with open(file_path,newline='',encoding='utf-8') as f:
        content = f.read()
        
        raw_chunks = content.split("#")
        
        for chunk in raw_chunks:
            cleaned = chunk.strip()
            if cleaned:
                docs.append(Document(page_content=cleaned,metadata={"source": str(file_path)}))
    logging.info(f"Loaded {len(docs)} documents.")
    return docs

@log_function_call
def load_csv(file_path):
    docs = []
    with open(file_path,newline='',encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            content = "\n".join(f"{k}: {v}" for k,v in row.items())
            docs.append(Document(page_content=content, metadata={"source": str(file_path)}))
    logging.info(f"Loaded {len(docs)} documents.")
    return docs

@log_function_call
def load_excel(file_path):
    docs = []
    try:
        df = pd.read_excel(file_path)
        for _,row in df.iterrows():
            content = "\n".join(f"{col}: {row[col]}" for col in df.columns)
            docs.append(Document(page_content=content, metadata={"source": str(file_path)}))
    except Exception as e:
        logging.error(f"Failed to read Excel file {file_path}: {e}")
    logging.info(f"Loaded {len(docs)} documents.")
    return docs
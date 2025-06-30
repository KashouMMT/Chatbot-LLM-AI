from langchain_community.vectorstores import Chroma

from chatbot.tools import print_colored

def search(query_text,database : Chroma):
    results = database.similarity_search_with_relevance_scores(query_text,k=3)
    if len(results) == 0 or results [0][1] < 0.7:
        print_colored("System:","Unable to find matching results.")
        return None
    return results
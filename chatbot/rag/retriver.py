from .db_builder import Database
from chatbot.tools import print_colored,log_function_call

@log_function_call
def search(query_text,database : Database):
    results = database.chroma.similarity_search_with_relevance_scores(query_text,k=3)
    
    if not results:
        print_colored("System:", "No relevant results found.", "red")
        return results

    print_colored("System:", "Search Results:", "cyan")
    for i, (doc, score) in enumerate(results, start=1):
        print_colored(f"[{i}] Score: {score:.2f}", doc.page_content.strip(), "green")
        print_colored("Metadata:", doc.metadata, "yellow")
        print("-" * 50)
    
    return results  
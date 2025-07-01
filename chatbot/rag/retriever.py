from .db_builder import Database
from chatbot.tools import log_function_call

import logging

logger = logging.getLogger(__name__)

@log_function_call
def search(query_text: str, database: Database):
    # Wrap Chroma as a retriever
    retriever = database.chroma.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
        # For search query along with score.
        # search_type="similarity_score_threshold",
        # search_kwargs={"score_threshold": 0.75, "k": 5}
    )
    
    # Use retriever to search for relevant documents
    results = retriever.invoke(query_text)

    if not results:
        logger.warning("No relevant results found from search")
        return "No relevant results found from database."
    
    logger.info(f"Search Results: {results}")
    return results
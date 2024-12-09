from sentence_transformers import SentenceTransformer
import os
from typing import List, Union
import chromadb


# Generate embedding for a single string input
def generate_embedding(text: str, model_name: str = 'all-MiniLM-L6-v2') -> Union[list, None]:
    if not isinstance(text, str):
        return TypeError(f"Input must be a string. Got {type(text)._name_}")
    if not text.strip():
        return ValueError("Input string cannot be empty or contain only whitespace")
    try:
        model = SentenceTransformer(model_name)
        embedding = model.encode(text)
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Generate collection names for user data
def Collection_name_gen(user_id: str, collection_types: List[str]) -> List[str]:
    return [f"{user_id}_{collection_type}_collection" for collection_type in collection_types]

# Search in Chroma database
def searching_in_chroma(user_query: str, user_id: str, mode: str):
    database_directory = r'./vectorDB'
    os.makedirs(database_directory, exist_ok=True)
    client = chromadb.PersistentClient(path=database_directory)

    valid_modes = ['todo', 'notes', 'reminders']
    if mode not in valid_modes:
        return ValueError(f"Invalid mode. Must be one of {valid_modes}")

    collection_name = f"{user_id}_{mode}_collection"
    collection_object = client.get_or_create_collection(name=collection_name)

    query_embedding = generate_embedding(text=user_query)
    query_result = collection_object.query(query_embeddings=query_embedding, n_results=5)
    return query_result

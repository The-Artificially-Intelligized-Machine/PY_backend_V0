from sentence_transformers import SentenceTransformer
from typing import Union
import os
import chromadb
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from prompts.save import dict_list_to_string_list
import datetime
GROQ_API_KEY='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'
# Initialize models
chat = ChatGroq(
    temperature=0,
    model_name="gemma2-9b-it",
    groq_api_key = GROQ_API_KEY)

curr_time = datetime.datetime.now()

# Embedding function With error handeling
def generate_embedding(text: str, model_name: str = 'all-MiniLM-L6-v2') -> Union[list, None]:
    """
    Generate embedding for a single string input.
    
    Args:
        text: Input string to embed
        model_name: Sentence transformer model to use
    
    Returns:
        Embedding vector or None if generation fails
    """
    # Validate input
    if not isinstance(text, str):
        return TypeError(f"Input must be a string. Got {type(text).__name__}")
        #return False
    
    if not text.strip():
        return ValueError("Input string cannot be empty or contain only whitespace")
    
    try:
        # Create model
        model = SentenceTransformer(model_name)
        
        # Generate embedding
        embedding = model.encode(text)
        type(embedding)
        return embedding
    
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return f"Error generating embedding: {e}"
    
# Output serch result inchrma DB
def searching_in_chroma(User_qery, username, mode):
    # connect to DB
    database_directory = r"./vectorDB"
    # Ensure directory exists
    os.makedirs(database_directory, exist_ok=True)
    
    client = chromadb.PersistentClient(path=database_directory)
    
    # Validate mode
    valid_modes = ['todo', 'note', 'reminder']
    if mode not in valid_modes:
        return ValueError(f"Invalid mode. Must be one of {valid_modes}")
    
    # Concatenate userid and mode to create collection_name
    collection = f"{username}_{mode}_collection"
    
    collection_object=client.get_or_create_collection(name=collection)
    
    Qery_embedding = generate_embedding(text = User_qery)
    Query_result = collection_object.query(
        query_embeddings = Qery_embedding,
        n_results = 5
    )
    type(Query_result)
    return Query_result

def add_braces(answer):
    data = answer["documents"][0][0]
    data = str(data)
    update = re.sub(r"{","{{", data)
    update= re.sub(r"}","}}", update)
    return update

def agent_to_answer(context, user_query, user_name: str):
    query = user_query
    Answer_user = f"""
    Context Information:
    {context}

    User Query: {query}

    Carefully analyze the provided context and respond to the query based ONLY on the information available. 
    Follow these guidelines:
    1. Read the entire context thoroughly
    2. Identify relevant information directly related to the query
    3. Provide a precise, concise answer using only the details from the context
    4. If the information cannot be found in the context, clearly state that the answer is not available in the given information
    5. Do not add any external information or make assumptions beyond the provided context

    Your response should be:
    - Directly answering the specific question
    - Based solely on the context provided
    - Clear and to the point
    """

    prompt = ChatPromptTemplate.from_messages([ 
        ("system", f"You are azmth to user: {user_name}"),
        ("human", Answer_user)
    ])
    chain = prompt | chat

    try:
        result = chain.invoke({}).content.strip()
        return result
    except Exception as e:
        return str(e)
    
def main_search(user_query, username, mode):
    context = searching_in_chroma(user_query, username, mode)
    context = add_braces(context)
    
    answer = agent_to_answer(context,user_query, user_name= username)
    return answer
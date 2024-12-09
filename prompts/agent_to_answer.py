from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import datetime
import os

def agent_to_answer(context, user_query, user_name: str):
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    chat = ChatGroq(temperature=0, model_name="gemma2-9b-it", groq_api_key=GROQ_API_KEY)
    curr_time = datetime.datetime.now()

    answer_user = f"""
    Context Information: {context}
    User Query: {user_query}
    Carefully analyze the provided context and respond to the query based ONLY on the information available. Follow these guidelines:
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
        ("human", answer_user)
    ])
    chain = prompt | chat
    result = chain.invoke({}).content.strip()
    return result
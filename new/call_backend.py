from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import Dict, List, Tuple
import datetime
import os
from fastapi import HTTPException
from new.summar import summarizer

class ChatbotLogic:
    def __init__(self):
        self.groq_api_key = "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"
        self.chat = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
            groq_api_key=self.groq_api_key
        )
        self.conversation_store: Dict[str, Dict] = {}

    def generate_question(self, introduction: str, previous_questions: List[str]) -> str:
        """Generate next question based on context"""
        prompt = (
            "Based on the following user introduction, ask a specific, technical, or professional question "
            "that has not been asked before. Questions should be concise, targeted towards students, "
            "IT professionals, entrepreneurs, or investors. Include questions about how the user plans "
            "to use AZMTH as an AI-powered assistant for extracting todos and notes from messages. "
            "Do not ask questions with too much technical jargon. Note that these are people who "
            "have not used AZMTH. So remember asking stuff that is relevant to AZMTH but is also friendly to new users and beginners and not too daunting with jargon."
            "Also keep the questions specific and small. Don't ask something way too big for a beginner to answer."
            "Do not ask philosophical or psychological questions. Only ask one question at a time.\n\n"
            f"User Introduction: {introduction}\n"
            f"Previous Questions: {previous_questions}"
        )
        
        try:
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an AI assistant generating professional questions."),
                ("human", prompt)
            ])
            result = self.chat.invoke(prompt)
            return result.content.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")

    def start_conversation(self, introduction: str) -> Tuple[str, str, bool]:
        """Initialize a new conversation and return first question"""
        conversation_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.conversation_store[conversation_id] = {
            "introduction": introduction,
            "previous_questions": [],
            "responses": {},
            "active": True
        }
        
        question = self.generate_question(introduction, [])
        self.conversation_store[conversation_id]["previous_questions"].append(question)
        
        return conversation_id, question, True

    def continue_conversation(self, conversation_id: str, user_input: str) -> Tuple[str, bool]:
        """Process user input and generate next question"""
        if conversation_id not in self.conversation_store:
            raise HTTPException(status_code=404, detail="Conversation not found")
            
        conversation = self.conversation_store[conversation_id]
        
        if user_input.lower() == "preview":
            conversation["active"] = False
            print("processsssssed for saveeeeeeeeeeeeeeeee")
            filelocation = self.save_conversation(conversation_id)
            return filelocation
        
        if conversation["previous_questions"]:
            last_question = conversation["previous_questions"][-1]
            conversation["responses"][last_question] = user_input
        
        if conversation["active"]:
            next_question = self.generate_question(
                conversation["introduction"],
                conversation["previous_questions"]
            )
            conversation["previous_questions"].append(next_question)
            return next_question, True
        
        return "Conversation has ended", False

    def get_conversation(self, conversation_id: str) -> Dict:
        """Retrieve conversation history"""
        if conversation_id not in self.conversation_store:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return self.conversation_store[conversation_id]

    def save_conversation(self, conversation_id: str) -> None:
        """Save conversation to file"""
        if conversation_id not in self.conversation_store:
            raise HTTPException(status_code=404, detail="Conversation not found")

        conversation = self.conversation_store[conversation_id]
        
        # Create directory if it doesn't exist
        save_directory = "conversations"
        os.makedirs(save_directory, exist_ok=True)

        filename = os.path.join(save_directory, f"conversation_{conversation_id}.txt")

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("User Introduction:\n")
                f.write(f"{conversation['introduction']}\n\n")
                
                for question in conversation["previous_questions"]:
                    f.write(f"Question: {question}\n")
                    answer = conversation["responses"].get(question, "Unanswered")
                    f.write(f"Answer: {answer}\n\n")

            result = summarizer(filename)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving conversation: {str(e)}")
from sentence_transformers import SentenceTransformer
from typing import List
import os
import chromadb

def dict_list_to_string_list(input_list):
    # Get the length of the input list
    n = len(input_list)
    # Initialize the result list
    result = []
    # Loop n times and append converted strings
    for i in range(n):
        # Convert the current dictionary to a string
        task_string = str(input_list[i])
        result.append(task_string)
    
    return result

def Embedd_Loop(items: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[List[float]]:
    # Initialize the model
    model = SentenceTransformer(model_name)
    
    # Generate embeddings
    embeddings = model.encode(items)
    
    return embeddings.tolist()

def collection_name_gen(user_id: str, collection_types: List[str]) -> List[str]:
    return [f"{user_id}_{collection_type}_collection" for collection_type in collection_types]

# Todo Counter

class TodoCounter:
    def __init__(self, counter_file='todo_counter.txt'):
        """
        Initialize the TodoCounter with a file to persist the count
        
        :param counter_file: Path to the file storing the counter value
        """
        self.counter_file = counter_file
        
        # Create the file if it doesn't exist
        if not os.path.exists(self.counter_file):
            with open(self.counter_file, 'w') as f:
                f.write('0')
        
        # Read the current count from the file
        with open(self.counter_file, 'r') as f:
            self.count = int(f.read().strip())
    
    def _save_count(self):
        """
        Save the current count to the file
        """
        with open(self.counter_file, 'w') as f:
            f.write(str(self.count))
    
    def increment_counter_by(self, amount):
        """
        Increment the counter by a specified amount
        
        :param amount: Number to increase the counter by
        """
        self.count += amount
        self._save_count()
        print(f"Counter incremented. New count: {self.count}")
    
    def decrement_counter_by(self, amount):
        """
        Decrement the counter by a specified amount
        
        :param amount: Number to decrease the counter by
        """
        # Ensure count doesn't go below 0
        self.count = max(0, self.count - amount)
        self._save_count()
        print(f"Counter decremented. New count: {self.count}")
    
    def get_current_count(self):
        """
        Get the current count
        
        :return: Current count value
        """
        return self.count

class NotesCounter:
    def __init__(self, counter_file='notes_counter.txt'):
        """
        Initialize the NotesCounter with a file to persist the count
        
        :param counter_file: Path to the file storing the counter value
        """
        self.counter_file = counter_file
        
        # Create the file if it doesn't exist
        if not os.path.exists(self.counter_file):
            with open(self.counter_file, 'w') as f:
                f.write('0')
        
        # Read the current count from the file
        with open(self.counter_file, 'r') as f:
            self.count = int(f.read().strip())
    
    def _save_count(self):
        """
        Save the current count to the file
        """
        with open(self.counter_file, 'w') as f:
            f.write(str(self.count))
    
    def increment_counter_by(self, amount):
        """
        Increment the counter by a specified amount
        
        :param amount: Number to increase the counter by
        """
        self.count += amount
        self._save_count()
        print(f"Notes Counter incremented. New count: {self.count}")
    
    def decrement_counter_by(self, amount):
        """
        Decrement the counter by a specified amount
        
        :param amount: Number to decrease the counter by
        """
        # Ensure count doesn't go below 0
        self.count = max(0, self.count - amount)
        self._save_count()
        print(f"Notes Counter decremented. New count: {self.count}")
    
    def get_current_count(self):
        """
        Get the current count
        
        :return: Current count value
        """
        return self.count

class ReminderCounter:
    def __init__(self, counter_file='reminder_counter.txt'):
        """
        Initialize the ReminderCounter with a file to persist the count
        
        :param counter_file: Path to the file storing the counter value
        """
        self.counter_file = counter_file
        
        # Create the file if it doesn't exist
        if not os.path.exists(self.counter_file):
            with open(self.counter_file, 'w') as f:
                f.write('0')
        
        # Read the current count from the file
        with open(self.counter_file, 'r') as f:
            self.count = int(f.read().strip())
    
    def _save_count(self):
        """
        Save the current count to the file
        """
        with open(self.counter_file, 'w') as f:
            f.write(str(self.count))
    
    def increment_counter_by(self, amount):
        """
        Increment the counter by a specified amount
        
        :param amount: Number to increase the counter by
        """
        self.count += amount
        self._save_count()
        print(f"Reminder Counter incremented. New count: {self.count}")
    
    def decrement_counter_by(self, amount):
        """
        Decrement the counter by a specified amount
        
        :param amount: Number to decrease the counter by
        """
        # Ensure count doesn't go below 0
        self.count = max(0, self.count - amount)
        self._save_count()
        print(f"Reminder Counter decremented. New count: {self.count}")
    
    def get_current_count(self):
        """
        Get the current count
        
        :return: Current count value
        """
        return self.count

def convert_to_string_and_return_embedding(extracted_result, username):
    # Connect to DB
    database_directory = r"./vectorDB"
    
    # Ensure directory exists
    os.makedirs(database_directory, exist_ok=True)
    client = chromadb.PersistentClient(path=database_directory)
    
    # Generate collections names specific to the user
    collections_name_user_specific = collection_name_gen(username, ["todo", "note", "reminder"])
    
    # Initialize TodoCounter
    todo_counter = TodoCounter()
    notes_counter = NotesCounter()
    reminder_counter = ReminderCounter()
    
    # Process Todos
    if extracted_result[0]:
        todos_list = extracted_result[0]
        todos_list = dict_list_to_string_list(todos_list)
        todos_embedding_list = Embedd_Loop(todos_list)
        
        # Get current todo count or start from 0
        todo_count = todo_counter.get_current_count() or 0
        
        # Create user's todo collection
        user_todos_collection = client.get_or_create_collection(collections_name_user_specific[0])
        
        # Upsert todos with unique IDs
        user_todos_collection.upsert(
            ids=[f"{username}_todo_{i + todo_count}" for i in range(len(todos_list))],
            documents=todos_list,
            embeddings=todos_embedding_list
        )
        todo_counter.increment_counter_by(len(todos_list))
        print(f"Saved {len(todos_list)} todos for user {username}")
    
    # Process Notes
    if extracted_result[1]:
        notes_list = extracted_result[1]
        notes_list = dict_list_to_string_list(notes_list)
        notes_embedding_list = Embedd_Loop(notes_list)
        
        # Get current todo count or start from 0
        note_count = notes_counter.get_current_count() or 0
        
        # Create user's notes collection
        user_notes_collection = client.get_or_create_collection(collections_name_user_specific[1])
        
        # Upsert notes
        user_notes_collection.upsert(
            ids=[f"{username}_note_{i + note_count}" for i in range(len(notes_list))],
            documents=notes_list,
            embeddings=notes_embedding_list
        )
        notes_counter.increment_counter_by(len(notes_list))
        print(f"Saved {len(notes_list)} notes for user {username}")
    
    # Process Reminders
    if extracted_result[2]:
        reminders_list = extracted_result[2]
        reminders_list = dict_list_to_string_list(reminders_list)
        reminders_embedding_list = Embedd_Loop(reminders_list)
        
        reminder_count = reminder_counter.get_current_count() or 0
        
        # Create user's reminders collection
        user_reminders_collection = client.get_or_create_collection(collections_name_user_specific[2])
        
        # Upsert reminders
        user_reminders_collection.upsert(
            ids=[f"{username}_reminder_{i + reminder_count}" for i in range(len(reminders_list))],
            documents=reminders_list,
            embeddings=reminders_embedding_list
        )
        reminder_counter.increment_counter_by(len(reminders_list))
        print(f"Saved {len(reminders_list)} reminders for user {username}")
    
    if extracted_result[0] or extracted_result[1] or extracted_result[2]:
        return(f"Data for user {username} has been successfully saved to the database.")
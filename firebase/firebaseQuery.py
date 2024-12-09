from firebase.firebase_init import db

def verify_user_in_firestore(email: str, username: str):
    """
    Verifies if a user with the given email and username exists in Firestore.
    """
    try:
        users_ref = db.collection("users")
        query = users_ref.where("email", "==", email).where("username", "==", username).stream()

        users = [doc.to_dict() for doc in query]
        if not users:
            return None
        return users[0]
    except Exception as e:
        raise e

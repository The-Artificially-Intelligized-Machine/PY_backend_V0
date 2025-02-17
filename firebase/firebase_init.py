import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("admin.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
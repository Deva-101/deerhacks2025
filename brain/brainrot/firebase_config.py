import os
import firebase_admin
from firebase_admin import credentials, db

# Get the absolute path to the JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED_PATH = os.path.join(BASE_DIR, "deerhacks2025-firebase-adminsdk-fbsvc-d20d847bda.json")

# Initialize Firebase app
cred = credentials.Certificate(CRED_PATH)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://deerhacks2025-default-rtdb.firebaseio.com/'
    })

def get_database_ref():
    """ Returns a reference to the Firebase Realtime Database """
    return db.reference()

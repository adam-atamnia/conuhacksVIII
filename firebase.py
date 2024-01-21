import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase Admin SDK with your service account key JSON file
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def add_documents_to_firestore(request):
    try:
        # Get the data as JSON from the request (assuming it's a POST request)
        request_json = request.get_json()

        # Check if the 'data' key is present and contains a list of dictionaries
        if 'data' in request_json and isinstance(request_json['data'], list):
            data_list = request_json['data']

            # Firestore collection reference
            collection_ref = db.collection('your_collection_name')  # Replace with your desired collection name

            # Add each dictionary as a document
            for data in data_list:
                collection_ref.add(data)

            return "Documents added to Firestore successfully.", 200
        else:
            return "Invalid request data format.", 400
    except Exception as e:
        return str(e), 500
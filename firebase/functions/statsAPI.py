from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from Hackathon2024 import turn_to_dict
import csv

db = firestore.client()
appointments_Ref = db.collection('appointments')
batch = db.batch()

statsAPI = Blueprint('statsAPI', __name__)


  


@statsAPI.route('/get_data', methods=['GET'])
def get_data_between_dates():
    try:
        # Get the start and end dates for the reservation day from the query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # Convert start_date and end_date to datetime objects if needed
        # Example: start_date = "2022-11-27", end_date = "2022-11-27"
        # You can use datetime.strptime to parse the date strings if needed.

        # Query Firestore to retrieve records within the specified time range
        appointments_ref = db.collection('appointments')
        query = appointments_ref.where('Reservation_Date', '>=', start_date).where('Reservation_Date', '<=', end_date)
        results = query.stream()

        # Create a list to store the retrieved records
        records = []

        for doc in results:
            # Convert Firestore document data to a Python dictionary
            data = doc.to_dict()

            # Add the document data to the list of records
            records.append(data)

        # Return the list of records as a JSON response
        return jsonify(records)

    except Exception as e:
        return jsonify({"error": str(e)}), 500











# @statsAPI.route('/updateStats', methods=['POST'])
# def updateStats():
#   try:
#     list_of_dict = get_list()

#     # # out with the old
#     # docs = appointments_Ref.stream()
#     # # Delete each document
#     # for doc in docs:
#     #   doc.reference.delete()


#     # in with the new
#     for data in list_of_dict:
#       new_doc_ref = db.collection("appointments").document()
#       batch.set(new_doc_ref, data)
    
#     batch.commit()

#     return jsonify({"success": True}), 200
#   except Exception as e:
#     return f'An ErrorOccured: {e}'


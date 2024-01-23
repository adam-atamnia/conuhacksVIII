from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
batch = db.batch()
appointments_collection_name = 'appointments'

statsAPI = Blueprint('statsAPI', __name__)


@statsAPI.route('/get_data', methods=['GET'])
def get_data_between_dates():
    try:
        # Get the start and end dates for the reservation day from the query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        # isAccepted = request.args.get('isAccepted')
        # type = request.args.get('type')

        # Convert start_date and end_date to datetime objects if needed
        # Example: start_date = "2022-11-27", end_date = "2022-11-27"
        # You can use datetime.strptime to parse the date strings if needed.

        # Query Firestore to retrieve records within the specified time range
        appointments_ref = db.collection(appointments_collection_name)
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

from sapParser import get_final_appointments_dict_list

@statsAPI.route('/updateStats', methods=['POST'])
def update_stats():
  try:
    appointments = get_final_appointments_dict_list(request.json['appointments'])

    appointments_Ref = db.collection(appointments_collection_name)

    # in with the new
    for appointment in appointments:
      new_doc_ref = appointments_Ref.document()
      batch.set(new_doc_ref, appointment)
    
    batch.commit()

    return jsonify({"success": True}), 200
  except Exception as e:
    return f'An ErrorOccured: {e}'
  
@statsAPI.route('/deleteStats', methods=['DELETE'])
def delete_stats():
  try:

    appointments_Ref = db.collection(appointments_collection_name)
    delete_documents_in_batches(appointments_Ref)

    return jsonify({"success": True}), 200
  except Exception as e:
    return f'An ErrorOccured: {e}'


def delete_documents_in_batches(collection_ref, batch_size=500):
    while True:
        # Retrieve a batch of documents
        docs = collection_ref.limit(batch_size).stream()

        # Start a new batch
        batch = db.batch()
        count = 0

        for doc in docs:
            # Add a delete operation to the batch
            batch.delete(doc.reference)
            count += 1

        # If there are no documents left, break the loop
        if count == 0:
            break

        # Commit the batch
        batch.commit()


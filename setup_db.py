from firebase_admin import firestore
import csv

from firebase_admin import credentials, initialize_app

cred = credentials.Certificate('./credentials.json')

default_app = initialize_app(cred)

db = firestore.client()
appointments_Ref = db.collection('appointments')
batch = db.batch()



def get_list():
  csv_file_path = './sap_dataset.csv'

  # Initialize an empty list to store the dictionaries
  data_list = []

  # Open the CSV file and read it
  with open(csv_file_path, mode='r', newline='') as csv_file:
      csv_reader = csv.reader(csv_file)
      
      # Skip any existing header row if it exists
      next(csv_reader, None)
      
      # Iterate over each row in the CSV and create dictionaries with specified keys
      for row in csv_reader:
          # Assuming the CSV columns are in this order: call_time, appointment_time, type
          Type, Book_Date, Book_Time,Reservation_Date,Reservation_Time,Reservation_End_Time,isAccepted,Revenue= row
          data_dict = {
              "Book_Date": Book_Date,
              "Book_Time": Book_Time,
              "Reservation_Date": Reservation_Date,
              "Reservation_Time": Reservation_Time,
              "Reservation_End_Time": Reservation_End_Time,
              "isAccepted": isAccepted,
              "Revenue": Revenue,
              "type": Type
          }
          data_list.append(data_dict)
  

  return data_list



list_of_dict = get_list()

# # out with the old
# docs = appointments_Ref.stream()
# # Delete each document
# for doc in docs:
#   doc.reference.delete()


# in with the new
for data in list_of_dict:
  new_doc_ref = db.collection("appointments").document()
  batch.set(new_doc_ref, data)

batch.commit()
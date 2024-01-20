import csv
from datetime import datetime
import copy

# Specify the path to your CSV file
csv_file_path = './datafile.csv'

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
        call_time, appointment_time, appointment_type = row
        data_dict = {
            "call_time": call_time,
            "appointment_time": appointment_time,
            "type": appointment_type
        }
        data_list.append(data_dict)


# Sort the list by appointment_time
appointments = sorted(data_list, key=lambda x: datetime.strptime(x["call_time"], "%Y-%m-%d %H:%M"))


# Create the dictionary
bay_def = {
    'appointments': [],
}

# Create a list by repeating the dictionary 10 times using list comprehension
bay_list = [bay_def.copy() for _ in range(10)]

reserved_bays = [
    'compact',
    'medium',
    'full-size',
    'class 1 truck',
    'class 2 truck',
]

def add_appointment(appointment):

    for i in range(len(bay_list)):
        if i < 5 and reserved_bays[i] != appointment['type']:
            continue
        if is_bay_available(i, appointment):
            bay_list[i]['appointments'].append(appointment)
            return True
    return False
        
def is_bay_available(bay_index, appointment):
    for booked_appointment in bay_list[bay_index]['appointments']:
        if is_conflict(booked_appointment, appointment):
            return False
    return True

from datetime import datetime, timedelta

def is_conflict(appointment1, appointment2):
    # Define servicing times for each type
    servicing_times = {
        'compact': timedelta(minutes=30),
        'medium': timedelta(minutes=30),
        'full-size': timedelta(minutes=30),
        'class 1 truck': timedelta(hours=1),
        'class 2 truck': timedelta(hours=2),
    }

    # Parse appointment times as datetime objects
    time_format = "%Y-%m-%d %H:%M"
    start_time1 = datetime.strptime(appointment1['appointment_time'], time_format)
    end_time1 = start_time1 + servicing_times.get(appointment1['type'], timedelta())
    
    start_time2 = datetime.strptime(appointment2['appointment_time'], time_format)
    end_time2 = start_time2 + servicing_times.get(appointment2['type'], timedelta())

    # Check for conflict
    if start_time1 < end_time2 and start_time2 < end_time1:
        return True  # Conflict exists
    else:
        return False  # No conflict

# # Example appointments
# appointment1 = {'appointment_time': '2022-11-30 18:19', 'type': 'class 2 truck'}
# appointment2 = {'appointment_time': '2022-11-30 18:49', 'type': 'compact'}

# # Check for conflict
# if is_conflict(appointment1, appointment2):
#     print("There is a conflict between the two appointments.")
# else:
#     print("There is no conflict between the two appointments.")




for i in range(len(appointments)):

    is_added = add_appointment(appointments[i])

    appointments[i]['is_added'] = is_added
    # print(appointments[i])

print(appointments)

import csv

# List of dictionaries
data_list = [
    {'name': 'John', 'age': 30},
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 35}
]

# Specify the path to the CSV file
csv_file_path = 'output.csv'

# Write the list of dictionaries to the CSV file
with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = appointments[0].keys()  # Assuming all dictionaries have the same keys
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data rows
    writer.writerows(appointments)



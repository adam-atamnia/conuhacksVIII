import csv
from datetime import datetime

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
        if is_outside_working_hours(appointment): return False
        if i < 5 and reserved_bays[i] != appointment['type']:
            continue
        if binary_search_for_conflict(i, appointment):
            bay_list[i]['appointments'].append(appointment)
            return True
    return False
        
def is_bay_available(bay_index, appointment):
    for booked_appointment in bay_list[bay_index]['appointments']:
        if is_conflict(booked_appointment, appointment):
            return False
    return True

def binary_search_for_conflict(bay_index, appointment):
    # Sort the list of appointments by appointment_time
    bay_list[bay_index]['appointments'].sort(key=lambda x: x['appointment_time'])
    
    # Binary search for conflicts
    left, right = 0, len(bay_list[bay_index]['appointments']) - 1
    while left <= right:
        mid = (left + right) // 2
        booked_appointment = bay_list[bay_index]['appointments'][mid]
        
        if is_conflict(booked_appointment, appointment):
            return False  # Conflict found, return False
        elif booked_appointment['appointment_time'] < appointment['appointment_time']:
            left = mid + 1
        else:
            right = mid - 1
    
    return True  # No conflicts found

from datetime import datetime, timedelta

def is_outside_working_hours(appointment):
    # Define the working hour thresholds (7 AM and 7 PM)
    start_working_hour = datetime.strptime('07:00:00', '%H:%M:%S').time()
    end_working_hour = datetime.strptime('19:00:00', '%H:%M:%S').time()

    # Parse the appointment time as a datetime object
    appointment_time = datetime.strptime(appointment['appointment_time'], '%Y-%m-%d %H:%M')

    # Extract the time part from the datetime
    appointment_time = appointment_time.time()

    # Check if the appointment starts before 7 AM or finishes after 7 PM
    if appointment_time < start_working_hour or appointment_time > end_working_hour:
        return True  # Outside working hours
    else:
        return False  # Within working hours

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



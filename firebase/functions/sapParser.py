import csv
from datetime import datetime, timedelta

def read_original_appointments_csv():
# Specify the path to your CSV file
    csv_file_path = r'C:\Users\adam1\Desktop\Side_Projects\conuhacksVIII\data_csv\datafile.csv' # './datafile.csv'

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
    appointments = sort_appointments_and_convert_time(data_list)

    return appointments

def sort_appointments_and_convert_time(appointments):
    for data_dict in appointments:
        data_dict["call_time"] = datetime.strptime(data_dict["call_time"], "%Y-%m-%d %H:%M")
        data_dict["appointment_time"] = datetime.strptime(data_dict["appointment_time"], "%Y-%m-%d %H:%M")
    return sorted(appointments, key=lambda x: x["call_time"])

bay_list = [[] for _ in range(10)]

reserved_bays = [
    'compact',
    'medium',
    'full-size',
    'class 1 truck',
    'class 2 truck',
    'any 1',
    'any 2',
    'any 3',
    'any 4',
    'any 5',
]

revenue_per_type = {
    'compact': 150,
    'medium': 150,
    'full-size': 150,
    'class 1 truck': 250,
    'class 2 truck': 700,
}

servicing_times = {
    'compact': timedelta(minutes=30),
    'medium': timedelta(minutes=30),
    'full-size': timedelta(minutes=30),
    'class 1 truck': timedelta(hours=1),
    'class 2 truck': timedelta(hours=2),
}

def add_appointment(appointment):

    for i in range(len(bay_list)):
        if is_outside_working_hours(appointment): return False
        if i < 5 and reserved_bays[i] != appointment['type']:
            continue
        if is_bay_available_binary_search(i, appointment):
            return True, reserved_bays[i], revenue_per_type[appointment['type']]
    return False, 'none', revenue_per_type[appointment['type']]
        
def is_bay_available(bay_index, appointment):
    for booked_appointment in bay_list[bay_index]:
        if is_conflict(booked_appointment, appointment):
            return False
    return True

def is_bay_available_binary_search(bay_index, appointment):
    
    # Binary search for conflicts and find insertion point
    left, right = 0, len(bay_list[bay_index])
    while left < right:
        mid = (left + right) // 2
        booked_appointment = bay_list[bay_index][mid]

        if is_conflict(booked_appointment, appointment):
            return False  # Conflict found, return False
        elif booked_appointment['appointment_time'] < appointment['appointment_time']:
            left = mid + 1
        else:
            right = mid

    # Insert the appointment at the found position
    bay_list[bay_index].insert(left, appointment)
    return True  # Appointment inserted successfully

def is_outside_working_hours(appointment):
    # Define the working hour thresholds (7 AM and 7 PM)
    start_working_hour = datetime.strptime('07:00:00', '%H:%M:%S').time()
    end_working_hour = datetime.strptime('19:00:00', '%H:%M:%S').time()

    # Parse the appointment time as a datetime object
    appointment_time = appointment['appointment_time']

    # Extract the time part from the datetime
    appointment_time = appointment_time.time()

    # Check if the appointment starts before 7 AM or finishes after 7 PM
    if appointment_time < start_working_hour or appointment_time > end_working_hour:
        return True  # Outside working hours
    else:
        return False  # Within working hours

def is_conflict(appointment1, appointment2):

    # Parse appointment times as datetime objects
    start_time1 = appointment1['appointment_time']
    end_time1 = start_time1 + servicing_times.get(appointment1['type'], timedelta())
    
    start_time2 = appointment2['appointment_time']
    end_time2 = start_time2 + servicing_times.get(appointment2['type'], timedelta())

    # Check for conflict
    if start_time1 < end_time2 and start_time2 < end_time1:
        return True  # Conflict exists
    else:
        return False  # No conflict

def output_csv(appointments):
    # Specify the path to the CSV file
    csv_file_path = 'output.csv'

    # Write the list of dictionaries to the CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = appointments[0].keys()  
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write the data rows
        writer.writerows(appointments)

def get_final_appointments(appointments):
    for i in range(len(appointments)):

        is_added, bay_name, revenue = add_appointment(appointments[i])

        appointments[i]['is_added'] = is_added
        appointments[i]['bay_name'] = bay_name
        appointments[i]['revenue'] = revenue
    
    return appointments

def get_final_appointments_csv():
    appointments = read_original_appointments_csv()
    
    appointments = get_final_appointments(appointments)
    
    output_csv(appointments)

def get_final_appointments_dict_list(dict_list):
    appointments = sort_appointments_and_convert_time(dict_list)

    return get_final_appointments(appointments)

if __name__ == "__main__":
    get_final_appointments_csv()

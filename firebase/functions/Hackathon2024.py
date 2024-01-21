#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime,time, timedelta


pd.set_option('display.max_rows', 10)


# column_names = ["Book time", "Reservation", "Type"]
# sap_dataset = pd.read_csv("C:/Users/TheRe/Downloads/datafile.csv",names = column_names)


def csvSplit(df):
    df[['Book Date', 'Book Time']] = df['Book time'].str.split(' ', expand=True)
    df[['Reservation Date', 'Reservation Time']] = df['Reservation'].str.split(' ', expand=True)
    df = df.drop(['Book time', 'Reservation'], axis=1)


def calculateRevenue(row):
    revenue = 0

    if row['Type'] == 'compact':
         revenue += 150
    elif row['Type'] == 'medium':
           revenue += 150
    elif row['Type'] == 'full-size':
        revenue += 150
    elif row['Type'] == 'class 1 truck':
        revenue += 250
    elif row['Type'] == 'class 2 truck':
        revenue += 700
            
    if row['isAccepted'] == False:
        revenue *= -1

    return revenue


def parse_time(time_input):
    if isinstance(time_input, str):
        return datetime.strptime(time_input, '%H:%M').time()
    elif isinstance(time_input, time):
        return time_input
    else:
        raise TypeError("Time input must be a string or a datetime.time object")


def parseAndSortDataFrame(df, target_day):
    # Convert date columns to datetime objects
    df['Reservation Date'] = pd.to_datetime(df['Reservation Date'])
    df['Book Date'] = pd.to_datetime(df['Book Date'])

    # Convert 'Reservation Time' from string to datetime.time
    df['Reservation Time'] = df['Reservation Time'].apply(parse_time)
    def calculate_end_time(row):
        # Combine date and time into a full datetime object
        reservation_datetime = datetime.combine(row['Reservation Date'], row['Reservation Time'])
        
        if row['Type'] == 'class 1 truck':
            end_datetime = reservation_datetime + timedelta(hours=1)
        elif row['Type'] == 'class 2 truck':
            end_datetime = reservation_datetime + timedelta(hours=2)
        else:
            end_datetime = reservation_datetime + timedelta(minutes=30)

        # Extracting only the time component for the end time
        return end_datetime.time()

    # Apply the function to calculate 'Reservation End Time'
    df['Reservation End Time'] = df.apply(calculate_end_time, axis=1)

    # Filter the DataFrame based on the specified day
    filtered_df = df[df['Reservation Date'] == pd.to_datetime(target_day)]

    # Sort the DataFrame
    sorted_df = filtered_df.sort_values(by=['Book Date', 'Book Time','Reservation Time'])

    return sorted_df


# Generate time slots from 7 AM to 7 PM
def generate_time_slots(start_time, end_time, interval_minutes):
    times = []
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time)
        current_time += timedelta(minutes=interval_minutes)
    return times

# Create the initial empty schedule
def create_schedule(placeholder_date):
    # Extract year, month, and day from the placeholder_date
    year = placeholder_date.year
    month = placeholder_date.month
    day = placeholder_date.day

    garage_types = ['compact', 'medium', 'full-size', 'class 1 truck', 'class 2 truck', 'Any 1', 'Any 2', 'Any 3', 'Any 4', 'Any 5']
    time_slots = generate_time_slots(datetime(year, month, day, 7, 0), datetime(year, month, day, 19, 0), 1)
    schedule = pd.DataFrame(index=time_slots, columns=garage_types)
    schedule.fillna('Available', inplace=True)

    return schedule

# Function to book a reservation
def book_reservation(schedule, garage_type, start_time_str, end_time_str, placeholder_date):
    # Parse the start and end times and combine them with the placeholder date
    start_time = datetime.combine(placeholder_date, parse_time(start_time_str))
    end_time = datetime.combine(placeholder_date, parse_time(end_time_str))

    # Check if the end time is after 7 PM
    if end_time > datetime(placeholder_date.year, placeholder_date.month, placeholder_date.day, 19, 0):
        return schedule  # Reject the reservation

    # Adjust for garage-specific or 'any' type
    if garage_type not in ['compact', 'medium', 'full-size', 'class 1 truck', 'class 2 truck']:
        garage_type = [col for col in schedule.columns if 'Any ' in col and schedule.loc[start_time:end_time, col].eq('Available').all()][0]
    
    # Mark the time slot as 'Not Available'
    schedule.loc[start_time:end_time, garage_type] = 'Not Available'
    return schedule




def book_reservations_from_df(df, garage_slots):
    def parse_time(time_str, date):
        # Combine time with the given date
        return datetime.combine(date, datetime.strptime(time_str, '%H:%M').time())

    # Initialize 'isAccepted' column to False
    df['isAccepted'] = False

    for index, row in df.iterrows():
        garage_type = row['Type']
        placeholder_date = row['Reservation Date']
        start_time_str = row['Reservation Time'].strftime('%H:%M')
        end_time_str = row['Reservation End Time'].strftime('%H:%M')
        
        # Parse the start and end times
        start_time = parse_time(start_time_str, placeholder_date)
        end_time = parse_time(end_time_str, placeholder_date)

        is_booked = False
        
        # Adjust for garage-specific or 'any' type
        if garage_type in ['compact', 'medium', 'full-size', 'class 1 truck', 'class 2 truck']:
            # Check if specific type garage is available
            if garage_slots.loc[start_time:end_time, garage_type].eq('Available').all():
                selected_garage = garage_type
                is_booked = True
            else:
                # Find an available 'Any' garage
                available_any_garages = [col for col in garage_slots.columns if 'Any ' in col]
                for any_garage in available_any_garages:
                    if garage_slots.loc[start_time:end_time, any_garage].eq('Available').all():
                        selected_garage = any_garage
                        is_booked = True
                        break

        # Mark the time slot as 'Not Available' and update 'isAccepted'
        if is_booked:
            garage_slots.loc[start_time:end_time, selected_garage] = 'Not Available' + ' ' + row['Type']
            df.at[index, 'isAccepted'] = True
            
    df['Revenue'] = df.apply(calculateRevenue, axis=1)

    return garage_slots,df



def createFullDataset(df,start_date,end_date):
    sap_dataset = csvSplit(df)
    def create_schedule_for_day(start_date):
        year = start_date.year
        month = start_date.month
        day = start_date.day

        garage_types = ['compact', 'medium', 'full-size', 'class 1 truck', 'class 2 truck', 'Any 1', 'Any 2', 'Any 3', 'Any 4', 'Any 5']
        time_slots = generate_time_slots(datetime(year, month, day, 7, 0), datetime(year, month, day, 19, 0), 1)
        schedule = pd.DataFrame(index=time_slots, columns=garage_types)
        schedule.fillna('Available', inplace=True)

        return schedule

    # Initialize counters for the total accepted and rejected reservations
    total_accepted = 0
    total_rejected = 0

    # Iterate over each day in the date range
    current_date = start_date

    while current_date <= end_date:
        # Create garage slots for the current day
        daily_garage_slots = create_schedule_for_day(current_date)

        # Use parseAndSortDataFrame to get the reservations for the current day
        daily_reservations = parseAndSortDataFrame(sap_dataset, current_date)
    
        # Book reservations and update the DataFrame
        daily_garage_slots, daily_reservations = book_reservations_from_df(daily_reservations, daily_garage_slots)

        for index, row in daily_reservations.iterrows():
        # Get the index of the row in sap_dataset that matches the current row
            matching_index = sap_dataset[
            (sap_dataset['Reservation Date'] == sap_dataset['Reservation Date']) &
            (sap_dataset['Reservation Time'] == sap_dataset['Reservation Time']) &
            (sap_dataset['Type'] == row['Type'])].index

            # Check if there is a matching row in sap_dataset
            if not matching_index.empty:
                matching_index = matching_index[0]  # Take the first matching index

            # Update the 'isAccepted' and 'Revenue' values in sap_dataset
            sap_dataset.at[matching_index, 'isAccepted'] = row['isAccepted']
            sap_dataset.at[matching_index, 'Revenue'] = row['Revenue']
        
        # Count accepted and rejected reservations for the day
        accepted = daily_reservations['isAccepted'].sum()
        rejected = len(daily_reservations) - accepted

        # Update total counters
        total_accepted += accepted
        total_rejected += rejected

        # Print out daily statistics
        print(f"On {current_date.date()}, {accepted} reservations were accepted and {rejected} were rejected.")

        # Move to the next day
        current_date += timedelta(days=1)

    # # Print out total statistics
    # print(f"Total accepted reservations: {total_accepted}")
    # print(f"Total rejected reservations: {total_rejected}")

    return sap_dataset


# In[24]:


def createFullDatasetFullTime(df):
    start_date = datetime(2022, 10, 1)
    end_date = datetime(2022, 11, 30)
    return createFullDataset(df,start_date,end_date)




def create_schedule_for_day(placeholder_date):
    year = placeholder_date.year
    month = placeholder_date.month
    day = placeholder_date.day

    garage_types = ['compact', 'medium', 'full-size', 'class 1 truck', 'class 2 truck', 'Any 1', 'Any 2', 'Any 3', 'Any 4', 'Any 5']
    time_slots = generate_time_slots(datetime(year, month, day, 7, 0), datetime(year, month, day, 19, 0), 1)
    schedule = pd.DataFrame(index=time_slots, columns=garage_types)
    schedule.fillna('Available', inplace=True)

    return schedule

# Initialize counters for the total accepted and rejected reservations

# profit = sap_dataset[sap_dataset['Revenue'] > 0]['Revenue'].sum()

# loss = sap_dataset[sap_dataset['Revenue'] < 0]['Revenue'].sum()



def turn_to_dict(csv):

    import os
    current_directory = os.getcwd()
    print(current_directory, '--------------------------------------------------') 

    column_names = ["Book time", "Reservation", "Type"]
    original_df = pd.read_csv(csv, names = column_names)

    df = createFullDatasetFullTime(original_df)

    dictionairy = pd.DataFrame(df)

    # Transform the DataFrame into a list of dictionaries
    list_of_dicts = dictionairy.to_dict(orient='records')

    return list_of_dicts



def generateAvailableSlots(df, garage_slots):
    def parse_time(time_str, date):
        # Combine time with the given date
        return datetime.combine(date, datetime.strptime(time_str, '%H:%M').time())

    # Initialize 'isAccepted' column to False
    df['isAccepted'] = False

    for index, row in df.iterrows():
        garage_type = row['Type']
        placeholder_date = row['Reservation Date']
        start_time_str = row['Reservation Time'].strftime('%H:%M')
        end_time_str = row['Reservation End Time'].strftime('%H:%M')
        
        # Parse the start and end times
        start_time = parse_time(start_time_str, placeholder_date)
        end_time = parse_time(end_time_str, placeholder_date)

        is_booked = False
        
        # Adjust for garage-specific or 'any' type
        if garage_type in ['compact', 'medium', 'full-size', 'class 1 truck', 'class 2 truck']:
            # Check if specific type garage is available
            if garage_slots.loc[start_time:end_time, garage_type].eq('Available').all():
                selected_garage = garage_type
                is_booked = True
            else:
                # Find an available 'Any' garage
                available_any_garages = [col for col in garage_slots.columns if 'Any ' in col]
                for any_garage in available_any_garages:
                    if garage_slots.loc[start_time:end_time, any_garage].eq('Available').all():
                        selected_garage = any_garage
                        is_booked = True
                        break

        # Mark the time slot as 'Not Available' and update 'isAccepted'
        if is_booked:
            garage_slots.loc[start_time:end_time, selected_garage] = 'Not Available' + ' ' + row['Type']
            df.at[index, 'isAccepted'] = True
            
    df['Revenue'] = df.apply(calculateRevenue, axis=1)

    return garage_slots


# In[34]:


def selectGarageDateDF(df,selectDay):
    selectDayDF = parseAndSortDataFrame(df, selectDay)
    placeholder_date = selectDayDF['Reservation Date'].iloc[0]
    garageSlots = create_schedule(placeholder_date)
  ##  newGarageSlots = book_reservations_from_df(selectDayDF, garageSlots)
    finalGarageSlots = generateAvailableSlots(selectDayDF, garageSlots)
    return finalGarageSlots


import matplotlib.pyplot as plt
import matplotlib.dates as mdates



def createPlot(df, selectDay):
    # Convert the time index to datetime
    df.index = pd.to_datetime(df.index)

    # Define color mapping for car types
    color_map = {
        'compact': 'red',
        'medium': 'blue',
        'full-size': 'yellow',
        'class 1 truck': 'green',
        'class 2 truck': 'purple'
    }

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Filter the dataframe to select data for the given day
    df_selectDay = df[df['Reservation Date'] == selectDay]

    # Iterate through each row in the dataframe
    for _, row in df_selectDay.iterrows():
        reservation_time = row.name  # Get the reservation time from the index
        any_occupancy = {}  # Dictionary to store occupancy of 'Any' garages
        
        # Iterate through each garage type in the row
        for garage_type in df.columns:
            if 'Any' in garage_type:
                # If it's an 'Any' garage, check if it's occupied
                if row[garage_type] != 'Available':
                    # Determine the color based on the car type
                    car_type = row[garage_type].split()[-1]  # Extract the car type from the occupancy
                    color = color_map.get(car_type, 'white')  # Default to 'white' if not found in color_map
                    any_occupancy[garage_type] = color  # Store the color in the dictionary
        
        # Plot bars for 'Any' garages with labels
        for garage_type, color in any_occupancy.items():
            ax.bar(reservation_time, 1, bottom=0, width=pd.Timedelta(minutes=1), color=color, label=f'{garage_type} ({car_type})')

    # Set x-axis limits to represent 7am to 7pm
    date_str = selectDay
    date = pd.to_datetime(date_str).date()
    ax.set_xlim(pd.Timestamp(f'{date} 07:00:00'), pd.Timestamp(f'{date} 19:00:00'))

    # Format x-axis labels
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set y-axis labels and title
    ax.set_yticks([])
    ax.set_ylabel("Garage Types")
    ax.set_title("Garage Occupancy by Car Type")

    # Add a legend
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


# In[38]:


def createPlot(df, selectDay):
    # Convert the time index to datetime
    df.index = pd.to_datetime(df.index)

    # Define color mapping for car types
    color_map = {
        'compact': 'red',
        'medium': 'blue',
        'full-size': 'yellow',
        'class 1 truck': 'green',
        'class 2 truck': 'purple'
    }

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Filter the dataframe to select data for the given day
    df_selectDay = df[df.index.date == pd.to_datetime(selectDay).date()]

    # Extract unique car types for legend
    unique_car_types = set()
    
    # Iterate through each row in the dataframe
    for _, row in df_selectDay.iterrows():
        reservation_time = row.name  # Get the reservation time from the index
        
        # Iterate through each garage type in the row
        for garage_type, occupancy in row.iteritems():
            if occupancy != 'Available':
                # Determine the color based on the car type
                car_type = occupancy.split()[-1]  # Extract the car type from the occupancy
                color = color_map.get(car_type, 'white')  # Default to 'white' if not found in color_map
                
                # Plot a bar for the garage type with the determined color
                ax.bar(reservation_time.strftime("%H:%M"), 1, bottom=0, width=pd.Timedelta(minutes=1), color=color, label=f'{garage_type} ({car_type})')
                
                # Add car type to unique_car_types
                unique_car_types.add(car_type)

    # Print information for debugging (outside of the loop)
    print(f"Unique Car Types: {unique_car_types}")

    # Set x-axis limits to represent 7am to 7pm
    date_str = selectDay
    date = pd.to_datetime(date_str).date()
    ax.set_xlim(pd.Timestamp(f'{date} 07:00:00'), pd.Timestamp(f'{date} 19:00:00'))

    # Format x-axis labels
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set y-axis labels and title
    ax.set_yticks([])
    ax.set_ylabel("Garage Types")
    ax.set_title("Garage Occupancy by Car Type")

    # Create a legend using unique car types
    legend_labels = [f'{car_type}' for car_type in unique_car_types]
    ax.legend(labels=legend_labels, loc='upper right')

    # Show the plot
    plt.tight_layout()
    plt.show()


# In[39]:


def createPlot(df, selectDay):
    # Convert the time index to datetime
    df.index = pd.to_datetime(df.index)

    # Define color mapping for car types
    color_map = {
        'compact': 'red',
        'medium': 'blue',
        'full-size': 'yellow',
        'class 1 truck': 'green',
        'class 2 truck': 'purple'
    }

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Filter the dataframe to select data for the given day
    df_selectDay = df[df.index.date == pd.to_datetime(selectDay).date()]

    # Extract unique car types for legend
    unique_car_types = set()
    
    # Iterate through each row in the dataframe
    for _, row in df_selectDay.iterrows():
        reservation_time = row.name  # Get the reservation time from the index
        
        # Iterate through each garage type in the row
        for garage_type, occupancy in row.iteritems():
            if occupancy != 'Available':
                # Split the occupancy string into parts
                parts = occupancy.split()
                if len(parts) >= 3:
                    car_type = parts[-2]  # Extract the car type from the occupancy
                    color = color_map.get(car_type, 'white')  # Default to 'white' if not found in color_map
                    
                    # Plot a bar for the garage type with the determined color
                    ax.bar(reservation_time.strftime("%H:%M"), 1, bottom=0, width=pd.Timedelta(minutes=1), color=color, label=f'{garage_type} ({car_type})')
                    
                    # Add car type to unique_car_types
                    unique_car_types.add(car_type)

    # Print information for debugging (outside of the loop)
    print(f"Unique Car Types: {unique_car_types}")

    # Set x-axis limits to represent 7am to 7pm
    date_str = selectDay
    date = pd.to_datetime(date_str).date()
    ax.set_xlim(pd.Timestamp(f'{date} 07:00:00'), pd.Timestamp(f'{date} 19:00:00'))

    # Format x-axis labels
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set y-axis labels and title
    ax.set_yticks([])
    ax.set_ylabel("Garage Types")
    ax.set_title("Garage Occupancy by Car Type")

    # Create a legend using unique car types
    legend_labels = [f'{car_type}' for car_type in unique_car_types]
    ax.legend(labels=legend_labels, loc='upper right')

    # Show the plot
    plt.tight_layout()
    plt.show()



def createHistogramPlot(df, selectDay):
    # Define color mapping for car types
    color_map = {
        'compact': 'red',
        'medium': 'blue',
        'full-size': 'yellow',
        'class 1 truck': 'green',
        'class 2 truck': 'purple',
        'Any': 'grey'  # Color for 'Any' type garages
    }

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Filter the dataframe to select data for the given day
    df_selectDay = df[df.index.date == pd.to_datetime(selectDay).date()]

    # Garage types
    garage_types = df.columns

    # Mapping each garage to a y-axis value
    y_values = {garage: i for i, garage in enumerate(garage_types)}

    # Iterate through each row in the dataframe
    for _, row in df_selectDay.iterrows():
        reservation_time = row.name  # Get the reservation time from the index

        # Iterate through each garage type in the row
        for garage_type, occupancy in row.iteritems():
            if occupancy != 'Available':
                # Split the occupancy string into parts
                car_type= occupancy[-1]
                color = color_map.get(car_type, 'white')  # Default to 'white' if not found in color_map
                
                # Plot a bar for the garage type with the determined color
                ax.bar(reservation_time, 0.8, bottom=y_values[garage_type], color=color, align='center')

    # Set the y-axis to show garage types
    ax.set_yticks(range(len(garage_types)))
    ax.set_yticklabels(garage_types)

    # Set x-axis limits to represent 7am to 7pm
    date_str = selectDay
    date = pd.to_datetime(date_str).date()
    ax.set_xlim(pd.Timestamp(f'{date} 07:00:00'), pd.Timestamp(f'{date} 19:00:00'))

    # Format x-axis labels
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))  # Use a 5-minute interval for clarity
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Set axis labels and title
    ax.set_xlabel("Time")
    ax.set_ylabel("Garage Types")
    ax.set_title("Garage Occupancy by Car Type")

    # Create a legend using the color map
    legend_labels = [f'{car_type} ({color})' for car_type, color in color_map.items()]
    ax.legend(labels=legend_labels, loc='upper right', title="Car Types")

    # Show the plot
    plt.tight_layout()
    plt.show()




# createPlot(sap_dataset,'2022-11-01')




# def createHistogramPlotV2(df, selectDay):
#     df =selectGarageDateDF(df,selectDay)
#     # Define color mapping for car types
#     color_map = {
#         'compact': 'red',
#         'medium': 'blue',
#         'full-size': 'yellow',
#         'class 1 truck': 'green',
#         'class 2 truck': 'purple',
#         'Any': 'grey'  # Color for 'Any' type garages
#     }

#     # Create a figure and axis
#     fig, ax = plt.subplots(figsize=(12, 8))

#     # Filter the dataframe to select data for the given day
#     df_selectDay = df[df.index.date == pd.to_datetime(selectDay).date()]

#     # Garage types
#     garage_types = df.columns

#     # Mapping each garage to a y-axis value
#     y_values = {garage: i for i, garage in enumerate(garage_types)}

#     # Iterate through each row in the dataframe
#     for garage_type, occupancy in row.iteritems():
#             if occupancy != 'Available':
#                 # Split the occupancy string into parts
#                 parts = occupancy.split()
#                 car_type = parts[-2] if len(parts) >= 3 else 'Any'
#                 color = color_map.get(car_type, 'white')  # Default to 'white' if not found in color_map
                
#                 # Plot a bar for the garage type with the determined color
#                 ax.bar(reservation_time, 0.8, bottom=y_values[garage_type], color=color, align='center')


#     # Set the y-axis to show garage types
#     ax.set_yticks(range(len(garage_types)))
#     ax.set_yticklabels(garage_types)

#     # Set x-axis limits to represent 7am to 7pm
#     date_str = selectDay
#     date = pd.to_datetime(date_str).date()
#     ax.set_xlim(pd.Timestamp(f'{date} 07:00:00'), pd.Timestamp(f'{date} 19:00:00'))

#     # Format x-axis labels to display every 30 minutes
#     ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
#     ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45)

#     # Set axis labels and title
#     ax.set_xlabel("Time")
#     ax.set_ylabel("Garage Types")
#     ax.set_title("Garage Occupancy by Car Type")

#     # Create a legend using the color map
#     legend_labels = [f'{car_type} ({color})' for car_type, color in color_map.items()]
#     ax.legend(labels=legend_labels, loc='upper right', title="Car Types")

#     # Show the plot
#     plt.tight_layout()
#     plt.show()


# # In[43]:


# createHistogramPlotV2(sap_dataset,'2022-11-01')


if __name__ == "__main__":
    list_of_dict = turn_to_dict('firebase/functions/datafile.csv')
    print(list_of_dict)
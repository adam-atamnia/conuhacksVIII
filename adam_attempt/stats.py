from ipynb.fs.full.Hackathon2024 import *
import pandas as pd

column_names = ["Book time", "Reservation", "Type"]

csv_file_path = './datafile.csv'
df = pd.read_csv(csv_file_path, names = column_names)

full_data_set = createFullDatasetFullTime(df)
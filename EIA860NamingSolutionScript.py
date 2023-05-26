#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import datetime 
import zipfile
import pandas as pd 

def get_latest_modified(path):
    """
    This function takes the path of a .zip file or a directory, and returns the date of the most
    recently modified .xlsx file contained within the .zip file or the directory.
    """
    latest_date = None

    # Check if the path is a directory
    if os.path.isdir(path):
        # Get list of Excel files in the directory
        excel_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.xlsx')]

        # Loop through each Excel file
        for excel_file in excel_files:
            # Get the last modified date of the file
            last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(excel_file))
            # Update the latest_date if it's either the first file or a more recent file
            if latest_date is None or last_modified_date > latest_date:
                latest_date = last_modified_date

    else:
        # Assume the path is a zip file
        with zipfile.ZipFile(path, 'r') as zip_file:
            # Loop over all files in the .zip file
            for file in zip_file.namelist():
                if file.endswith('.xlsx'):
                    # Get the last modified date of the file
                    info = zip_file.getinfo(file)
                    last_modified_date = datetime.datetime(*info.date_time)
                    # Update the latest_date if it's either the first file or a more recent file
                    if latest_date is None or last_modified_date > latest_date:
                        latest_date = last_modified_date

    return latest_date





def check_first_row_length(path):
    """
    This function takes the path of a .zip file or a regular directory, checks each .xlsx file contained
    within, and if any first row of these .xlsx files contains more than 40 characters, it prints 1.
    If none of the .xlsx files' first row contain more than 40 characters, it prints 0.
    """

    # Check if the path is a directory
    if os.path.isdir(path):
        # Get list of Excel files in the directory
        excel_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.xlsx')]
    else:
        # Assume the path is a zip file
        with zipfile.ZipFile(path, "r") as zip_file:
            # Get the list of Excel files in the zip file
            excel_files = [file for file in zip_file.namelist() if file.endswith('.xlsx')]

    # Check if any Excel files were found
    if not excel_files:
        print("No Excel files found.")
        return

    # Loop through each Excel file
    for excel_file in excel_files:
        # Check if the file is from a zip file
        if path.endswith('.zip'):
            # Open the Excel file from the zip file
            with zipfile.ZipFile(path, 'r').open(excel_file) as file:
                df = pd.read_excel(file)
        else:
            # Open the Excel file from the directory
            df = pd.read_excel(excel_file)

        # Get the values from the first row
        first_row_values = df.iloc[0].values

        # Check if the first row has more than 40 characters
        if any(len(str(value)) > 40 for value in first_row_values):
            print("1")
            return

    print("0")

# Example usage
zip_file_path = "eia860a_er.zip"
#zip_file_path = "eia8602021.zip"
check_first_row_length(zip_file_path)
latest_date = get_latest_modified(zip_file_path)
print(f"The latest date last modified in the zip file is: {latest_date}") 


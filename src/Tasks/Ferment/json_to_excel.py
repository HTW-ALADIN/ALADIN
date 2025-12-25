import os
import pandas as pd

def json_to_excel(json_file, excel_filename='output.xlsx'):
    
    
    # Get the default download folder based on the operating system
    if os.name == 'nt':  # Windows
        download_folder = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:  # Mac/Linux
        download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Load the JSON file into a DataFrame
    df = pd.read_json(json_file)

    # Set the path for the Excel file
    excel_file = os.path.join(download_folder, excel_filename)

    # Save the DataFrame as an Excel file
    df.to_excel(excel_file, index=False, engine='openpyxl')

    # Return the full path to the Excel file
    return excel_file

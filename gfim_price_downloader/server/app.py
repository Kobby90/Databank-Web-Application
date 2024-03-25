from flask import Flask, render_template, request
from flask_cors import CORS  # Import CORS from Flask-CORS
import os
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_data_from_excel(file_path, isins):
    try:
        # Extract date from the file name
        file_name = os.path.basename(file_path)
        date = file_name.split('TRADING REPORT FOR GFIM-')[1][:8]

        # Load the Excel file
        df = pd.read_excel(file_path, sheet_name='NEW GOG NOTES AND BONDS ', header=3)

        # Filter the DataFrame based on column numbers
        column_d = 3  # Column D (ISIN)
        column_f = 5  # Column F (CLOSING YIELD)
        column_g = 6  # Column G (END OF DAY CLOSING PRICE)

        # Filter the DataFrame
        filtered_df = df.iloc[:, [column_d, column_f, column_g]]

        # Rename columns
        filtered_df.columns = ['ISIN','CLOSING YIELD','END OF DAY CLOSING PRICE']

        # Filter rows based on ISIN values from user input
        filtered_df = filtered_df[filtered_df['ISIN'].isin(isins)]

        # Convert date column format from "ddmmyyyy" to "mm/dd/yyyy"
        date_formatted = datetime.strptime(date, '%d%m%Y').strftime('%m/%d/%Y')
        filtered_df['Date'] = date_formatted

        return filtered_df
    except ValueError:
        print(f"Worksheet named 'NEW GOG NOTES AND BONDS ' not found in file: {file_path}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        # Retrieve form data
        data = request.json
        start_date = data['startDate']
        end_date = data['endDate']
        isins = data['isins']
        
        # Define folder containing Excel files
        folder_path = "DATA"

        # Initialize an empty DataFrame to store all data
        combined_df = pd.DataFrame()

        # Iterate through dates from start_date to end_date
        current_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        while current_date <= end_date:
            # Generate file name based on the current date
            file_name = 'TRADING REPORT FOR GFIM-' + current_date.strftime('%d%m%Y') + '.xlsx'
            file_path = os.path.join(folder_path, file_name)

            # Check if the file exists
            if os.path.isfile(file_path):
                # Extract data from the file
                df = extract_data_from_excel(file_path, isins)
                if df is not None:
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
            else:
                # Check if the current day is a weekend
                if current_date.weekday() == 5 or current_date.weekday() == 6:  # Saturday or Sunday
                    print(f"File not found: {file_path}. It's a Weekend.")
                else:
                    print(f"File not found: {file_path}")
            
            # Move to the next date
            current_date += timedelta(days=1)

        # Export the combined DataFrame to Excel
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_file_path = os.path.join(output_folder, 'historical_gfim.xlsx')
        combined_df.to_excel(output_file_path, index=False)
        
        return "Data processing completed successfully!"

if __name__ == '__main__':
    app.run(debug=True)

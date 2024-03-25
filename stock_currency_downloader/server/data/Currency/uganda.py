# uganda.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from datetime import datetime


def fetch_exchange_rates():
    # URL of the website
    url = "https://www.bou.or.ug/bouwebsite/BOU-HOME/"
    
    countryName = "uganda"
    current_Date = datetime.now().strftime("%Y-%m-%d")
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with class "myTable"
        exchange_rate_table = soup.find('table', class_='myTable')

        table_title = "Unganda Exchange Rate"

        # Extract and store the data in a list of lists
        data = []
        if exchange_rate_table:
            # Find all table rows within the table body
            rows = exchange_rate_table.find_all('tr')

            # Skip the first row as it contains column headers
            for row in rows[1:]:
                # Find all table cells (columns) within the row
                columns = row.find_all('td')

                # Extract and store the text content of each column
                row_data = [column.text.strip() for column in columns]

                # Append the row data to the list
                data.append(row_data)

            # Create a DataFrame from the list of lists
            df = pd.DataFrame(data, columns=["Currency", "Buying", "Selling"])

            # Drop repeating rows
            df = df.drop_duplicates()
            
            output_folder = "output/Currency"
            os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Check for files with the partial filename and remove them
            partial_filename = f"Currency_{countryName}_"
            for filename in os.listdir(output_folder):
                if filename.startswith(partial_filename):
                    os.remove(os.path.join(output_folder, filename))

            # Plot the DataFrame as a table and save it as a PDF
            fig, ax = plt.subplots(figsize=(8, 4))  # Adjust the figure size as needed
            ax.set_title(table_title, fontsize=16)  # Add title to the plot
            ax.axis('tight')
            ax.axis('off')
            ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

            pdf_filename = f"{output_folder}/Currency_{countryName}_{current_Date}.pdf"
            plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')
            plt.close()

            return f"DataFrame saved as {pdf_filename}"
        else:
            return "Table not found on the page."
    else:
        return f"Failed to retrieve the page. Status code: {response.status_code}"

# Call the function
result = fetch_exchange_rates()
print(result)

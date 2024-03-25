# tanzania.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

countryName = "tanzania"
current_Date = datetime.now().strftime("%Y-%m-%d")

def fetch_exchange_rates():
    url = "https://www.bot.go.tz/"
    countryName = "tanzania"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table with the specified class
        table = soup.find('table', class_='table table-sm table-bordered table-hover p-0')

        # Check if the table is found
        if table:
            table_title = "Tanzania Exchange Rate"
            # Find all the rows in the table body
            rows = table.find_all('tr')

            # Initialize empty lists to store data
            currencies = []
            buying_rates = []
            selling_rates = []

            # Loop through rows and extract data
            for row in rows[1:]:  # Skip the header row
                columns = row.find_all('td')
                currency = columns[0].get_text(strip=True)
                buying_rate = columns[1].get_text(strip=True)
                selling_rate = columns[2].get_text(strip=True)

                # Append data to lists
                currencies.append(currency)
                buying_rates.append(buying_rate)
                selling_rates.append(selling_rate)

            # Create a DataFrame
            df = pd.DataFrame({
                'Currency': currencies,
                'Buy': buying_rates,
                'Sell': selling_rates
            })

            output_folder = "output/Currency"
            os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Check for files with the partial filename and remove them
            partial_filename = f"Currency_{countryName}_"
            for filename in os.listdir(output_folder):
                if filename.startswith(partial_filename):
                    os.remove(os.path.join(output_folder, filename))

            # Save the DataFrame as a PDF
            pdf_filename = f"{output_folder}/Currency_{countryName}_{current_Date}.pdf"
            df.to_html(pdf_filename, index=False)

            # Plot the DataFrame as a table with title and save as a PDF
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.axis('off')
            ax.set_title(table_title, fontsize=16)  # Add title to the plot
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            plt.savefig(pdf_filename, format='pdf', bbox_inches='tight')

            return f"DataFrame saved as {pdf_filename}"
        else:
            return "Table not found on the page."
    else:
        return f"Failed to retrieve the page. Status Code: {response.status_code}"

# Call the function
result = fetch_exchange_rates()
print(result)

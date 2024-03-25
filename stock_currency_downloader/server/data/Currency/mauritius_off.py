# mauritius.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
import os

CountryName= "mauritius"
current_Date = datetime.now().strftime("%Y-%m-%d")

def scrape_specific_table(url, table_class):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the specific table by class
        table = soup.find('table', class_=table_class)

        # Check if the table was found
        if table:
            # Assign a fixed title to the DataFrame
            table_title = "Mauritius Rupee Exchange Rate"

            # Extract data from the table
            data = []
            for row in table.find('tbody').find_all('tr'):
                columns = row.find_all('td')
                row_data = [column.get_text(strip=True) for column in columns]
                data.append(row_data)

            # Create a DataFrame with the specified column titles
            df = pd.DataFrame(data, columns=["Currency", "Buy (Notes)", "Sell"])

            return df, table_title
        else:
            print(f"Table with class '{table_class}' not found on the webpage.")
    else:
        print(f"Error accessing the website. Status code: {response.status_code}")

def save_dataframe_to_pdf(dataframe, filename, title):# Save the PDF to a file in the "output" folder
    output_folder = "output/Currency"
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Check for files with the partial filename and remove them
    partial_filename = f"Currency_{CountryName}_"
    for filename in os.listdir(output_folder):
        if filename.startswith(partial_filename):
            os.remove(os.path.join(output_folder, filename))

    # Save the DataFrame as a PDF with the title and without the index
    pdf_filename = f"{output_folder}/Currency_{CountryName}_{current_Date}.pdf"
    with PdfPages(pdf_filename) as pdf:
        ax = plt.subplot(111, frame_on=False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

        # Add title to the table
        plt.title(title, fontsize=14, loc='center', pad=20)

        table = plt.table(cellText=dataframe.values, colLabels=dataframe.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        pdf.savefig()
        plt.close()
    print(f"DataFrame saved as {pdf_filename}")

# Specify the URL of the website and the class of the specific table
website_url = "https://www.bom.mu/"
specific_table_class = "views-table cols-3 table table-hover table-striped"

# Call the function to scrape and create a DataFrame from the specific table
result_df, table_title = scrape_specific_table(website_url, specific_table_class)

# Save the DataFrame as a PDF with the fixed title and without the index
save_dataframe_to_pdf(result_df, "Exchange_Rates", table_title)

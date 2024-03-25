import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

user_date = datetime.now()

# Function to scrape data from the provided URL
def scrape_dse_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with the specified ID
        table = soup.find('div', id='equity-watch').find('table')
        
        # Extract table headers
        headers = [th.text.strip() for th in table.find('thead').find_all('th')]
        
        # Extract table rows
        rows = []
        for tr in table.find('tbody').find_all('tr'):
            row = [td.text.strip() for td in tr.find_all('td')]
            rows.append(row)
        
        # Create a DataFrame from the extracted data
        df = pd.DataFrame(rows, columns=headers)
        
        return df
    else:
        # Print an error message if the request fails
        print("Failed to retrieve data from the URL:", url)
        return None

# URL of the website to scrape
url = "https://www.dse.co.tz/"

# Scrape data from the provided URL
data = scrape_dse_data(url)

# Create the output directory if it doesn't exist
directory = 'output/Stocks'
os.makedirs(directory, exist_ok=True)

# Save DataFrame as PDF using Matplotlib
file_name = f"Stocks_tanzania_{user_date.strftime('%Y-%m-%d')}.pdf"
output_file = os.path.join(directory, file_name)

# Check if any file with the partial name exists and overwrite it
for file_name in os.listdir(directory):
    if file_name.startswith("Stocks_tanzania_"):
        os.remove(os.path.join(directory, file_name))
        print(f"Overwriting existing file {file_name}")
        break  # Assuming only one file needs to be overwritten

with PdfPages(output_file) as pdf:
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('tight')
    ax.axis('off')
    ax.set_title('DSE Market Summary', fontweight ="bold") 
    table = ax.table(cellText=data.values, colLabels=data.columns, cellLoc='left', loc='center', colColours=['#ffffff']*len(data.columns))
    table.auto_set_font_size(False)
    table.set_fontsize(7)  # Adjust font size of column headers
    table.scale(1.2, 1.2)  # Increase cell size
    pdf.savefig()
    plt.close()
    
    
print(f"PDF saved to: {output_file}")

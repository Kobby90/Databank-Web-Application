from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date
import os
import time

# Launch Chrome browser
driver = webdriver.Chrome()

# Open the webpage
url = "https://www.boz.zm/"
driver.get(url)

# Wait for the JavaScript to load the data (you might need to adjust the wait time)
time.sleep(5)

# Extract the HTML content after JavaScript execution
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find the table element
table = soup.find("table",class_="table table-striped", id="hp_key")

if table:
    # Initialize lists to store table data
    headers = []
    data = []

    # Extract table headers
    header_row = table.find("thead").find("tr")
    for th in header_row.find_all("th"):
        headers.append(th.get_text(strip=True))

    # Extract table rows
    for row in table.find("tbody").find_all("tr"):
        row_data = []
        for td in row.find_all("td"):
            row_data.append(td.get_text(strip=True))
        data.append(row_data)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=["Currency","Buying","Selling"])

    print(df)
    
    # Define the path for saving the PDF file
    output_folder = "output/Currency"
    pdf_path = f"{output_folder}/Currency_zambia_{date.today()}.pdf"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(output_folder):
        if filename.startswith("Currency_zambia_"):
            os.remove(os.path.join(output_folder, filename))
            print(f"Overwriting existing file {filename}")
            break  # Assuming only one file needs to be overwritten

    # Save the DataFrame as a PDF file
    # Save the DataFrame as a PDF file
    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(16, 12)) # Increase figure size
        ax.axis('tight')
        ax.axis('off')
        ax.set_title('Average Exchange rates in Zambia', fontweight="bold") # Adjust title padding
        # Calculate column widths based on content
        col_widths = [max(df[col].apply(lambda x: len(str(x))).max(), len(col)) for col in df.columns]

        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(14) # Adjust font size of column headers
        table.scale(1.2, 1.2) # Increase cell size
   
        # Adjust column widths
        for i, width in enumerate(col_widths):
            table.auto_set_column_width(col=i)

        pdf.savefig()
        plt.close()

    print(f"DataFrame saved as PDF: {pdf_path}")
else:
    print("Table not found on the webpage.")


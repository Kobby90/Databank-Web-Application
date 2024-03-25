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
url = "https://www.centralbank.go.ke/forex/"
driver.get(url)

# Wait for the JavaScript to load the data (you might need to adjust the wait time)
time.sleep(5)

# Extract the HTML content after JavaScript execution
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find the specific table by ID
table = soup.find("table", {"id": "table_4"})


# Find the specific table by class
table = soup.find("table", class_="tg")

if table:
    # Initialize lists to store table data
    data = []
    
    # Extract table rows
    for row in table.find_all("tr"):
        row_data = [td.get_text(strip=True) for td in row.find_all("td")]
        data.append(row_data)
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=["Currency", "Exchange Rate"])
    
    # Drop rows with indices 0 and 4
    df = df.drop([0, 4])

    print(df)
    
    # Define the path for saving the PDF file
    output_folder = "output/Currency"
    pdf_path = f"{output_folder}/Currency_kenya_{date.today()}.pdf"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(output_folder):
        if filename.startswith("Currency_kenya_"):
            os.remove(os.path.join(output_folder, filename))
            print(f"Overwriting existing file {filename}")
            break  # Assuming only one file needs to be overwritten

    # Save the DataFrame as a PDF file
    # Save the DataFrame as a PDF file
    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(16, 12)) # Increase figure size
        ax.axis('tight')
        ax.axis('off')
        ax.set_title('Key New CBK Indicative Exchange Rates', fontweight="bold") # Adjust title padding
        # Calculate column widths based on content
        col_widths = [max(df[col].apply(lambda x: len(str(x))).max(), len(col)) for col in df.columns]

        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10) # Adjust font size of column headers
        table.scale(1.2, 1.2) # Increase cell size
   
        # Adjust column widths
        for i, width in enumerate(col_widths):
            table.auto_set_column_width(col=i)

        pdf.savefig()
        plt.close()

    print(f"DataFrame saved as PDF: {pdf_path}")
else:
    print("Table not found on the webpage.")



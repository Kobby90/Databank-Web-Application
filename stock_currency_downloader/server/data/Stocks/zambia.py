import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import os

# Define the base URL
base_url = "https://luse.co.zm/market-data/"

# Define the output folder
output_folder = "output/Stocks"

# Get the current date
current_date = date.today()

# Initialize a variable to store the found link
trade_summary_link = None

# Iterate through dates until finding a valid link
while trade_summary_link is None:
    # Generate the expected link format for the current date
    formatted_date = current_date.strftime("%Y/%m/%d-%B-%Y")
    expected_link = f"https://luse.co.zm/wp-content/uploads/{formatted_date}-Trade-Summary-Report.pdf"

    # Fetch the webpage content
    response = requests.get(base_url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all <a> tags
        links = soup.find_all("a")
        
        # Check each link to see if it matches the expected format
        for link in links:
            href = link.get("href")
            if href and href == expected_link:
                trade_summary_link = href
                break
    
    # Move to the previous date
    current_date -= timedelta(days=1)

# If a link is found, download the PDF file
if trade_summary_link:
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Define the PDF file path
    pdf_path = f"{output_folder}/Stocks_zambia_{date.today()}.pdf"
    
    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(output_folder):
        if filename.startswith("Stocks_zambia_"):
            os.remove(os.path.join(output_folder, filename))
            print(f"Overwriting existing file {filename}")
            break  # Assuming only one file needs to be overwritten
    
    # Download the PDF file
    with open(pdf_path, 'wb') as f:
        response = requests.get(trade_summary_link)
        f.write(response.content)
    
    print(f"Trade Summary Report saved as PDF: {pdf_path}")
else:
    print("Trade Summary Report not found for today or previous dates.")

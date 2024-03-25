import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

def download_pdf():
    # Send a GET request to the URL
    url = "https://mse.co.mw/public/market/reports"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all rows in the table
        rows = soup.select('table.table tbody tr')
        
        # Get today's date in the format "dd mm yyyy"
        today_date = datetime.now().strftime('%d %B %Y').lower()

        # Search for the row that matches today's date
        pdf_link = None
        for row in rows:
            date_published = row.select_one('td:nth-child(3)').text.strip().lower()
            if today_date in date_published:
                pdf_link = row.select_one('a')['href']
                break

        # If today's date not found, find the closest previous date
        if not pdf_link:
            for row in rows:
                date_published = row.select_one('td:nth-child(3)').text.strip().lower()
                date_published = datetime.strptime(date_published, '%d %B %Y').date()
                if date_published < datetime.now().date():
                    pdf_link = row.select_one('a')['href']
                    break

        if pdf_link:
            # Construct the filename with the current date
            filename = f"Stocks_malawi_{datetime.now().strftime('%Y-%m-%d')}.pdf"
            complete_file_path = os.path.join('output/Stocks', filename)

            # Ensure the directory exists
            directory = os.path.dirname(complete_file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Check if any file with the partial name exists and overwrite it
            for filename in os.listdir(directory):
                if filename.startswith("Stocks_malawi_"):
                    os.remove(os.path.join(directory, filename))
                    print(f"Overwriting existing file {filename}")
                    break  # Assuming only one file needs to be overwritten

            # Send a GET request to download the PDF
            pdf_response = requests.get(pdf_link)

            # Check if the request was successful (status code 200)
            if pdf_response.status_code == 200:
                # Save the PDF content to the specified path
                with open(complete_file_path, "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"PDF downloaded successfully as {complete_file_path}")
            else:
                print(f"Failed to download PDF. Status code: {pdf_response.status_code}")
        else:
            print("No PDF found for today's date or the nearest previous date.")
    else:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    download_pdf()

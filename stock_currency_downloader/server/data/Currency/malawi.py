# malawi.py

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from fpdf import FPDF
from datetime import datetime
import  os

def fetch_exchange_rates():
    url = "https://www.rbm.mw/"
    countryName = "malawi"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Initialize data list to store exchange rate data
        data = []

        # Find the div containing the exchange rate data
        exchange_rate_div = soup.find("div", class_="home-rates")

        if exchange_rate_div:
            # Extract the date
            date_element = exchange_rate_div.find("span", id="exhangeRateDate")
            date = date_element.text.strip()

            # Find the exchange rate table
            exchange_rate_table = exchange_rate_div.find("table", id="exchange-rates_home")

            if exchange_rate_table:
                # Extract table data
                rows = exchange_rate_table.find_all("tr")
                currencies = {}

                for row in rows[1:]:  # Skip the header row
                    columns = row.find_all("td")
                    if len(columns) >= 3:
                        currency = columns[0].text.strip()
                        buying = columns[1].text.strip()
                        selling = columns[2].text.strip()

                        currencies[currency] = (buying, selling)

                data.append([date, currencies])

                # Create a PDF document
                class PDF(FPDF):
                    def header(self):
                        self.set_font("Arial", "B", 12)
                        self.cell(0, 10, f"Exchange Rate Data for {countryName}", align="C")
                        self.ln(10)

                    def footer(self):
                        self.set_y(-15)
                        self.set_font("Arial", "I", 8)
                        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Create a table and add data to the PDF
                table_data = [["Currency", "Buying", "Selling"]]
                for currency, (buying, selling) in currencies.items():
                    table_data.append([currency, buying, selling])

                pdf.ln(10)
                pdf.multi_cell(0, 10, tabulate(table_data, headers="firstrow", tablefmt="grid"))

                current_Date = datetime.now().strftime("%Y-%m-%d")
                
                # Save the PDF to a file in the "output" folder
                output_folder = "output/Currency"
                os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

                # Check for files with the partial filename and remove them
                partial_filename = f"Currency_{countryName}_"
                for filename in os.listdir(output_folder):
                    if filename.startswith(partial_filename):
                        os.remove(os.path.join(output_folder, filename))

                 # Save the PDF to a file with countryName
                pdf_filename = f"{output_folder}/Currency_{countryName}_{current_Date}.pdf"
                pdf.output(pdf_filename)

                return f"Exchange rate data saved as {pdf_filename}"
            else:
                return "Exchange Rate Table Not Found on the Page"
        else:
            return "Exchange Rate Data Not Found on the Page"
    else:
        return "Error accessing the website. Please try again later."
# Call the function
result = fetch_exchange_rates()
print(result)

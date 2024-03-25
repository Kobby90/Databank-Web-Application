import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from fpdf import FPDF
import os
from datetime import datetime

def fetch_exchange_rates():
    url = "https://www.bceao.int/en/content/main-indicators-and-interest-rates"
    countryName = "cote_divoire"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Initialize data list to store exchange rate data
        data = []

        # Find the div containing the exchange rate data
        exchange_rate_div = soup.find("div", class_="blcCart1 blcDevise wow fadeInLeft contextual-region")

        if exchange_rate_div:
            # Extract the date
            date_element = exchange_rate_div.find("h2")
            date = date_element.text.strip()

            # Find the exchange rate table
            exchange_rate_table = exchange_rate_div.find("table")

            if exchange_rate_table:
                # Extract table data
                rows = exchange_rate_table.find_all("tr")
                currencies = {}

                for row in rows[1:]: # Skip the header row
                    columns = row.find_all("td")
                    if len(columns) == 3:
                        currency = columns[0].text.strip()
                        purchase = columns[1].text.strip()
                        sale = columns[2].text.strip()

                        currencies[currency] = (purchase, sale)

                data.append([date, currencies])
                
                            # Format date to a more readable format
            
                formatted_dt = datetime.today().strftime("%Y-%m-%d")

                # Ensure the directory exists
                directory = "output/Currency"
                if not os.path.exists(directory):
                    os.makedirs(directory)

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
                table_data = [["Currency", "Purchase", "Sale"]]
                for currency, (purchase, sale) in currencies.items():
                    table_data.append([currency, purchase, sale])

                pdf.ln(10)
                pdf.multi_cell(0, 10, tabulate(table_data, headers="firstrow", tablefmt="grid"))
                
                partial_filename = f"Currency_{countryName}_"
                for filename in os.listdir(directory):
                    if filename.startswith(partial_filename):
                        os.remove(os.path.join(directory, filename))
                        
                # Save the PDF to a file with countryName inside the "output/Currency" directory
                pdf_filename = f"{directory}/Currency_{countryName}_{formatted_dt}.pdf"
                pdf.output(pdf_filename)

                return f"Exchange rate data saved as {pdf_filename}"
            else:
                return "Exchange Rate Table Not Found on the Page"
        else:
            return "Exchange Rate Data Not Found on the Page"
    else:
        return "Error accessing the website. Please try again later."

# Example usage
if __name__ == "__main__":
    print(fetch_exchange_rates())
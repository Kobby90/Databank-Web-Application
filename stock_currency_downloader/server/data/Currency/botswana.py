# botswana.py

import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from fpdf import FPDF
from datetime import datetime

def fetch_exchange_rates():
    url = "https://www.bankofbotswana.bw/"
    country_name = "botswana"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Initialize data list to store exchange rate data
        data = []

        # Find the div containing the exchange rate data
        exchange_rate_div = soup.find("div", class_="clearfix views-row")

        if exchange_rate_div:
            # Extract the date
            date_element = exchange_rate_div.find("div", class_="views-field-field-exchange-date")
            date = date_element.find("div", class_="field-content").text.strip()

            # Format date to a more readable format
            formatted_date = " ".join(date.split('-'))
            formatted_dt = datetime.today().strftime("%Y-%m-%d")

            # Create a dictionary to map labels to their corresponding classes
            currency_labels = {
                "CNH": "views-label-field-cnh",
                "EUR": "views-label-field-eur",
                "GBP": "views-label-field-gbp",
                "USD": "views-label-field-usd",
                "ZAR": "views-label-field-zar",
                "YEN": "views-label-field-yen"
            }

            currencies = {}

            for label, label_class in currency_labels.items():
                label_element = exchange_rate_div.find("span", class_=label_class)

                if label_element:
                    label = label_element.text.strip()
                    value_element = label_element.find_next("div", class_="field-content")

                    if value_element:
                        # Convert value to float for numerical operations
                        value = float(value_element.text.strip())
                    else:
                        value = "Value Not Found"
                else:
                    label = f"Label for {label} Not Found"
                    value = "Value Not Found"

                currencies[label] = value

            data.append([formatted_date, currencies])

            # Create a PDF document
            class PDF(FPDF):
                def header(self):
                    self.set_font("Arial", "B", 12)
                    self.cell(0, 10, f"Exchange Rate Data for {country_name}", align="C")
                    self.ln(10)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("Arial", "I", 8)
                    self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Create a table and add data to the PDF
            table_data = [["Currency", "Value"]]
            for label, value in currencies.items():
                table_data.append([label, value])

            # Simplify table generation
            pdf.ln(10)
            pdf.multi_cell(0, 10, tabulate(table_data, headers="firstrow", tablefmt="grid"))

            # Save the PDF to a file in the "output" folder
            output_folder = "output/Currency"
            os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

            # Check for files with the partial filename and remove them
            partial_filename = f"Currency_{country_name}_"
            for filename in os.listdir(output_folder):
                if filename.startswith(partial_filename):
                    os.remove(os.path.join(output_folder, filename))

            pdf_filename = f"{output_folder}/Currency_{country_name}_{formatted_dt}.pdf"
            pdf.output(pdf_filename)

            return f"Exchange rate data saved as {pdf_filename}"
        else:
            print("Exchange Rate Data Not Found on the Page")
            return "Exchange Rate Data Not Found on the Page"
    else:
        return "Error accessing the website. Please try again later."

# Call the function
result = fetch_exchange_rates()
print(result)

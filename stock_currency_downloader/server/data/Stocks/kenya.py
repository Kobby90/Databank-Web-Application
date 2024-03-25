import requests
from datetime import datetime, timedelta
import os


def download_pdf():
  # Attempt to download the PDF for today's date
  user_date = datetime.now()
  formatted_date = user_date.strftime("%d-%b-%y").upper()
  month_year = user_date.strftime("%m/%Y")
  pdf_url = f"https://www.nse.co.ke/wp-content/uploads/{formatted_date}.pdf"
  response = requests.get(pdf_url)

  # If the status code is 404, try downloading the PDF for yesterday's date
  if response.status_code == 404:
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%d-%b-%y").upper()
    month_year = yesterday.strftime("%m/%Y")
    pdf_url = f"https://www.nse.co.ke/wp-content/uploads/{formatted_date}.pdf"
    response = requests.get(pdf_url)

  if response.status_code == 200:
    # Ensure the directory exists
    directory = 'output/Stocks'
    if not os.path.exists(directory):
      os.makedirs(directory)

    # Construct the complete file path
    file_name = f"Stocks_kenya_{user_date.strftime('%Y-%m-%d')}.pdf"
    complete_file_path = os.path.join(directory, file_name)

    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(directory):
      if filename.startswith("Stocks_kenya_"):
        os.remove(os.path.join(directory, filename))
        print(f"Overwriting existing file {filename}")
        break  # Assuming only one file needs to be overwritten

    # Save the PDF content to the specified path
    with open(complete_file_path, "wb") as pdf_file:
      pdf_file.write(response.content)
    print(f"PDF downloaded successfully as {complete_file_path}")
  else:
    print(f"Failed to download PDF. Status code: {response.status_code}")


if __name__ == "__main__":
  download_pdf()

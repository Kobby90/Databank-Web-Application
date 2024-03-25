import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

countryName = "nigeria"
current_Date = datetime.now().strftime("%Y-%m-%d")

def fetch_exchange_rates():
    url = "https://www.cbn.gov.ng/Functions/export.asp?tablename=exchange"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open("nigeria_exchange_rates.csv", "w", encoding="utf-8") as file:
            file.write(response.text)
        
        data = pd.read_csv("nigeria_exchange_rates.csv", index_col=False)
        
        if data.empty:
            return "Error: No data available."
        
        data = data.drop(["Rate Year", "Rate Month"], axis=1)
        
        result_messages = []
        
        # Fetch data for today
        target_date = datetime.now().strftime("%m/%d/%Y")
        data_target_date = data[pd.to_datetime(data["Rate Date"], format="%m/%d/%Y") == pd.to_datetime(target_date, format="%m/%d/%Y")]
        
        if not data_target_date.empty:
            result_messages.append(save_data_to_pdf(data_target_date, target_date))
        else:
            result_messages.append(f"No data available for {target_date}")
        
        # Fetch data for yesterday
        target_date = (datetime.now() - timedelta(1)).strftime("%m/%d/%Y")
        data_target_date = data[pd.to_datetime(data["Rate Date"], format="%m/%d/%Y") == pd.to_datetime(target_date, format="%m/%d/%Y")]
        
        if not data_target_date.empty:
            result_messages.append(save_data_to_pdf(data_target_date, target_date))
        else:
            result_messages.append(f"No data available for {target_date}")
        
        # Fetch data for day before yesterday
        target_date = (datetime.now() - timedelta(2)).strftime("%m/%d/%Y")
        data_target_date = data[pd.to_datetime(data["Rate Date"], format="%m/%d/%Y") == pd.to_datetime(target_date, format="%m/%d/%Y")]
        
        if not data_target_date.empty:
            result_messages.append(save_data_to_pdf(data_target_date, target_date))
        else:
            # If no data for day before yesterday, check if one day after yesterday is empty
            target_date = (datetime.now() - timedelta(3)).strftime("%m/%d/%Y")
            data_target_date = data[pd.to_datetime(data["Rate Date"], format="%m/%d/%Y") == pd.to_datetime(target_date, format="%m/%d/%Y")]
            
            if not data_target_date.empty:
                result_messages.append(save_data_to_pdf(data_target_date, target_date))
            else:
                # If no data for two days before yesterday, fetch data for three days before yesterday
                target_date = (datetime.now() - timedelta(4)).strftime("%m/%d/%Y")
                data_target_date = data[pd.to_datetime(data["Rate Date"], format="%m/%d/%Y") == pd.to_datetime(target_date, format="%m/%d/%Y")]
                
                if not data_target_date.empty:
                    result_messages.append(save_data_to_pdf(data_target_date, target_date))
                else:
                    result_messages.append(f"No data available for {target_date}")
        
        return "\n".join(result_messages)
    else:
        return "Error fetching exchange rates data for Nigeria."

def save_data_to_pdf(data, target_date):
    output_folder = "output/Currency"
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Check for files with the partial filename and remove them
    partial_filename = f"Currency_{countryName}_{target_date}"
    for filename in os.listdir(output_folder):
        if filename.startswith(partial_filename):
            os.remove(os.path.join(output_folder, filename))
            
    # Save the DataFrame as a PDF
    pdf_filename = f"{output_folder}/Currency_{countryName}_{current_Date}.pdf"
    with plt.style.context('ggplot'):
        plt.figure(figsize=(10, 6))
        plt.title(f"Exchange Rates for Nigeria ({target_date})", fontsize=16)
        plt.axis('off')
        plt.table(cellText=data.values, colLabels=data.columns, cellLoc='center', loc='center')
        plt.tight_layout()
        plt.savefig(pdf_filename, format='pdf')  # Save as PDF
    
    return f"Exchange rates data for Nigeria fetched, processed, and saved as {pdf_filename}."

# Call the function
result = fetch_exchange_rates()
print(result)

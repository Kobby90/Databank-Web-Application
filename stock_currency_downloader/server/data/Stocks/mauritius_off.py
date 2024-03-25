import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.pipelines.files import FilesPipeline
from datetime import date
import os
import io
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend


class StockExchangeSpider(scrapy.Spider):
  name = 'stock_exchange'
  start_urls = [
      'https://www.stockexchangeofmauritius.com/products-market-data/equities-board/trading-quotes/official'
  ]

  def parse(self, response):
    rows = response.css('.table-cnt .main-table tbody tr')
    data = []

    for row in rows:
      company_name = row.css('th.fixed-side a::text').get()
      currency = row.css('th.fixed-side + th::text').get()
      trend = row.css('.trend span::attr(class)').get().split()[-1]
      last_closing_price = row.css('td:nth-child(4) strong::text').get()
      latest = row.css('td:nth-child(5)::text').get()
      change = row.css('td:nth-child(6)::text').get()
      percent_change = row.css('td:nth-child(7)::text').get()
      volume = row.css('td:nth-child(8)::text').get()
      value = row.css('td:nth-child(9)::text').get()
      closing_vwap = row.css('td:nth-child(10)::text').get()

      data.append({
          'Company Name': company_name,
          'Currency': currency,
          'Trend': trend,
          'Last Closing Price': last_closing_price,
          'Latest': latest,
          'Change': change,
          '% Change': percent_change,
          'Volume': volume,
          'Value': value,
          'Closing VWAP': closing_vwap,
      })

    df = pd.DataFrame(data)
    df = df.drop('Trend', axis=1)
    print(df)

    # Save the DataFrame as a PDF file with increased font size
    pdf_content = io.BytesIO()
    pdf_pages = pdf_backend.PdfPages(pdf_content)
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('tight')
    ax.axis('off')

    # Increase font size
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     cellLoc='left',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)  # Adjust font size of column headers
    table.scale(1.2, 1.2)  # Increase cell size

    pdf_pages.savefig(fig, bbox_inches='tight')
    pdf_pages.close()

    folder_path = 'output/Stocks'

    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Construct the complete file path
    pdf_filename = f'Stocks_mauritius_off_{date.today()}.pdf'
    complete_file_path = os.path.join(folder_path, pdf_filename)

    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(folder_path):
      if filename.startswith("Stocks_mauritius_off_"):
        os.remove(os.path.join(folder_path, filename))
        print(f"Overwriting existing file {filename}")
        break  # Assuming only one file needs to be overwritten

    # Save the PDF content to a file
    with open(complete_file_path, 'wb') as pdf_file:
      pdf_file.write(pdf_content.getvalue())

    # Yield a request to download the file
    yield {'file_urls': [os.path.abspath(complete_file_path)]}


process = CrawlerProcess({
    'ITEM_PIPELINES': {
        'scrapy.pipelines.files.FilesPipeline': 1,
    },
    'FILES_STORE': 'output',  # Set the directory where files will be stored
})

process.crawl(StockExchangeSpider)
process.start()

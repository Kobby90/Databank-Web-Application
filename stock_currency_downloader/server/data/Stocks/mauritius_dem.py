import scrapy
import pandas as pd
import matplotlib.pyplot as plt
from scrapy.crawler import CrawlerProcess
from datetime import date
import os
from matplotlib.backends.backend_pdf import PdfPages


class StockExchangeSpider(scrapy.Spider):
  name = 'stock_exchange'
  start_urls = [
      'https://www.stockexchangeofmauritius.com/products-market-data/equities-board/trading-quotes/dem'
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

    # Save the DataFrame as a PDF file with improved table formatting
    pdf_filename = f'Stocks_mauritius_dem_{date.today()}.pdf'
    complete_file_path = os.path.join('output/Stocks', pdf_filename)

    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(os.path.dirname(complete_file_path)):
      if filename.startswith("Stocks_mauritius_dem_"):
        os.remove(os.path.join(os.path.dirname(complete_file_path), filename))
        print(f"Overwriting existing file {filename}")
        break  # Assuming only one file needs to be overwritten

    with PdfPages(complete_file_path) as pdf:
      fig, ax = plt.subplots(figsize=(14, 10))
      ax.axis('tight')
      ax.axis('off')

      table_data = [df.columns] + df.values.tolist()
      table=ax.table(cellText=table_data,
               colLabels=None,
               cellLoc='left',
               loc='left'
               )
      table.auto_set_font_size(False)
      table.set_fontsize(9)  # Adjust font size of column headers
      table.scale(1.2, 1.2)  # Increase cell size

      pdf.savefig(fig, bbox_inches='tight')
    yield {'file_urls': [os.path.abspath(complete_file_path)]}


# Set up the Scrapy process with the appropriate settings
process = CrawlerProcess({
    'ITEM_PIPELINES': {
        'scrapy.pipelines.files.FilesPipeline': 1,
    },
    'FILES_STORE': 'output',  # Set the directory where files will be stored
    'LOG_LEVEL': 'INFO',  # Set the logging level to INFO for better visibility
})

# Start the Scrapy process with the defined spider
process.crawl(StockExchangeSpider)
process.start()

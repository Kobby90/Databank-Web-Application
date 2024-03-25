import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from datetime import date
import os


class StockSpider(scrapy.Spider):
  name = 'stock_spider'
  start_urls = ['https://www.brvm.org/fr/cours-actions/0']

  def parse(self, response):
    # Extracting data from the table
    rows = response.xpath(
        '//table[@class="table table-hover table-striped sticky-enabled"]/tbody/tr'
    )

    data = []
    for row in rows:
      symbol = row.xpath('.//td[1]/text()').get()
      name = row.xpath('.//td[2]/text()').get()
      volume = row.xpath('.//td[3]/text()').get()
      monitoring_course = row.xpath('.//td[4]/text()').get()
      opening_price = row.xpath('.//td[5]/text()').get()
      closing_price = row.xpath('.//td[6]/text()').get()
      variation_percent = row.xpath('.//td[7]/span/text()').get()

      data.append({
          'Symbol': symbol,
          'Name': name,
          'Volume': volume,
          'Monitoring course (FCFA)': monitoring_course,
          'Opening Price (FCFA)': opening_price,
          'Closing Price (FCFA)': closing_price,
          'Variation Percent': variation_percent,
      })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Save the DataFrame as a PDF file with increased font size
    output_folder = 'output/Stocks'
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)

    pdf_file_path = os.path.join(output_folder,
                                 f'Stocks_cote_divoire_{date.today()}.pdf')
    # Check if any file with the partial name exists and overwrite it
    for filename in os.listdir(output_folder):
      if filename.startswith("Stocks_cote_divoire_"):
        os.remove(os.path.join(output_folder, filename))
        print(f"Overwriting existing file {filename}")
        break  # Assuming only one file needs to be overwritten

    pdf_pages = pdf_backend.PdfPages(pdf_file_path)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')

    # Increase font size
    table = ax.table(cellText=df.values,
                     colLabels=df.columns,
                     cellLoc='center',
                     loc='center',
                     fontsize=14)

    # Adjust column widths to fit the content
    for i, key in enumerate(df.columns):
      col_width = max([len(str(value)) for value in df[key]] + [len(str(key))])
      table.auto_set_column_width([i])
      table.auto_set_font_size(False)
      table.set_fontsize(10)

    pdf_pages.savefig(fig, bbox_inches='tight')
    pdf_pages.close()

    print(f'DataFrame saved as {pdf_file_path}')


# Run the spider
process = CrawlerProcess()
process.crawl(StockSpider)
process.start()

import subprocess
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from io import BytesIO

def generate_pdf(program_path):
    try:
        # Run the Python program using subprocess and capture the output
        process_output = subprocess.check_output(['python', program_path], stderr=subprocess.STDOUT, text=True)
        
        # Assuming the output is a DataFrame in string format
        df_string = process_output.strip()

        # Convert the DataFrame string to a DataFrame (this part may need adjustments based on the actual output format)
        # df = pd.read_csv(StringIO(df_string))

        # For demonstration purposes, let's just use a simple example
        # You should modify this part according to the actual output and PDF generation logic in your .py files
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, df_string, ha='center', va='center', fontdict={'size': 12})
        pdf_file_content = BytesIO()
        pdf_pages = pdf_backend.PdfPages(pdf_file_content)
        pdf_pages.savefig(fig, bbox_inches='tight')
        pdf_pages.close()

        pdf_file_content.seek(0)
        return pdf_file_content.read()

    except subprocess.CalledProcessError as e:
        raise Exception(f'Error running {program_path}: {e.output}')

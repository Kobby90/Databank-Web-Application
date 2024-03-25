from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import tempfile
from datetime import date
import io
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend

app = Flask(__name__)
CORS(app, resources={r"/*": {
    "origins": "*"
}})  # Allow all origins for simplicity


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/fetch_data', methods=['POST'])
def fetch_data():
  try:
    data_type = request.form['dataType']
    country = request.form['countrySelect']

    # Define the directory based on DataType
    if data_type == 'Currency' or data_type == 'Stocks':
      directory = os.path.join('data', data_type)
    else:
      return jsonify({'error': 'Invalid DataType'})

    print(f"Received data: {data_type}, {country}")
    print(f"Directory: {directory}")  # Print the directory

    # Build the path to the Python program
    program_path = os.path.join(directory, f"{country}.py")

    print(f"Program path: {program_path}")

    # Check if the program file exists
    if not os.path.exists(program_path):
      return jsonify({
          'error': f"No program found for {data_type} in {country}",
          'directory': directory.replace(os.path.sep, '/')
      })

    # Create a temporary file to store the output
    with tempfile.NamedTemporaryFile(mode='w+', delete=False,
         suffix='.pdf') as temp_output:
      try:
        # Run the Python program using subprocess and redirect output to the temporary file
        subprocess.run(['python', program_path],
          stdout=temp_output,
          stderr=subprocess.STDOUT,
          check=True)

        # Read the output from the temporary file
        temp_output.seek(0)
        output = temp_output.read()

        print(f"Output of {program_path}:\n{output}")

        # If the output is a PDF content, send it as a downloadable file
        if output.startswith('%PDF'):
          return send_from_directory(
              directory,
              temp_output.name,
              as_attachment=True,
              download_name=f'{data_type}_{country}_{date.today()}.pdf')

        return jsonify({'message': 'Data fetched successfully'})

      except subprocess.CalledProcessError as e:
        # If an error occurs, read the output and return the error message
        temp_output.seek(0)
        output = temp_output.read()
        return jsonify({'error': f'Error running {program_path}: {output}'})

  except Exception as e:
    return jsonify({'error': f'Error: {str(e)}'})


if __name__ == '__main__':
  app.run(debug=True)

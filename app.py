from flask import Flask, render_template, request
import io
import csv
import requests 
# Import the functions from your original script


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        file = request.files['csv_file']
        choice = request.form['choice']
        url = request.form['url']

        if file.filename == '' or not file.filename.endswith('.csv'):
            return "Please upload a valid CSV file."

        try:
            file_content = file.read()  # Read the file content as bytes
            process_csv_file(file_content, choice, url)  # Pass the file content to the function
            return "Hall tickets downloaded successfully!"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return redirect(url_for('home'))  # Redirect to the home page if accessed via GET


def process_csv_file(file_content, choice, url):
    if choice == "1":
        data_field = "aadar"
    elif choice == "2":
        data_field = "Date Of Birth"
    else:
        raise ValueError("Invalid choice. Please choose 1 for Aadhaar number or 2 for Date of Birth.")

    # Use the io module to convert file content (bytes) to a file-like object
    csvfile = io.StringIO(file_content.decode('utf-8'))
    reader = csv.DictReader(csvfile)
    for row in reader:
        roll_number = row['Register No']
        data = row[data_field]
        download_hall_ticket(roll_number, data, url)

def download_hall_ticket(roll_number, date_of_birth, url):

    url = url + 'hallticket.php'
    if len(date_of_birth)==12:
        payload = {
            'regno': roll_number,
            'aadar': date_of_birth
        }
    else:
        payload = {
            'regno': roll_number,
            'dob': date_of_birth
        }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        # Check if the hall ticket is available in the response content
        if roll_number in response.text:
            with open(f'hall_ticket_{roll_number}.html', 'w') as f:
                f.write(response.text)
            print(f"Hall ticket for Roll Number {roll_number} downloaded successfully.")
        else:
            print(f"Hall ticket not found for Roll Number {roll_number}.")
    else:
        print(f"Failed to access hall ticket website for Roll Number {roll_number}.")

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")


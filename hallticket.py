import csv
import requests
from bs4 import BeautifulSoup

def download_hall_ticket(roll_number, date_of_birth):
    url = 'http://www.exam.kannuruniversity.ac.in/IntegratedPG/HALL_TICKET/intpg4semreg_april_2023/hallticket.php'
    
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

def main():
    file_name = input("Enter the File name: ")
    print("1 for aadar \n2 for DOB")
    choice = input("Enter aadar or DOB:")
    try:
        if choice=="1":
            with open(file_name, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    roll_number = row['Register No']
                    aadar = row['aadar']
                    download_hall_ticket(roll_number, aadar)
        else:
            with open(file_name, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    roll_number = row['Register No']
                    date_of_birth = row['Date Of Birth']
                    download_hall_ticket(roll_number, date_of_birth)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except KeyError:
        print("Error: The specified row does not exist in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
if __name__ == '__main__':
    main()

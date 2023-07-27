import csv
import requests
from bs4 import BeautifulSoup

def download_hall_ticket(roll_number, date_of_birth):
    url = 'http://www.exam.kannuruniversity.ac.in/IntegratedPG/HALL_TICKET/intpg4semreg_april_2023/hallticket.php'
    
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
    with open('Hall_Ticket.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            roll_number = row['Register No']
            date_of_birth = row['Date Of Birth']
            download_hall_ticket(roll_number, date_of_birth)

if __name__ == '__main__':
    main()

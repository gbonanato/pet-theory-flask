import csv
import sys
from faker import Faker
from google.cloud import logging
from flask import Flask, request

app = Flask(__name__)
fake = Faker()

# Configuração do Logging
log_name = "pet-theory-logs-createTestData"
logging_client = logging.Client()
log = logging_client.logger(log_name)

resource = {
    "type": "global",
    "labels": {}
}

def get_random_customer_email(first_name, last_name):
    provider = fake.domain_name()
    email = fake.email(domain=provider)
    return email.lower()

def create_test_data(record_count):
    file_name = f"customers_{record_count}.csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'email', 'phone'])
        for _ in range(record_count):
            id = fake.random_number()
            first_name = fake.first_name()
            last_name = fake.last_name()
            name = f"{first_name} {last_name}"
            email = get_random_customer_email(first_name, last_name)
            phone = fake.phone_number()
            writer.writerow([id, name, email, phone])
    print(f"Created file {file_name} containing {record_count} records.")
    # A text log entry
    success_message = f"Success: createTestData - Created file {file_name} containing {record_count} records."
    log.log_text(success_message, resource=resource)

@app.route('/create', methods=['POST'])
def create_data():
    record_count = int(request.form['record_count'])
    create_test_data(record_count)
    return "Data creation completed"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Include the number of test data records to create. Example:")
        print("    python create_test_data.py 100")
        sys.exit(1)
    record_count = int(sys.argv[1])
    create_test_data(record_count)

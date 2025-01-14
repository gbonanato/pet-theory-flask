import csv
import sys
from google.cloud import firestore
from google.cloud import logging
from flask import Flask, request

app = Flask(__name__)

# Configuração do Firestore
db = firestore.Client()

# Configuração do Logging
log_name = "pet-theory-logs-importTestData"
logging_client = logging.Client()
log = logging_client.logger(log_name)

def write_to_firestore(records):
    batch = db.batch()
    for record in records:
        print(f"Write: {record}")
        doc_ref = db.collection("customers").document(record['email'])
        batch.set(doc_ref, record, merge=True)
    batch.commit()
    print('Batch executed')

def import_csv(csv_filename):
    try:
        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)
            records = [row for row in reader]
            print("Call write to Firestore")
            write_to_firestore(records)
            print(f"Wrote {len(records)} records")
            # A text log entry
            success_message = f"Success: importTestData - Wrote {len(records)} records"
            log.log_text(success_message)
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        sys.exit(1)

@app.route('/import', methods=['POST'])
def import_data():
    csv_filename = request.form['csv_filename']
    import_csv(csv_filename)
    return "Import completed"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please include a path to a csv file")
        sys.exit(1)
    import_csv(sys.argv[1])

from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="creds/serenity-gbq-4f1a4edba243.json"

client = bigquery.Client()

# Perform a query.
QUERY = (
    'SELECT * FROM `serenity-gbq.waterways.test_stac` '
    'LIMIT 10'
)
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(f"id: {row.name}")
    print(f"geometry: {row.geo1}")

import streamlit as st
import pandas as pd
import numpy as np

from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="creds/serenity-gbq-4f1a4edba243.json"

client = bigquery.Client()

@st.cache
def load_data():
    QUERY = (
        'SELECT * FROM `serenity-gbq.waterways.test_stac` '
        'LIMIT 10'
    )
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    list_row = []
    for row in rows:
        # print(f"id: {row.name}")
        # print(f"geometry: {row.geo1}")
        list_row.append(
            {
                "id": row.name,
                "geom": row.geo1,
            }
        )
    return list_row

st.title('STAC Collection GBQ viewer')

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data...done!')

st.subheader('Raw data')
st.write(data)
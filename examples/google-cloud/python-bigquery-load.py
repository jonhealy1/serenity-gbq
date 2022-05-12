import pandas
import geopandas
from shapely import wkt
from google.cloud.bigquery.schema import SchemaField
import google.cloud.bigquery.job
from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="creds/serenity-gbq-4f1a4edba243.json"

def load_geodataframe(bigquery_client, dataset_id):

    df = geopandas.GeoDataFrame(
        pandas.DataFrame(
            dict(
                name=["foo", "bar"],
                geo1=[None, None],
                geo2=[None, wkt.loads("Point(1 1)")],
            )
        ),
        geometry="geo1",
    )

    table_id = f"{dataset_id}.lake_from_gp"
    bigquery_client.load_table_from_dataframe(df, table_id).result()

    table = bigquery_client.get_table(table_id)
    assert table.schema == [
        SchemaField("name", "STRING", "NULLABLE"),
        SchemaField("geo1", "GEOGRAPHY", "NULLABLE"),
        SchemaField("geo2", "GEOGRAPHY", "NULLABLE"),
    ]
    assert sorted(map(list, bigquery_client.list_rows(table_id))) == [
        ["bar", None, "POINT(1 1)"],
        ["foo", None, None],
    ]

def dataset_client(bigquery_client, dataset_id):
    return bigquery.Client(
        default_query_job_config=google.cloud.bigquery.job.QueryJobConfig(
            default_dataset=f"{bigquery_client.project}.{dataset_id}",
        )
    )

client = bigquery.Client()
load_geodataframe(client, "waterways")
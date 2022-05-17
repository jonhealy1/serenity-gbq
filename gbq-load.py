import json
import os
from shapely.geometry import shape
import pandas
import geopandas
from shapely import wkt
from google.cloud.bigquery.schema import SchemaField
import google.cloud.bigquery.job
from google.cloud import bigquery
import random

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="creds/serenity-gbq-4f1a4edba243.json"

def geojson_to_wkt(geojson: dict) -> str:
    """Convert geojson to wkt."""
    geom = shape(geojson)

    return geom.wkt

def load_data(filename: str) -> dict:
    """Load json data."""
    with open(filename) as file:
        return json.load(file)

def load_geodataframe(bigquery_client, dataset_id):
    feature_collection = load_data("data/stac-data/sentinel-s2-l2a-cogs_30001_100000.json")
    # feature_collection = load_data("data/fgb-demo/xab.json")

    df = geopandas.GeoDataFrame(
        pandas.DataFrame(
            dict(
                #name=[str(random.randint(1, 1000000)) for data in feature_collection["features"]],
                name=['wkt' for data in feature_collection["features"]],
                geo1=[wkt.loads(geojson_to_wkt(data["geometry"])) for data in feature_collection["features"]],
            )
        ),
        geometry="geo1",
    )
    print(df)
    

    table_id = f"{dataset_id}.test_stac"
    bigquery_client.load_table_from_dataframe(df, table_id).result()

    table = bigquery_client.get_table(table_id)

    print("Table: ", table)
    assert table.schema == [
        SchemaField("name", "STRING", "NULLABLE"),
        SchemaField("geo1", "GEOGRAPHY", "NULLABLE"),
    ]
 
client = bigquery.Client()
load_geodataframe(client, "waterways")
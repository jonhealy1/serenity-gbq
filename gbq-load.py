import json
import os
from shapely.geometry import shape
import pandas
import geopandas
from shapely import wkt
from google.cloud.bigquery.schema import SchemaField
import google.cloud.bigquery.job
from google.cloud import bigquery

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
    feature_collection = load_data("data/stac-data/sentinel-s2-l2a-cogs_100_10000.json")

    geo_dict = {
        "name": [],
        "geo": []
    }
    for data in feature_collection["features"]:
        geo_dict["name"].append(data["id"])
        geo_dict["geo1"].append(data["geometry"])
        
    df = geopandas.GeoDataFrame(
        pandas.DataFrame(geo_dict),
        geometry="geo1",
    )
    # print(df)

    table_id = f"{dataset_id}.test_stac"
    bigquery_client.load_table_from_dataframe(df, table_id).result()

    table = bigquery_client.get_table(table_id)
    assert table.schema == [
        SchemaField("name", "STRING", "NULLABLE"),
        SchemaField("geo1", "GEOGRAPHY", "NULLABLE"),
    ]
 
client = bigquery.Client()
load_geodataframe(client, "waterways")
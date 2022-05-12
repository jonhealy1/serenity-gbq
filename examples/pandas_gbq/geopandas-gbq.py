import geopandas as gpd
import pandas_gbq as gbq

project_id = "serenity-gbq"
table_id = "demo"

def ingest_shapefile_bigquery(**kwargs):
    geo_df = gpd.read_file("Vancouver-shp/shape/buildings.shp")
    dataset_id = "waterways"
    print(geo_df)
    gbq.to_gbq(dataframe=geo_df,
        destination_table=dataset_id +"." +table_id,
        project_id=project_id,
        if_exists="replace",
        # table_schema=specify_schema_object
    )

ingest_shapefile_bigquery()

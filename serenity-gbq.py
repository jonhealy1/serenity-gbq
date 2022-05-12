import json
import os
from shapely.geometry import shape

def geojson_to_wkt(geojson: dict) -> str:
    """Convert geojson to wkt."""
    geom = shape(geojson)

    return geom.wkt

def load_data(filename: str) -> dict:
    """Load json data."""
    with open(filename) as file:
        return json.load(file)

def load_items() -> list:
    """Load stac items, convert"""
    feature_collection = load_data("data/stac-data/sentinel-s2-l2a-cogs_0_100.json")
    data_list = []

    for feature in feature_collection["features"]:
        data_list.append(
            {
                "id": feature["id"],
                "wkt": geojson_to_wkt(feature["geometry"])
            }
        )
        
    return data_list

data_list = load_items()

print(data_list)
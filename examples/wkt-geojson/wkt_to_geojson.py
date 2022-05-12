from shapely.wkt import loads
from shapely.geometry import mapping
import geojson
import ast

wkt_string = '''POLYGON ((23.314208 37.768469, 24.039306 37.768469, 24.039306 38.214372, 23.314208 38.214372, 23.314208 37.768469))'''

geojson_string = geojson.dumps(mapping(loads(wkt_string)))

geojson_dict = ast.literal_eval(geojson_string)
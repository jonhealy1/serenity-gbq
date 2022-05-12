# https://gist.github.com/drmalex07/5a54fc4f1db06a66679e

from shapely.geometry import shape

o = {
   "coordinates": [[[23.314208, 37.768469], [24.039306, 37.768469], [24.039306, 38.214372], [23.314208, 38.214372], [23.314208, 37.768469]]], 
   "type": "Polygon"
}
geom = shape(o)

# Now it's very easy to get a WKT/WKB representation
geom.wkt
geom.wkb

print(geom.wkt)
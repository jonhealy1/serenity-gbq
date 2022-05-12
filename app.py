import streamlit as st
import pandas as pd
import numpy as np
import folium
import geopandas
from shapely import wkt
from matplotlib import pyplot
from shapely.geometry.polygon import LinearRing, Polygon
from streamlit_folium import st_folium

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

# st.subheader('Map')
# # st.map(data)
# st.map(data=None, zoom=None, use_container_width=True)

# st.subheader('Raw data')
# st.write(data)

df = pd.DataFrame(
    {
        'id': [row["id"] for row in data],
        'geometry': [row["geom"] for row in data]
    }
)

df['geometry'] = geopandas.GeoSeries.from_wkt(df['geometry'])

gdf = geopandas.GeoDataFrame(df, geometry='geometry')

print(gdf.head())

# gdf.plot()

# plt.show()

gdf.loc[5, "geometry"]

m = folium.Map(location=[40.70, -73.94], zoom_start=10, tiles='CartoDB positron')

st_data = st_folium(m, width = 725)
# st.set_option('deprecation.showPyplotGlobalUse', False)
# st.pyplot()
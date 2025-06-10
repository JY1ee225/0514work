import streamlit as st
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap

# 從 Streamlit Secrets 讀取 GEE 服務帳戶金鑰 JSON
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]

credentials  = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# 初始化 GEE
ee.Initialize(credentials)

st.set_page_config(layout="wide")
st.title("🌍阿里山地區的森林覆蓋狀況")

if not ee.data._initialized:
    ee.Authenticate()
    ee.Initialize()

alishan = ee.Geometry.Rectangle([120.7, 23.45, 121.0, 23.6])

def get_ndvi(year):
    collection = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2') \
        .filterDate(f'{year}-01-01', f'{year}-12-31') \
        .filterBounds(alishan) \
        .filter(ee.Filter.lt('CLOUD_COVER', 50))
    
    if collection.size().getInfo() == 0:
        st.warning(f"{year} 年無可用資料")
        return ee.Image().rename('NDVI')

    image = collection.median()
    ndvi = image.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
    return ndvi.clip(alishan)

ndvi_1990 = get_ndvi(1990)
ndvi_2010 = get_ndvi(2010)

ndvi_vis = {'min': 0, 'max': 1, 'palette': ['white', 'green']}

left = geemap.ee_tile_layer(ndvi_1990, ndvi_vis, 'NDVI 1990')
right = geemap.ee_tile_layer(ndvi_2010, ndvi_vis, 'NDVI 2010')

Map.split_map(
    left_layer=left,
    right_layer=right,
    left_label="NDVI 1990",
    right_label="NDVI 2010"
)
Map.to_streamlit(width=1200, height=600)

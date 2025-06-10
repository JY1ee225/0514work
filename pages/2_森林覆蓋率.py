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

# 地理區域
alishan = ee.Geometry.Rectangle(120.67890712750258,23.56504921800958,120.85503169704448,23.486982449033867)

# 計算 NDVI 的函數，使用 Collection 2
def get_ndvi_landsat5_c2(year):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    collection = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2') \
        .filterDate(start_date, end_date) \
        .filterBounds(alishan) \
        .filter(ee.Filter.lt('CLOUD_COVER', 30)) \
        .median()
    
    # Collection 2 的波段：SR_B4 = NIR, SR_B3 = RED
    ndvi = collection.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
    return ndvi

# 計算 NDVI 1990 和 2010
ndvi_1990 = get_ndvi_landsat5_c2(1990)
ndvi_2010 = get_ndvi_landsat5_c2(2010)

# NDVI 顯示樣式
ndvi_vis = {
    'min': 0.0,
    'max': 1.0,
    'palette': ['white', 'green']
}

# Split Map（左：1990，右：2010）
left_layer = geemap.ee_tile_layer(ndvi_1990.clip(alishan), ndvi_vis, 'NDVI 1990')
right_layer = geemap.ee_tile_layer(ndvi_2010.clip(alishan), ndvi_vis, 'NDVI 2010')

# 建立 split map
Map = geemap.Map(center=[23.52, 120.76], zoom=13)
Map.split_map(left_layer, right_layer)
Map

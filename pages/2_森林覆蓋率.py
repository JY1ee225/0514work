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

# 初始化 Earth Engine
if not ee.data._initialized:
    ee.Authenticate()
    ee.Initialize()

# 阿里山區域（矩形範圍）
alishan = ee.Geometry.Rectangle(120.67890712750258,23.56504921800958,120.85503169704448,23.486982449033867)

# NDVI 計算函數（Landsat 5 C2）
def get_ndvi(year):
    collection = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2') \
        .filterDate(f'{year}-01-01', f'{year}-12-31') \
        .filterBounds(alishan) \
        .filter(ee.Filter.lt('CLOUD_COVER', 50))

    if collection.size().getInfo() == 0:
        st.warning(f"{year} 年無可用資料")
        return None

    image = collection.median()
    ndvi = image.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
    return ndvi.clip(alishan)

# 計算 NDVI 影像
ndvi_1990 = get_ndvi(1990)
ndvi_2010 = get_ndvi(2010)

# 若任一影像為空則不執行
if not ndvi_1990 or not ndvi_2010:
    st.stop()

# 顏色參數
ndvi_vis = {
    'min': 0.0,
    'max': 1.0,
    'palette': ['white', 'green']
}

# 包裝成地圖圖層
left_layer = geemap.ee_tile_layer(ndvi_1990, ndvi_vis, 'NDVI 1990')
right_layer = geemap.ee_tile_layer(ndvi_2010, ndvi_vis, 'NDVI 2010')

# 建立地圖
Map = geemap.Map(center=[23.5, 120.76], zoom=13)
Map.split_map(
    left_layer=left_layer,
    right_layer=right_layer,
    left_label="NDVI 1990",
    right_label="NDVI 2010"
)
Map.to_streamlit(width=1200, height=600)

st.header("看圖說故事")
st.markdown(
    """
    -白色（white） 表示 NDVI 值較低 的區域（接近 0），通常代表：無植被或植被稀疏區域（例如城市、裸地、岩石、乾燥土壤）、水體（有時 NDVI 值甚至為負）
    
    -綠色（green） 表示 NDVI 值較高 的區域（接近 1），通常代表：濃密健康的植被（例如森林、農作物）NDVI 值愈高，表示植物光合作用愈旺盛、葉綠素含量高
    """
)
st.markdown(
    """
    經由1990年以及2010年的圖對比，可以發現白色部分逐年變多，河川部分可能是因河水侵蝕而導致河床變寬；而右區變得稍微較白的原因可能為地形崩塌等，會在第三節中加以說明；而左下角為奮起湖，則是觀光事業的興起而導致的房屋變多。
    """
)

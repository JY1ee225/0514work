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
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")

# 地理區域
point = ee.Geometry.Point([120.5583462887228, 24.081653403304525])

# 擷取 Landsat 
my_image = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')\
    .filterBounds(point)\
    .filterDate('2021-01-01', '2022-01-01')\
    .sort('CLOUDY_PIXEL_PERCENTAGE')\
    .first()\
    .select('B.*')
)
vis_params = {'min':100, 'max': 3500, 'bands': ['B5',  'B4',  'B3']}

training001 = my_image.sample(
    **{
        'region': my_image.geometry(),  # 若不指定，則預設為影像my_image的幾何範圍。
        'scale': 10,
        'numPixels': 10000,
        'seed': 0,
        'geometries': True,  # 設為False表示取樣輸出的點將忽略其幾何屬性(即所屬網格的中心點)，無法作為圖層顯示，可節省記憶體。
    }
)

num_clusters = 5
clusterer_KMeans = ee.Clusterer.wekaKMeans(nClusters=num_clusters).train(training001)
result001 = my_image.cluster(clusterer_KMeans)


# 英文數字標籤
labels = [
    'zero', 'one', 'two', 'three', 'four', 'five',
    'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'
][:num_clusters]  # 擷取前 num_clusters 個標籤

# 你可以使用 color palette（這裡使用 colorbrewer 上的一組 palette）
palette = [
    '#ab0000', '#1c5f2c', '#d99282', '#466b9f', '#ab6c28',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
][:num_clusters]  # 擷取前 num_clusters 種顏色

# 建立 legend_dict：將每一個群（label）對應一種顏色
legend_dict = dict(zip(labels, palette))

# 視覺化參數
vis_params_001 = {'min': 0, 'max': num_clusters - 1, 'palette': palette}

Map = geemap.Map()
Map.add_basemap('HYBRID')
left_layer = geemap.ee_tile_layer(my_image, vis_params, 'S2')
right_layer = geemap.ee_tile_layer(result001, vis_params_001, 'wekakMeans')
Map.centerObject(my_image.geometry(), 10)
Map.split_map(left_layer, right_layer)
Map.add_legend(title='Land Cover Type', legend_dict = legend_dict,draggable=False, position = 'bottomright')
Map.to_streamlit(height=700)

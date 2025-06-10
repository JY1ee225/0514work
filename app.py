import streamlit as st
from datetime import date

#wide使螢幕使用到最寬的範圍 
st.set_page_config(layout="wide", page_title="阿里山地區土地使用及災害")

st.title("阿里山地區土地使用及災害")

#三個雙引號內都是字串
#超連結【文字】(連結)
st.markdown(
    """
    本app會討論阿里山地區的土地使用以及災害後地景變化還有微微的觀光
    """
)

st.header("阿里山森林遊樂區簡介")

markdown = """
阿里山國家風景區包括番路、竹崎、梅山、阿里山共四鄉，如葉脈般的交通路網蔓延群山，引領旅人穿梭在層疊的山林綠意，驚豔日出流雲之美、品味細緻茶園風光，還有鄒族原鄉人文，都是阿里山不容錯過的遊憩焦點！

"""

st.markdown(markdown)

with st.expander("阿里山森林遊樂區"):
    st.image("關西機場.gif")



st.title("選擇日期區間")


# 初始化 session_state
#if 'start_date' not in st.session_state:
#    st.session_state['start_date'] = date(2024, 1, 1)
#if 'end_date' not in st.session_state:
#    st.session_state['end_date'] = date.today()

st.session_state['start_date'] = date(2024, 1, 1)
st.session_state['end_date'] = date.today()


# 日期選擇器
start_date = st.date_input(label = "選擇起始日期", value = st.session_state['start_date'], min_value = date(2018, 1, 1), max_value = date.today())
end_date = st.date_input(label = "選擇結束日期", value = st.session_state['end_date'], min_value = start_date, max_value = date.today())

# 儲存使用者選擇
st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date

st.success(f"目前選擇的日期區間為：{start_date} 到 {end_date}")


st.title("利用擴充器示範")

#st.image("網址")或是上傳資料然後打名稱
with st.expander("展示gif檔"):
    st.image("關西機場.gif")

with st.expander("播放mp4檔"):
    video_file = open("pucallpa.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)

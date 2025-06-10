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
    st.image("ali-img-2-md.jpg")



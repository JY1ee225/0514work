import streamlit as st

st.title("眠月線的崩塌情況")
st.markdown(
    """
    由以下動圖可了解此山區到了1999年突然有了很大的變化，推測是因為921大地震，整條路線坍方崩壞，眠月線鐵路嚴重毀損而暫停行駛，八八風災(2009)後鐵道舊線及車站更顯頹圮不堪。
    """
)
st.header("眠月線旅遊新勝地？")

markdown = """
此路線原本是民國60-70年間，救國團溪阿緃活動中的一段行程，沿路可看到森林、鐵道、車站、廢棄林業工作站等具特色的景觀，歷經多次災害後斑駁錯落的時空感，卻更顯眠月線之難得與靈氣，為回溯台灣林業史必走之路徑。
"""

st.markdown(markdown)
with st.expander("眠月線"):
    st.image("眠月線.jpg")
    
with st.expander("眠月線timelapse"):
    st.image("阿里山 (1).gif")

with st.expander("眠月線google earth pro影像"):
    video_file = open("Google Earth Pro 2025-06-10 11-19-52.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)

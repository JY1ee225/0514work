import streamlit as st

with st.expander("眠月線timelapse"):
    st.image("阿里山 (1).gif")

with st.expander("眠月線google earth pro影像"):
    video_file = open("pucallpa.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)

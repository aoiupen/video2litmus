import streamlit as st
import os
from adapter_streamlit import streamlit_analyze

THUMBNAIL_WIDTH = 320
APP_PADDING = 40

st.set_page_config(
    page_title="영상 색상 타임라인",
    layout="centered"
)

st.markdown(
    f"""
    <style>
    .main .block-container {{
        max-width: {THUMBNAIL_WIDTH + APP_PADDING}px;
        padding-left: 20px;
        padding-right: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("영상 색상 타임라인 분석")

uploaded_file = st.file_uploader("분석할 영상 파일 업로드", type=["mp4"])

if uploaded_file:
    os.makedirs(".st_tmp_frames", exist_ok=True)
    video_path = os.path.join(".st_tmp_frames", "uploaded.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    num_frames = st.slider("분석할 프레임 개수", 10, 100, 30)
    frame_pos = st.slider("분석할 프레임 위치", 0, num_frames-1, 0)
    n_colors = st.slider("상위 색상 개수", 1, 20, 10)

    frame_img, bar_img = streamlit_analyze(video_path, frame_pos, num_frames, n_colors)
    if frame_img is not None:
        st.image(frame_img, caption=f"프레임 {frame_pos}", width=THUMBNAIL_WIDTH)
        st.image(bar_img, caption=f"상위 {n_colors}개 색상 리트머스 막대")
    else:
        st.error("프레임을 추출할 수 없습니다.") 
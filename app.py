import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
from mv_color_timeline import extract_frames, extract_main_colors, plot_litmus_bar

# 썸네일 이미지 크기(예: 320px)에 맞춰 전체 앱 너비 고정
THUMBNAIL_WIDTH = 320
APP_PADDING = 40  # 좌우 여백 포함

st.set_page_config(
    page_title="영상 색상 타임라인",
    layout="centered"
)

# CSS로 메인 컨테이너 너비 고정
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

# 썸네일 예시
st.markdown(
    f'<img src="https://img.youtube.com/vi/qIygxFUTo-A/maxresdefault.jpg" width="{THUMBNAIL_WIDTH}"/>',
    unsafe_allow_html=True
)

# 영상 업로드, 분석, 결과 시각화 등 추가
uploaded_file = st.file_uploader("분석할 영상 파일 업로드", type=["mp4"])

if uploaded_file:
    # 임시 폴더 생성
    os.makedirs(".st_tmp_frames", exist_ok=True)
    video_path = os.path.join(".st_tmp_frames", "uploaded.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    # 프레임 추출
    num_frames = st.slider("분석할 프레임 개수", 10, 100, 30)
    frame_paths = extract_frames(video_path, ".st_tmp_frames", num_frames=num_frames)
    st.success(f"총 {len(frame_paths)}개 프레임 추출 완료!")
    # 프레임 선택
    frame_idx = st.slider("분석할 프레임 위치", 0, len(frame_paths)-1, 0)
    frame_img = Image.open(frame_paths[frame_idx])
    st.image(frame_img, caption=f"프레임 {frame_idx}", width=THUMBNAIL_WIDTH)
    # 상위 색상 개수 슬라이더
    n_colors = st.slider("상위 색상 개수", 1, 20, 10)
    colors, counts = extract_main_colors(frame_paths[frame_idx], n_colors=n_colors)
    # 리트머스 막대 시각화(메모리상 생성)
    bar_img_path = os.path.join(".st_tmp_frames", "bar_tmp.png")
    plot_litmus_bar(colors, counts, bar_img_path, width=THUMBNAIL_WIDTH, height=300)
    st.image(bar_img_path, caption=f"상위 {n_colors}개 색상 리트머스 막대") 
import streamlit as st
import os
import cv2
from PIL import Image
from mv_color_timeline import extract_main_colors, plot_litmus_bar

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
    os.makedirs(".st_tmp_frames", exist_ok=True)
    video_path = os.path.join(".st_tmp_frames", "uploaded.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    # 전체 프레임 수 구하기
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    num_frames = st.slider("분석할 프레임 개수", 10, 100, 30)
    frame_pos = st.slider("분석할 프레임 위치", 0, num_frames-1, 0)
    n_colors = st.slider("상위 색상 개수", 1, 20, 10)

    # 실제 분석할 프레임 인덱스 계산
    frame_idx = int(total_frames * frame_pos / num_frames)

    # 해당 프레임만 추출
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()
    if ret:
        frame_img_path = os.path.join(".st_tmp_frames", "current_frame.png")
        cv2.imwrite(frame_img_path, frame)
        frame_img = Image.open(frame_img_path)
        st.image(frame_img, caption=f"프레임 {frame_idx}", width=THUMBNAIL_WIDTH)
        colors, counts = extract_main_colors(frame_img_path, n_colors=n_colors)
        bar_img_path = os.path.join(".st_tmp_frames", "bar_tmp.png")
        plot_litmus_bar(colors, counts, bar_img_path, width=THUMBNAIL_WIDTH, height=300)
        st.image(bar_img_path, caption=f"상위 {n_colors}개 색상 리트머스 막대")
    else:
        st.error("프레임을 추출할 수 없습니다.") 
import streamlit as st
import os
from viewmodel import analyze_frame, analyze_accumulated_bar

THUMBNAIL_WIDTH = 320
BAR_HEIGHT = 300
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

frame_img_path = None
bar_img_path = None
num_frames = 30
frame_pos = 0
n_colors = 10
mode_toggle = "단일 리트머스"

if uploaded_file:
    os.makedirs(".st_tmp_frames", exist_ok=True)
    video_path = os.path.join(".st_tmp_frames", "uploaded.mp4")
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    # 이미지 먼저 상단에 배치
    col1, col2 = st.columns([2, 1])
    with st.container():
        with col1:
            frame_img_placeholder = st.empty()
        with col2:
            bar_img_placeholder = st.empty()

    # 컨트롤(슬라이더, 라디오 등)은 하단에 배치
    with st.container():
        num_frames = st.slider("분석할 프레임 개수", 10, 100, 30)
        frame_pos = st.slider("분석할 프레임 위치", 0, num_frames-1, 0)
        n_colors = st.slider("상위 색상 개수", 1, 20, 10)
        mode_toggle = st.radio("리트머스 모드", ["단일 리트머스", "누적 리트머스"], index=0, help="오른쪽 리트머스 바를 누적/단일로 전환")

    try:
        min_side = max(8, int((n_colors) ** 0.5) + 1)
        if mode_toggle == "누적 리트머스":
            _, bar_img_path = analyze_accumulated_bar(
                video_path, frame_pos, num_frames, n_colors,
                tmp_dir=".st_tmp_frames", width=25, height=BAR_HEIGHT
            )
            frame_img_path = os.path.normpath(os.path.join(".st_tmp_frames", f"frame_{frame_pos:04d}.png"))
        else:
            frame_img_path, bar_img_path = analyze_frame(
                video_path, frame_pos, num_frames, n_colors,
                tmp_dir=".st_tmp_frames", width=THUMBNAIL_WIDTH, height=BAR_HEIGHT
            )
            frame_img_path = os.path.normpath(frame_img_path) if frame_img_path else None
            bar_img_path = os.path.normpath(bar_img_path) if bar_img_path else None
    except Exception:
        frame_img_path, bar_img_path = None, None

    # 두 이미지 모두 높이 BAR_HEIGHT로 맞춰서 표시
    with col1:
        if frame_img_path and os.path.exists(frame_img_path):
            st.image(frame_img_path, caption=f"프레임 {frame_pos}", width=THUMBNAIL_WIDTH)
        else:
            st.warning("프레임 이미지를 표시할 수 없습니다.")
    with col2:
        if bar_img_path and os.path.exists(bar_img_path):
            st.image(bar_img_path, caption=f"리트머스 바 ({mode_toggle})", width=THUMBNAIL_WIDTH)
        else:
            st.warning("리트머스 바 이미지를 표시할 수 없습니다.") 
import os
import cv2
import numpy as np
from PIL import Image
from mv_color_timeline import extract_main_colors, plot_litmus_bar
from io import BytesIO

def analyze_frame(video_path, frame_pos, num_frames, n_colors, tmp_dir=".st_tmp_frames", width=320, height=300):
    """
    영상 경로, 프레임 위치, 프레임 개수, 색상 개수를 받아 해당 프레임 이미지와 리트머스 막대 이미지를 반환
    """
    # 전체 프레임 수 구하기
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    frame_idx = int(total_frames * frame_pos / num_frames)
    # 해당 프레임 추출
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None, None
    frame_img_path = os.path.join(tmp_dir, "current_frame.png")
    cv2.imwrite(frame_img_path, frame)
    with open(frame_img_path, "rb") as f:
        frame_bytes = f.read()
    colors, counts = extract_main_colors(frame_img_path, n_colors=n_colors)
    bar_img_path = os.path.join(tmp_dir, "bar_tmp.png")
    plot_litmus_bar(colors, counts, bar_img_path, width=width, height=height)
    with open(bar_img_path, "rb") as f:
        bar_bytes = f.read()
    frame_img = Image.open(frame_img_path)
    bar_img = Image.open(bar_img_path)
    return frame_img.copy(), bar_img.copy() 
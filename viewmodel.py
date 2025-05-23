import os
import cv2
import numpy as np
from PIL import Image
from model import extract_main_colors, plot_litmus_bar, concat_bars
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
    print(f"[analyze_frame] frame_img_path={frame_img_path}, bar_img_path={bar_img_path}")
    print(f"[analyze_frame] frame_img={type(frame_img)}, bar_img={type(bar_img)}")
    return frame_img_path, bar_img_path

def analyze_accumulated_bar(video_path, frame_pos, num_frames, n_colors, tmp_dir=".st_tmp_frames", width=25, height=300):
    """
    0~frame_pos까지의 리트머스 바를 이어붙인 누적 이미지를 반환한다.
    (프레임 이미지는 None, 누적 리트머스 바 이미지는 concat_path 경로)
    """
    # 프레임 경로 리스트 확보
    frame_paths = [os.path.join(tmp_dir, f"frame_{i:04d}.png") for i in range(frame_pos+1)]
    bar_paths = []
    for i, frame_path in enumerate(frame_paths):
        if not os.path.exists(frame_path):
            continue
        colors, counts = extract_main_colors(frame_path, n_colors=n_colors)
        bar_img_path = os.path.join(tmp_dir, f"accum_bar_{i:04d}.png")
        plot_litmus_bar(colors, counts, bar_img_path, width=width, height=height)
        bar_paths.append(bar_img_path)
    if not bar_paths:
        return None, None
    concat_path = os.path.join(tmp_dir, f"accum_bar_concat_{frame_pos}.png")
    concat_bars(bar_paths, concat_path, direction='horizontal', total_bars=num_frames, bar_width=width, bar_height=height)
    print(f"[analyze_accumulated_bar] frame_paths={frame_paths}", flush=True)
    print(f"[analyze_accumulated_bar] concat_path={concat_path}", flush=True)
    print(f"[analyze_accumulated_bar] bar_img_path={concat_path}")
    return None, concat_path 
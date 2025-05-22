from viewmodel import analyze_frame
import os, shutil, tempfile

def gradio_analyze(video, frame_pos, num_frames, n_colors):
    # 고정 임시 폴더 사용
    tmp_dir = ".st_tmp_frames"
    os.makedirs(tmp_dir, exist_ok=True)
    video_path = os.path.join(tmp_dir, "uploaded.mp4")
    shutil.copy(video.name, video_path)
    frame_img_path, bar_img_path = analyze_frame(video_path, frame_pos, num_frames, n_colors, tmp_dir=tmp_dir)
    return frame_img_path, bar_img_path
from viewmodel import analyze_frame

def streamlit_analyze(video_path, frame_pos, num_frames, n_colors, tmp_dir=".st_tmp_frames", width=320, height=300):
    frame_img, bar_img = analyze_frame(video_path, frame_pos, num_frames, n_colors, tmp_dir=tmp_dir, width=width, height=height)
    return frame_img, bar_img 
import gradio as gr
import os
import cv2
import shutil
from viewmodel import analyze_frame, analyze_accumulated_bar
from mv_color_timeline import extract_main_colors
import time

def extract_and_cache_frames(video_path, num_frames, tmp_dir, min_resize_pixels=20):
    os.makedirs(tmp_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        return []
    step = max(total_frames // num_frames, 1)
    frame_paths = []
    for i, frame_idx in enumerate(range(0, total_frames, step)):
        if i >= num_frames:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(tmp_dir, f"frame_{i:04d}.png")
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
    cap.release()
    return frame_paths

def get_total_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total

def gradio_ui():
    with gr.Blocks() as demo:
        gr.Markdown("## Video Color Timeline Analysis (Gradio)")
        with gr.Row():
            with gr.Column(scale=2):
                frame_img = gr.Image(label="Frame", elem_id="frame-img")
            with gr.Column(scale=1):
                bar_img = gr.Image(label="Litmus Bar", elem_id="bar-img")
            with gr.Column(scale=1):
                video_file = gr.File(label="Video (.mp4)")
                num_frames = gr.Slider(10, 100, value=30, step=1, label="Number of Frames")
                n_colors = gr.Slider(1, 20, value=10, step=1, label="Top N Colors")
                frame_pos = gr.Slider(0, 0, value=0, step=1, label="Frame Position (auto)")
                mode_toggle = gr.Radio(["단일 리트머스", "누적 리트머스"], value="단일 리트머스", label="리트머스 모드", info="오른쪽 리트머스 바를 누적/단일로 전환")
        state = gr.State({"frame_paths": [], "total_frames": 0})

        def on_upload(video, num_frames, n_colors):
            tmp_dir = ".st_tmp_frames"
            os.makedirs(tmp_dir, exist_ok=True)
            video_path = os.path.join(tmp_dir, "uploaded.mp4")
            shutil.copy(video.name, video_path)
            frame_paths = extract_and_cache_frames(video_path, num_frames, tmp_dir)
            total = len(frame_paths)
            min_side = max(8, int((n_colors) ** 0.5) + 1)
            return gr.update(value=0, minimum=0, maximum=max(total-1, 0), step=1), {"frame_paths": frame_paths, "total_frames": total, "video_path": video_path, "resize": (min_side, min_side)}

        def on_change(state, frame_pos, n_colors, mode_toggle):
            frame_paths = state["frame_paths"]
            print(f"[on_change] frame_pos={frame_pos}, n_colors={n_colors}, mode_toggle={mode_toggle}")
            print(f"[on_change] frame_paths={frame_paths}")
            if not frame_paths:
                print("[on_change] frame_paths is empty!")
                return None, None
            min_side = max(8, int((n_colors) ** 0.5) + 1)
            if mode_toggle == "누적 리트머스":
                _, bar_img_path = analyze_accumulated_bar(
                    state["video_path"], frame_pos, len(frame_paths), n_colors,
                    tmp_dir=".st_tmp_frames", width=25, height=300
                )
                frame_img_path = frame_paths[frame_pos] if os.path.exists(frame_paths[frame_pos]) else None
                bar_img_path_with_query = f"{bar_img_path}?t={int(time.time()*1000)}"
                print(f"[on_change] 누적모드 frame_img_path={frame_img_path}, bar_img_path={bar_img_path_with_query}", flush=True)
                return frame_img_path, bar_img_path_with_query
            else:
                frame_img_path, bar_img_path = analyze_frame(
                    state["video_path"], frame_pos, len(frame_paths), n_colors,
                    tmp_dir=".st_tmp_frames", width=320, height=300, resize=(min_side, min_side)
                )
                print(f"[on_change] 단일모드 frame_img_path={frame_img_path}, bar_img_path={bar_img_path}")
                return frame_img_path, bar_img_path

        video_file.change(
            on_upload,
            inputs=[video_file, num_frames, n_colors],
            outputs=[frame_pos, state],
        )
        frame_pos.change(
            on_change,
            inputs=[state, frame_pos, n_colors, mode_toggle],
            outputs=[frame_img, bar_img],
        )
        n_colors.change(
            on_change,
            inputs=[state, frame_pos, n_colors, mode_toggle],
            outputs=[frame_img, bar_img],
        )
        mode_toggle.change(
            on_change,
            inputs=[state, frame_pos, n_colors, mode_toggle],
            outputs=[frame_img, bar_img],
        )
    return demo

demo = gradio_ui()

if __name__ == "__main__":
    demo.launch(inbrowser=True)
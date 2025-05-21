import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image

def extract_main_colors(image_path, n_colors=20, resize=(80, 45)):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if resize is not None:
        img = cv2.resize(img, resize, interpolation=cv2.INTER_AREA)
    img = img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=5, max_iter=100)
    kmeans.fit(img)
    colors = np.array(kmeans.cluster_centers_, dtype='uint8')
    counts = np.bincount(kmeans.labels_)
    sorted_idx = np.argsort(-counts)
    colors = colors[sorted_idx]
    counts = counts[sorted_idx]
    return colors, counts

def plot_bar(colors, counts, title, out_path):
    plt.figure(figsize=(8, 2))
    plt.bar(range(len(colors)), counts, color=colors/255, width=1)
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def plot_litmus_bar(colors, counts, out_path, width=25, height=300):
    total = np.sum(counts)
    if total == 0:
        total = 1
    heights = (counts / total * height).astype(int)
    bar_img = np.zeros((height, width, 3), dtype=np.uint8) + 255
    y = 0
    for color, h in zip(colors, heights):
        if h == 0:
            continue
        bar_img[y:y+h, :] = color
        y += h
    # 마지막 색상으로 남은 부분 채우기(오차 보정)
    if y < height:
        bar_img[y:height, :] = colors[0]
    Image.fromarray(bar_img).save(out_path)

def process_frames(frame_dir, out_dir, n_colors=20):
    os.makedirs(out_dir, exist_ok=True)
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.lower().endswith('.png')])
    bar_paths_20 = []
    bar_paths_1 = []
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(frame_dir, frame_file)
        colors, counts = extract_main_colors(frame_path, n_colors=n_colors)
        # 20색 리트머스 막대그래프
        bar_path_20 = os.path.join(out_dir, f'bar20_{i:04d}.png')
        plot_litmus_bar(colors, counts, bar_path_20, width=25, height=300)
        bar_paths_20.append(bar_path_20)
        # 1색 리트머스 막대그래프
        main_color = colors[0:1]
        main_count = counts[0:1]
        bar_path_1 = os.path.join(out_dir, f'bar1_{i:04d}.png')
        plot_litmus_bar(main_color, main_count, bar_path_1, width=25, height=300)
        bar_paths_1.append(bar_path_1)
    return bar_paths_20, bar_paths_1

def concat_bars(bar_paths, out_path, direction='horizontal', final_aspect_ratio=None):
    images = [Image.open(p) for p in bar_paths]
    widths, heights = zip(*(img.size for img in images))
    if direction == 'horizontal':
        total_width = sum(widths)
        max_height = max(heights)
        new_img = Image.new('RGB', (total_width, max_height), (255,255,255))
        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.size[0]
    else:
        max_width = max(widths)
        total_height = sum(heights)
        new_img = Image.new('RGB', (max_width, total_height), (255,255,255))
        y_offset = 0
        for img in images:
            new_img.paste(img, (0, y_offset))
            y_offset += img.size[1]
    # 16:9 비율로 리사이즈
    if final_aspect_ratio is not None:
        w, h = new_img.size
        target_w = w
        target_h = int(w * 9 / 16)
        if target_h > h:
            target_h = h
            target_w = int(h * 16 / 9)
        new_img = new_img.resize((target_w, target_h), Image.LANCZOS)
    new_img.save(out_path)

# 영상에서 균등 간격으로 프레임 추출하여 PNG로 저장하는 함수
# video_path: 입력 영상 경로
# out_dir: 프레임 저장 폴더
# num_frames: 추출할 프레임 개수
# 반환값: 저장된 프레임 파일 경로 리스트

def extract_frames(video_path, out_dir, num_frames=30):
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print(f"영상에서 프레임 정보를 읽을 수 없습니다: {video_path}")
        cap.release()
        return []
    step = max(total_frames // num_frames, 1)
    saved_paths = []
    for i, frame_idx in enumerate(range(0, total_frames, step)):
        if i >= num_frames:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        out_path = os.path.join(out_dir, f"frame_{i:04d}.png")
        cv2.imwrite(out_path, frame)
        saved_paths.append(out_path)
        print(f"프레임 저장: {out_path}")
    cap.release()
    print(f"총 {len(saved_paths)}개의 프레임을 추출했습니다.")
    return saved_paths

def main():
    # 0. 영상에서 프레임 추출
    video_path = os.path.join('sample', 'sample.mp4')  # 샘플 영상 경로
    frame_dir = 'frames'  # 프레임 PNG 이미지가 들어있는 폴더명
    out_dir = 'bars'      # 막대그래프 임시 저장 폴더
    num_frames = 100      # 추출할 프레임 개수(100개로 변경)
    os.makedirs(out_dir, exist_ok=True)

    print("영상에서 프레임 추출 중...")
    extract_frames(video_path, frame_dir, num_frames=num_frames)

    # 2. 각 프레임에서 주요 색상 추출 및 막대그래프 생성
    print("프레임별 주요 색상 추출 및 막대그래프 생성 중...")
    bar_paths_20, bar_paths_1 = process_frames(frame_dir, out_dir, n_colors=20)

    # 3. 막대그래프 이어붙이기 (시간 순서대로)
    print("막대그래프 이어붙이는 중...")
    concat_bars(bar_paths_20, 'timeline_20colors.png', direction='horizontal', final_aspect_ratio=(16,9))
    concat_bars(bar_paths_1, 'timeline_1color.png', direction='horizontal', final_aspect_ratio=(16,9))

    print("완료! 결과 파일: timeline_20colors.png, timeline_1color.png")

if __name__ == '__main__':
    main()

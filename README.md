# Video Color Timeline Visualization

## Project Overview

This project is a Python-based tool that visualizes the overall color mood and transitions of a video by extracting the main colors from each frame and displaying them as a timeline. You can intuitively understand how the color palette of a video changes over time.

---

## Key Features

- **Dual UI support: Streamlit & Gradio (adapter pattern)**
- **Frame extraction and caching at regular intervals**
- **KMeans-based extraction and ratio calculation of top N colors per frame**
- **Litmus bar (vertical color bar) visualization for each frame**
- **Toggle between single/accumulated litmus bar modes**
- **Sliders for frame count, frame position, and number of colors**
- **Gradio: 3-column (Frame | Litmus | Controls) horizontal layout, Streamlit: vertical layout**
- **Platform launcher (main.py) to select UI via web**

---

## How to Use

1. **Setup Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # (Windows)
   pip install -r requirements.txt
   ```

2. **Prepare Video**
   - Upload your video file via the UI (recommended)
   - (Direct file placement is not required; use the upload feature in the UI)

3. **Run**
   - Recommended: `python main.py` and select UI in browser (choose Gradio or Streamlit)
   - (Direct execution of view_gradio.py or view_streamlit.py is possible for development, but use main.py for normal use)

4. **Check Results**
   - Use the UI to view frame images, litmus bars, adjust sliders, and toggle modes

---

## Code Structure

- `view_gradio.py` : Gradio UI view
- `view_streamlit.py` : Streamlit UI view
- `main.py` : Flask-based UI launcher (choose Gradio/Streamlit in browser)
- `model.py` : Core functions for color extraction, litmus bar generation, frame extraction, etc.
- `.st_tmp_frames/`
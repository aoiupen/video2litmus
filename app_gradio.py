import gradio as gr
from adapter_gradio import gradio_analyze

iface = gr.Interface(
    fn=gradio_analyze,
    inputs=[
        gr.File(label="Video (.mp4)"),
        gr.Slider(0, 99, value=0, label="Frame Position"),
        gr.Slider(10, 100, value=30, label="Number of Frames"),
        gr.Slider(1, 20, value=10, label="Top N Colors")
    ],
    outputs=[
        gr.Image(label="Frame"),
        gr.Image(label="Litmus Bar")
    ],
    live=True  # 슬라이더 드래그 중에도 실시간 반영
)

if __name__ == "__main__":
    iface.launch(inbrowser=True) 
import os
import subprocess
import sys
import threading
import time
import webbrowser
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

# 포트 설정
GRADIO_PORT = 7860
STREAMLIT_PORT = 8501

# 서버 프로세스 핸들 저장
server_processes = {}

def run_gradio():
    # Gradio 서버 실행
    subprocess.Popen([sys.executable, "view_gradio.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_streamlit():
    # Streamlit 서버 실행
    subprocess.Popen(["streamlit", "run", "view_streamlit.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route("/")
def index():
    return render_template_string('''
    <h2>플랫폼 선택</h2>
    <form action="/launch/gradio" method="post"><button type="submit">Gradio로 실행</button></form>
    <form action="/launch/streamlit" method="post"><button type="submit">Streamlit으로 실행</button></form>
    ''')

@app.route("/launch/gradio", methods=["POST"])
def launch_gradio():
    threading.Thread(target=run_gradio, daemon=True).start()
    time.sleep(1.5)
    return redirect("/")

@app.route("/launch/streamlit", methods=["POST"])
def launch_streamlit():
    threading.Thread(target=run_streamlit, daemon=True).start()
    time.sleep(2.5)
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000, debug=False) 
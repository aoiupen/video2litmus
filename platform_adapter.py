import typer
import subprocess
import sys
import os

app = typer.Typer()

@app.command()
def streamlit():
    subprocess.run([sys.executable, "app_streamlit.py"])

@app.command()
def gradio():
    subprocess.run([sys.executable, "app_gradio.py"])

if __name__ == "__main__":
    app() 
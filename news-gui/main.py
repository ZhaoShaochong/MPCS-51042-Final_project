from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
async def run_streamlit():
    # 启动 Streamlit 脚本
    result = subprocess.run(
        ["streamlit", "run", "news_gui.py"], capture_output=True, text=True
    )
    return {"stdout": result.stdout, "stderr": result.stderr}
from fastapi import FastAPI
import asyncio
import subprocess

app = FastAPI()

@app.get("/")
async def run_streamlit():
    # Run the Streamlit app asynchronously
    result = await asyncio.to_thread(subprocess.run, 
                                      ["streamlit", "run", "news_gui.py"], 
                                      capture_output=True, 
                                      text=True)
    return {"stdout": result.stdout, "stderr": result.stderr}
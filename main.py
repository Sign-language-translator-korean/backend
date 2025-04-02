from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "수어 번역기 API입니다."}

class TextInput(BaseModel):
    text: str

@app.post("/translate/text")
def translate_text(input: TextInput):
    # 수어 영상 생성 로직 추가 필요
    video_url = f"http://localhost:8000/static/videos/{input.text}.mp4"
    return {"translated_video": video_url}

@app.post("/translate/video")
def translate_video(file: UploadFile = File(...)):
    return {"translated_text": f"{file.filename}에 관한 텍스트 생성"}
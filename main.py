from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

# Sign2Txt import
from sign2txt import process_video

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
    # 텍스트 -> 영상 생성 로직 필요
    video_url = f"http://localhost:8000/static/videos/{input.text}.mp4"
    return {"translated_video": video_url}

@app.post("/translate/video")
async def translate_video(file: UploadFile = File(...)):
    # 비디오 파일 임시 저장
    file_location = os.path.join("temp_video", file.filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
    with open(file_location, "wb") as f:
        f.write(await file.read())

    try:
        # 비디오 처리
        output_video_path = os.path.join("output_video", file.filename)
        result_text = process_video(file_location, output_path=output_video_path)

        # 텍스트 결과 반환
        return {"translated_text": result_text, "output_video": f"/static/videos/{file.filename}"}

    except Exception as e:
        return {"error": f"예측 실패: {str(e)}"}

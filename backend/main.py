import yt_dlp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
OUTPUT_DIR = Path("downloads")
OUTPUT_DIR.mkdir(exist_ok=True)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://app.pinnsystem.com",
    "https://pinnsystem.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str
    format: str

@app.post("/downloads/")
def download_video(request: DownloadRequest):
    try:
        ydl_opts = {
            'outtmpl': str(OUTPUT_DIR / '%(title)s.%(ext)s'),
            'quiet': True
        }

        if request.format == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }]
            })
        else:
            ydl_opts.update({'format': 'bestvideo+bestaudio/best'})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            file_name = ydl.prepare_filename(info).replace(".webm", ".mp3") if request.format == "mp3" else ydl.prepare_filename(info)

        return {"message": "Download completed", "file": file_name}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

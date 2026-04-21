from fastapi import FastAPI
import subprocess
import re

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mesin Pinky Nime v2 Aktif!"}

@app.get("/get_video")
def get_video(title: str, is_series: str = "false", season: int = 1, episode: int = 1):
    try:
        # Menggunakan V3 (API Aplikasi Android) untuk Full Movie
        if is_series.lower() == "true":
            # Command untuk TV Series
            cmd = f'moviebox v3 download-series "{title}" -s {season} -e {episode} --test --verbose'
        else:
            # Command untuk Film
            cmd = f'moviebox v3 download-movie "{title}" --test --verbose'
        
        # Jalankan mesin CLI Simatwa secara virtual di Vercel
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = process.communicate()
        
        # Output terminal digabungkan
        full_log = out + "\n" + err
        
        # Radar Regex untuk menangkap link m3u8 atau mp4 dari log Vercel
        stream_url = ""
        match = re.search(r'(https?://[^\s"\'\[\]]+\.(?:m3u8|mp4)[^\s"\'\[\]]*)', full_log)
        
        if match:
            stream_url = match.group(1)

        return {
            "status": "success",
            "title": title,
            "stream_url": stream_url,
            "debug_log": full_log # Munculkan log kalau gagal untuk kita pantau
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

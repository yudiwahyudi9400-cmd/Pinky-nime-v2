from fastapi import FastAPI
import subprocess
import re
import sys

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mesin Pinky Nime v2 Aktif!"}

@app.get("/get_video")
def get_video(title: str, is_series: str = "false", season: int = 1, episode: int = 1):
    try:
        # Gunakan path Python asli milik Vercel agar perintah dikenali
        python_bin = sys.executable
        
        # Tambahkan --yes agar mesin tidak nyangkut meminta konfirmasi
        if is_series.lower() == "true":
            cmd = [python_bin, "-m", "moviebox_api", "v3", "download-series", title, "-s", str(season), "-e", str(episode), "--test", "--verbose", "--yes"]
        else:
            cmd = [python_bin, "-m", "moviebox_api", "v3", "download-movie", title, "--test", "--verbose", "--yes"]
        
        # Jalankan mesin CLI tanpa shell=True agar lebih stabil di Vercel
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = process.communicate()
        
        # Gabungkan semua output terminal
        full_log = (out or "") + "\n" + (err or "")
        
        # Radar Regex yang lebih ganas untuk menangkap link m3u8 atau mp4
        stream_url = ""
        match = re.search(r'(https?://[^\s"\'\[\]]+\.(?:m3u8|mp4)[^\s"\'\[\]]*)', full_log)
        
        if match:
            stream_url = match.group(1)

        return {
            "status": "success",
            "title": title,
            "stream_url": stream_url,
            # Jika berhasil, jangan tampilkan log kotor. Jika gagal, tampilkan log-nya.
            "debug_log": full_log if not stream_url else "Video berhasil diekstrak!"
        }
    except Exception as e:
        return {"status": "error", "message": "Crash: " + str(e), "debug_log": str(e)}

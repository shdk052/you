import yt_dlp
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_audio():
    link = request.json.get('link')
    if not link:
        return jsonify({'status': 'error', 'message': 'לא נשלח קישור.'}), 400

    try:
        # Ensure the downloads directory exists
        download_dir = 'downloads'
        os.makedirs(download_dir, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',  # הורד רק אודיו
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # המר ל-MP3
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                # הסרנו את 'ffmpeg_location', כיוון שהוא גרם לשגיאת Python קודם לכן.
            }],
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # שם הקובץ: שם הסרטון, בתיקיית הורדות
            'noplaylist': True,  # הורד רק סרטון אחד
        }
        
        # *** הוספנו פה לוגיקה נוספת: הכרחה להתקנת ffmpeg באמצעות yt-dlp אם הוא חסר ***
        # yt-dlp יכולה להתקין את הכלים החסרים לה אם נדרש
        import subprocess
        try:
             subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
             # אם ffmpeg לא נמצא, ננסה להכריח עדכון/התקנה
             print("ffmpeg not found in PATH. Attempting yt-dlp update/install...")
             subprocess.run(['yt-dlp', '-U'], check=True) # זה ינסה לעדכן, ובתהליך יכול להוריד קבצים נוספים.
             
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        return jsonify({'status': 'success', 'message': '✅ השיר הורד בהצלחה!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'אירעה שגיאה: {str(e)}'}), 500

# הסרנו את if __name__ == '__main__': כדי לאפשר ל-Gunicorn לרוץ ישירות.

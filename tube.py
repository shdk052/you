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
            # הוספת ffmpeg_location: 'ffmpeg' גורמת ל-yt-dlp לחפש את הכלי
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # המר ל-MP3
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                'ffmpeg_location': 'ffmpeg', # הוספנו את זה כדי לעזור ל-yt-dlp למצוא את הכלי
            }],
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # שם הקובץ: שם הסרטון, בתיקיית הורדות
            'noplaylist': True,  # הורד רק סרטון אחד
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        return jsonify({'status': 'success', 'message': '✅ השיר הורד בהצלחה!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'אירעה שגיאה: {str(e)}'}), 500

# הסרנו את if __name__ == '__main__': כדי לאפשר ל-Gunicorn לרוץ ישירות.
# Gunicorn יקרא את הפקודה הזו: gunicorn --bind 0.0.0.0:$PORT you:app

import yt_dlp
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# הגדרה סטטית של תיקיית התבניות
app.template_folder = 'templates'
# הגדרה סטטית של תיקיית הקבצים הסטטיים (CSS/JS)
app.static_folder = 'static'

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
        
        # *** הגדרות yt-dlp המתוקנות - עוקפות את בעיית הנתיב FFmpeg ***
        ydl_opts = {
            'format': 'bestaudio/best',      # הורד רק אודיו
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,

            'extract_audio': True,           # מאפשר הוצאת אודיו
            'audio_format': 'mp3',           # הפורמט המועדף (MP3)
            'audio_quality': '192K',         # האיכות המועדפת

            # זהו התיקון הקריטי: מורה ל-yt-dlp להשתמש ב-ffmpeg המותקן בנתיב מוגדר
            # מאחר ו-Railway מתקין את ffmpeg, זו הדרך הנכונה לומר ל-yt-dlp למצוא אותו.
            'downloader_options': {
                'ffmpeg_location': 'ffmpeg'
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        return jsonify({'status': 'success', 'message': '✅ השיר הורד בהצלחה!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'אירעה שגיאה: {str(e)}'}), 500

# *** הסרנו את if __name__ == '__main__': כדי לאפשר ל-Gunicorn לרוץ ישירות. ***

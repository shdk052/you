import yt_dlp
import os
from flask import Flask, request, jsonify, render_template, send_file # הוספנו את send_file

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

    download_dir = 'downloads'
    # ודא שהתיקייה קיימת
    os.makedirs(download_dir, exist_ok=True)
    
    # משתנה לשמירת נתיב הקובץ שהורד
    output_filepath = None
    
    class DownloadLogger:
        def debug(self, msg):
            # שיטה לתפוס את שם הקובץ ש-yt-dlp יצר
            if 'Destination' in msg:
                # הנתיב הוא החלק שאחרי 'Destination: '
                nonlocal output_filepath
                output_filepath = msg.split('Destination: ')[-1].strip()
        def info(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass


    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'extract_audio': True,           # מאפשר הוצאת אודיו
            'audio_format': 'mp3',           # הפורמט המועדף (MP3)
            'audio_quality': '192K',
            'logger': DownloadLogger(),      # משתמשים בלוגר כדי לתפוס את שם הקובץ
            'downloader_options': {
                'ffmpeg_location': 'ffmpeg'  # התיקון הקריטי לבעיית הנתיב
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # הורדת הקובץ לשרת
            ydl.download([link])
        
        # *** הוספנו את הלוגיקה לשליחת הקובץ בחזרה למשתמש ***
        if output_filepath and os.path.exists(output_filepath):
             # שלח את הקובץ שהורד חזרה לדפדפן
            response = send_file(output_filepath, 
                                 mimetype='audio/mpeg', 
                                 as_attachment=True,
                                 download_name=os.path.basename(output_filepath))
            
            # נקה את הקובץ מהשרת אחרי השליחה
            @response.call_on_close
            def cleanup():
                 os.remove(output_filepath)
                 
            return response

        else:
            return jsonify({'status': 'error', 'message': 'שגיאה: הקובץ לא נוצר בשרת.'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'אירעה שגיאה: {str(e)}'}), 500

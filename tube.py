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
            }],
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # שם הקובץ: שם הסרטון, בתיקיית הורדות
            'noplaylist': True,  # הורד רק סרטון אחד
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        
        return jsonify({'status': 'success', 'message': '✅ השיר הורד בהצלחה!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'אירעה שגיאה: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




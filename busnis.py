from flask import Flask, render_template, request, jsonify
import yt_dlp
app = Flask(__name__)

def tube():
    link = input("הכנס קישור לסרטון יוטיוב: ")
    
    ydl_opts = {
        'format': 'bestaudio/best',  # הורד רק אודיו
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # המר ל-MP3
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',  # שם הקובץ: שם הסרטון
        'noplaylist': True,  # הורד רק סרטון אחד
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    
    print("✅ השיר הורד בהצלחה!")


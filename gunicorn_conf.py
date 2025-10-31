# gunicorn_conf.py
# הגדרת זמן קצוב ב-Workers (בשניות). 300 שניות = 5 דקות.
# זה אמור לכסות את כל השירים האפשריים.
timeout = 300
# מספר Workers
workers = 3

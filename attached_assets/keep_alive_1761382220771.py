from flask import Flask
from waitress import serve
import os, threading

app = Flask(__name__)

@app.get("/")
def home():
    return "Arki'Family swear jar is alive 💎"

def _run():
    port = int(os.getenv("PORT", "8080"))
    serve(app, host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=_run, daemon=True)
    t.start()

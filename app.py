from flask import Flask
from routes import main_bp
import threading
import webbrowser
import time
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.register_blueprint(main_bp)

def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "nmap").mkdir(exist_ok=True)
    threading.Thread(target=open_browser).start()
    app.run(debug=False, use_reloader=False)
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import webbrowser
import threading
import os
from pathlib import Path
import sys
import time
import json
import urllib.parse
from modules.nmap import NmapScanner  # Assuming this module exists

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Global progress tracking
progress = {'status': 'Idle', 'message': '', 'percentage': 0, 'filename': None}
reports_dir = Path('reports')
scanner = NmapScanner()
SUPPORTED_LANGS = ["EN", "TR"]

# Custom progress writer for Nmap output
class ProgressWriter:
    def write(self, text):
        global progress
        if "❌ Error" in text:
            progress['status'] = 'Error'
            progress['message'] = text.strip()
        elif text.strip() and "✅" in text:
            progress['message'] = text.strip()
            progress['percentage'] = 100
        elif text.strip():
            try:
                percentage = float(text.split()[-1].replace('%', ''))
                progress['percentage'] = percentage
                progress['message'] = text.split(']')[0].strip()
            except (ValueError, IndexError):
                progress['message'] = text.strip()

    def flush(self):
        pass

# Run analysis in a separate thread
def run_analysis_in_thread(func, *args):
    def wrapper():
        global progress
        try:
            progress['status'] = 'Running'
            func(*args)
            progress['status'] = 'Complete'
            progress['message'] = "Analysis complete!" if args[-1] == 'EN' else "Analiz tamamlandı!"
            progress['percentage'] = 100
            progress['filename'] = args[3]  # Filename is the 4th argument
        except Exception as e:
            progress['status'] = 'Error'
            progress['message'] = f"Error: {str(e)}"
            progress['percentage'] = 0
            flash(f"Error: {str(e)}", "error")
        finally:
            if progress['status'] != 'Error':
                flash("Analysis completed!" if args[-1] == 'EN' else "Analiz tamamlandı!", "success")

    sys.stdout = ProgressWriter()
    sys.stderr = sys.stdout
    thread = threading.Thread(target=wrapper)
    thread.start()

@app.route('/')
def index():
    lang = request.args.get('lang', 'EN')
    return render_template('index.html', langs=SUPPORTED_LANGS, lang=lang)

@app.route('/nmap', methods=['GET', 'POST'])
def nmap():
    global progress
    lang = request.args.get('lang', request.form.get('language', 'EN'))
    if request.method == 'POST':
        hosts = request.form.get('hosts', '').strip()
        ports = request.form.get('ports', '').strip() or None
        arguments = request.form.get('arguments', '').strip()
        if not hosts:
            flash("Hosts field cannot be empty." if lang == 'EN' else "Hedefler alanı boş olamaz.", "error")
            return redirect(url_for('nmap', lang=lang))
        progress = {'status': 'Running', 'message': 'Starting Nmap scan...' if lang == 'EN' else 'Nmap taraması başlıyor...', 'percentage': 0, 'filename': None}
        filename = f"report_{int(time.time())}.json"
        run_analysis_in_thread(scanner.scan_network, hosts, ports, arguments, filename, lang)
        return redirect(url_for('progress_page', lang=lang))
    return render_template('nmap.html', langs=SUPPORTED_LANGS, lang=lang)

@app.route('/about')
def about():
    lang = request.args.get('lang', 'EN')
    return render_template('about.html', langs=SUPPORTED_LANGS, lang=lang)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = request.args.get('lang', request.form.get('language', 'EN'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        github = request.form.get('github', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not email or not message:
            flash("Please fill in all required fields." if lang == 'EN' else "Lütfen tüm zorunlu alanları doldurun.", "error")
            return redirect(url_for('contact', lang=lang))
        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nGitHub: {github}\nMessage: {message}"
        subject = "Contact from Q-Pentest"
        mailto = f"mailto:info@q-e.io?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto)
        flash("Contact form submitted! Check your email client." if lang == 'EN' else "İletişim formu gönderildi! E-posta istemcinizi kontrol edin.", "success")
        return redirect(url_for('contact', lang=lang))
    return render_template('contact.html', langs=SUPPORTED_LANGS, lang=lang)

@app.route('/progress')
def progress_page():
    lang = request.args.get('lang', 'EN')
    return render_template('progress.html', progress=progress, lang=lang)

@app.route('/progress_status')
def progress_status():
    return jsonify(progress)

@app.route('/reports')
def reports():
    lang = request.args.get('lang', 'EN')
    if progress['status'] != 'Complete':
        flash("No reports available yet." if lang == 'EN' else "Henüz rapor yok.", "info")
        return redirect(url_for('index', lang=lang))
    repo_dirs = [d for d in reports_dir.iterdir() if d.is_dir()]
    reports_list = [{'name': repo_dir.name, 'files': [f.name for f in repo_dir.glob('*.json')]} for repo_dir in repo_dirs]
    return render_template('reports.html', reports=reports_list, langs=SUPPORTED_LANGS, lang=lang)

@app.route('/scan_results/<filename>')
def scan_results(filename):
    lang = request.args.get('lang', 'EN')
    report_path = reports_dir / "nmap" / filename
    if not report_path.exists():
        flash("Report not found." if lang == 'EN' else "Rapor bulunamadı.", "error")
        return redirect(url_for('reports', lang=lang))
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('scan_results.html', content=content, filename=filename, lang=lang)

@app.route('/report/<repo_name>/<filename>')
def view_report(repo_name, filename):
    lang = request.args.get('lang', 'EN')
    report_path = reports_dir / repo_name / filename
    if not report_path.exists():
        flash("Report not found." if lang == 'EN' else "Rapor bulunamadı.", "error")
        return redirect(url_for('reports', lang=lang))
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('report_view.html', content=content, repo_name=repo_name, filename=filename, langs=SUPPORTED_LANGS, lang=lang)

@app.route('/tutorial/<lang>')
def tutorial(lang):
    try:
        with open(f'modules/nmap.{lang}.json', 'r') as f:
            data = json.load(f)
        return jsonify(data['module'])
    except FileNotFoundError:
        return jsonify({"error": "Tutorial not found"}), 404

def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "nmap").mkdir(exist_ok=True)  # Ensure nmap subdirectory exists
    threading.Thread(target=open_browser).start()
    app.run(debug=False, use_reloader=False)
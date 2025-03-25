from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import webbrowser
import threading
import os
from pathlib import Path
import sys
import time
import json
import urllib.parse
from modules.nmap import NmapScanner  # Assuming this exists from your Kivy project

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Global variables for progress
progress = {'status': 'Idle', 'message': '', 'percentage': 0}
reports_dir = Path('reports')
scanner = NmapScanner()
SUPPORTED_LANGS = ["EN", "TR"]


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


def run_analysis_in_thread(func, *args):
    def wrapper():
        global progress
        try:
            progress['status'] = 'Running'
            func(*args)
            progress['status'] = 'Complete'
            progress['message'] = "Analysis complete!"
            progress['percentage'] = 100
        except Exception as e:
            progress['status'] = 'Error'
            progress['message'] = f"Error: {str(e)}"
            progress['percentage'] = 0
            flash(f"Error: {str(e)}", "error")
        finally:
            if progress['status'] != 'Error':
                flash("Analysis completed!", "success")

    sys.stdout = ProgressWriter()
    sys.stderr = sys.stdout
    thread = threading.Thread(target=wrapper)
    thread.start()


@app.route('/')
def index():
    return render_template('index.html', langs=SUPPORTED_LANGS)


@app.route('/nmap', methods=['GET', 'POST'])
def nmap():
    global progress
    if request.method == 'POST':
        hosts = request.form.get('hosts', '').strip()
        ports = request.form.get('ports', '').strip() or None
        args = request.form.get('args', '').strip()
        lang = request.form.get('language', 'EN')
        if not hosts:
            flash("Hosts field cannot be empty.", "error")
            return redirect(url_for('nmap'))

        progress = {'status': 'Running', 'message': 'Starting Nmap scan...', 'percentage': 0}
        run_analysis_in_thread(scanner.scan_network, hosts, ports, args)
        return redirect(url_for('progress_page'))

    return render_template('nmap.html', langs=SUPPORTED_LANGS)


@app.route('/about')
def about():
    lang = request.args.get('lang', 'EN')
    return render_template('about.html', lang=lang)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        github = request.form.get('github', '').strip()
        message = request.form.get('message', '').strip()
        lang = request.form.get('language', 'EN')

        if not name or not email or not message:
            flash("Please fill in all required fields.",
                  "error" if lang == 'EN' else "Lütfen tüm zorunlu alanları doldurun.", "error")
            return redirect(url_for('contact'))

        body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nGitHub: {github}\nMessage: {message}"
        subject = "Contact from Q-Pentest"
        mailto = f"mailto:info@q-e.io?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto)
        flash("Contact form submitted! Check your email client.",
              "success" if lang == 'EN' else "İletişim formu gönderildi! E-posta istemcinizi kontrol edin.", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', langs=SUPPORTED_LANGS)


@app.route('/progress')
def progress_page():
    return render_template('progress.html', progress=progress)


@app.route('/reports')
def reports():
    if progress['status'] != 'Complete':
        flash("No reports available yet.", "info")
        return redirect(url_for('index'))

    repo_dirs = [d for d in reports_dir.iterdir() if d.is_dir()]
    reports_list = []
    for repo_dir in repo_dirs:
        reports = [f.name for f in repo_dir.glob('*.md')]
        reports_list.append({'name': repo_dir.name, 'files': reports})

    return render_template('reports.html', reports=reports_list)


@app.route('/report/<repo_name>/<filename>')
def view_report(repo_name, filename):
    report_path = reports_dir / repo_name / filename
    if not report_path.exists():
        flash("Report not found.", "error")
        return redirect(url_for('reports'))

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return render_template('report_view.html', content=content, repo_name=repo_name, filename=filename)


def open_browser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:5000')


if __name__ == "__main__":
    reports_dir.mkdir(exist_ok=True)
    threading.Thread(target=open_browser).start()
    app.run(debug=False, use_reloader=False)
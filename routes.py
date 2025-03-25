from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from modules.nmap import NmapScanner
import threading
import time
import json
from pathlib import Path

# Blueprint for routes
main_bp = Blueprint('main', __name__)
SUPPORTED_LANGS = ['EN', 'TR']  # Adjust as needed

# Global progress tracking
progress = {'status': 'Idle', 'message': '', 'percentage': 0, 'filename': None}
reports_dir = Path('reports')
scanner = NmapScanner()

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

    import sys
    sys.stdout = ProgressWriter()
    sys.stderr = sys.stdout
    thread = threading.Thread(target=wrapper)
    thread.start()

@main_bp.route('/')
def index():
    lang = request.args.get('lang', 'EN')
    return render_template('index.html', langs=SUPPORTED_LANGS, lang=lang)

@main_bp.route('/nmap', methods=['GET', 'POST'])
def nmap():
    global progress
    lang = request.args.get('lang', request.form.get('language', 'EN'))
    if request.method == 'POST':
        hosts = request.form.get('hosts', '').strip()
        ports = request.form.get('ports', '').strip() or None
        arguments = request.form.get('arguments', '').strip()
        timing = request.form.get('timing', '').strip() or None
        sudo = request.form.get('sudo') == 'on'
        output_format = request.form.get('output_format', 'json')
        script_args = request.form.get('script_args', '').strip() or None
        if not hosts:
            flash("Hosts field cannot be empty." if lang == 'EN' else "Hedefler alanı boş olamaz.", "error")
            return redirect(url_for('main.nmap', lang=lang))
        progress = {'status': 'Running', 'message': 'Starting Nmap scan...' if lang == 'EN' else 'Nmap taraması başlıyor...', 'percentage': 0, 'filename': None}
        filename = f"report_{int(time.time())}.json"
        run_analysis_in_thread(scanner.scan_network, hosts, ports, arguments, filename, lang, timing=timing, sudo=sudo, output_format=output_format, script_args=script_args)
        return redirect(url_for('main.progress_page', lang=lang))
    return render_template('nmap.html', langs=SUPPORTED_LANGS, lang=lang)

@main_bp.route('/tools')
def tools():
    lang = request.args.get('lang', 'EN')
    return render_template('tools.html', lang=lang)

@main_bp.route('/progress')
def progress_page():
    lang = request.args.get('lang', 'EN')
    return render_template('progress.html', progress=progress, lang=lang)

@main_bp.route('/progress_status')
def progress_status():
    return jsonify(progress)

@main_bp.route('/reports')
def reports():
    lang = request.args.get('lang', 'EN')
    repo_dirs = [d for d in reports_dir.iterdir() if d.is_dir()]
    reports_list = [{'name': d.name, 'files': [f.name for f in d.glob('*.json')]} for d in repo_dirs]
    if not reports_list and progress['status'] != 'Complete':
        return render_template('reports.html', reports=[], message=("No reports available yet." if lang == 'EN' else "Henüz rapor yok."), lang=lang)
    return render_template('reports.html', reports=reports_list, lang=lang)

@main_bp.route('/about')
def about():
    lang = request.args.get('lang', 'EN')
    return render_template('about.html', langs=SUPPORTED_LANGS, lang=lang)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = request.args.get('lang', 'EN')
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        language = request.form.get('language', lang)
        # Add logic to process the form (e.g., send email, save to DB)
        flash("Message sent successfully!" if language == 'EN' else "Mesaj başarıyla gönderildi!", "success")
        return redirect(url_for('main.contact', lang=language))
    return render_template('contact.html', langs=SUPPORTED_LANGS, lang=lang)

@main_bp.route('/scan_results/<filename>')
def scan_results(filename):
    lang = request.args.get('lang', 'EN')
    report_path = reports_dir / "nmap" / filename
    if not report_path.exists():
        flash("Report not found." if lang == 'EN' else "Rapor bulunamadı.", "error")
        return redirect(url_for('main.reports', lang=lang))
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('scan_results.html', content=content, filename=filename, lang=lang)

@main_bp.route('/report/<repo_name>/<filename>')
def view_report(repo_name, filename):
    lang = request.args.get('lang', 'EN')
    report_path = reports_dir / repo_name / filename
    if not report_path.exists():
        flash("Report not found." if lang == 'EN' else "Rapor bulunamadı.", "error")
        return redirect(url_for('main.reports', lang=lang))
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('report_view.html', content=content, repo_name=repo_name, filename=filename, langs=SUPPORTED_LANGS, lang=lang)

@main_bp.route('/tutorial/<lang>')
def tutorial(lang):
    try:
        with open(f'modules/nmap.{lang}.json', 'r') as f:
            data = json.load(f)
        return jsonify(data['module'])
    except FileNotFoundError:
        return jsonify({"error": "Tutorial not found"}), 404


@main_bp.route('/network_traffic_sniffer')
def network_traffic_sniffer():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Network Traffic Sniffer', lang=lang)

@main_bp.route('/modem_firmware_update_check')
def modem_firmware_update_check():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Modem Firmware Update Check', lang=lang)

@main_bp.route('/device_eol_check')
def device_eol_check():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Device EOL Check', lang=lang)

@main_bp.route('/db_server_detector')
def db_server_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='DB Server Detector', lang=lang)

@main_bp.route('/android_detector')
def android_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Android Detector', lang=lang)

@main_bp.route('/iphone_detector')
def iphone_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='iPhone Detector', lang=lang)

@main_bp.route('/linux_detector')
def linux_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Linux Detector', lang=lang)

@main_bp.route('/windows_server_detector')
def windows_server_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Windows Server Detector', lang=lang)

@main_bp.route('/windows_detector')
def windows_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Windows Detector', lang=lang)

@main_bp.route('/macos_detector')
def macos_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='MacOS Detector', lang=lang)

@main_bp.route('/dns_server_detector')
def dns_server_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='DNS Server Detector', lang=lang)

@main_bp.route('/ftp_server_detector')
def ftp_server_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='FTP Server Detector', lang=lang)

@main_bp.route('/firewall_detector')
def firewall_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Firewall Detector', lang=lang)

@main_bp.route('/webserver_detector')
def webserver_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='WebServer Detector', lang=lang)

@main_bp.route('/password_leaked_controller')
def password_leaked_controller():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Password Leaked Controller', lang=lang)

@main_bp.route('/wifi_admin_panel_controller')
def wifi_admin_panel_controller():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Wifi Admin Panel Controller', lang=lang)

@main_bp.route('/wifi_deauth_detector')
def wifi_deauth_detector():
    lang = request.args.get('lang', 'EN')
    return render_template('placeholder.html', tool_name='Wifi / Deauth Detector and Defender', lang=lang)
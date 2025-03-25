# Create directories
New-Item -ItemType Directory -Force -Path "q-pentest\modules"
New-Item -ItemType Directory -Force -Path "q-pentest\templates"
New-Item -ItemType Directory -Force -Path "q-pentest\static"
New-Item -ItemType Directory -Force -Path "q-pentest\reports"

# app.py
@"
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import importlib.util
from pathlib import Path
import json
import xml.etree.ElementTree as ElementTree
import logging
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
SUPPORTED_LANGS = ['EN', 'TR']

logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

modules_dir = Path('modules')
modules = {}

def load_modules():
    for py_file in modules_dir.glob('*.py'):
        try:
            module_name = py_file.stem
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[module_name] = {
                'module': module,
                'docs': {},
                'xml': ElementTree.parse(modules_dir / f'{module_name}.xml').getroot()
            }
            for lang in SUPPORTED_LANGS:
                json_path = modules_dir / f'{module_name}.{lang}.json'
                if json_path.exists():
                    with open(json_path, 'r') as f:
                        modules[module_name]['docs'][lang] = json.load(f)
        except Exception as e:
            logging.error(f"Failed to load module {py_file}: {str(e)}")

load_modules()

@app.route('/')
def index():
    return render_template('base.html', modules=modules.keys(), lang='EN', theme='light')

@app.route('/module/<module_name>')
def module_page(module_name):
    if module_name not in modules:
        flash("Module not found.", "error")
        return redirect(url_for('index'))
    lang = request.args.get('lang', 'EN')
    return render_template('module.html', module_name=module_name, module=modules[module_name], lang=lang, theme='light')

@app.route('/module/<module_name>/<function_name>', methods=['GET', 'POST'])
def module_function(module_name, function_name):
    if module_name not in modules:
        flash("Module not found.", "error")
        return redirect(url_for('index'))

    module_data = modules[module_name]
    function = getattr(module_data['module'], function_name, None)
    if not function:
        flash("Function not found.", "error")
        return redirect(url_for('module_page', module_name=module_name))

    lang = request.args.get('lang', 'EN')
    function_params = module_data['xml'].find(f".//function[@name='{function_name}']")
    if function_params is None:
        flash("Function parameters not defined in XML.", "error")
        return redirect(url_for('module_page', module_name=module_name))

    params = [{'name': p.get('name'), 'type': p.get('type'), 'required': p.get('required') == 'true'}
              for p in function_params.findall('param')]

    if request.method == 'POST':
        try:
            form_params = {param['name']: request.form.get(param['name']) for param in params}
            result = function(**form_params)
            report_path = f"reports/{module_name}_{function_name}_{os.urandom(4).hex()}.txt"
            with open(report_path, 'w') as f:
                f.write(str(result))
            flash("Operation successful. Report saved.", "success")
            return render_template('module.html', module_name=module_name, module=module_data, lang=lang, result=result)
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            logging.error(f"Error in {module_name}.{function_name}: {str(e)}")

    return render_template('module.html', module_name=module_name, module=module_data, lang=lang, function_name=function_name, params=params)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(str(error))
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
"@ | Set-Content -Path "q-pentest\app.py"

# base.html
@"
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q-Pentest - {{ module_name | default('Home') }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <link rel="manifest" href="{{ url_for('static', filename='manifest.json') }}">
</head>
<body class="{{ theme }}">
    {% include 'header.html' %}
    {% include 'drawer.html' %}
    <main>
        {% block content %}{% endblock %}
    </main>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
"@ | Set-Content -Path "q-pentest\templates\base.html"

# header.html
@"
<header>
    <h1>Q-Pentest</h1>
    <nav>
        <a href="{{ url_for('index') }}">Home</a> |
        <a href="#">Reports</a>
        <select id="language" onchange="changeLanguage(this.value)">
            {% for lang_code in ['EN', 'TR'] %}
                <option value="{{ lang_code }}" {% if lang_code == lang %}selected{% endif %}>{{ lang_code }}</option>
            {% endfor %}
        </select>
        <button id="theme-toggle" onclick="toggleTheme()">Toggle Theme</button>
    </nav>
</header>
"@ | Set-Content -Path "q-pentest\templates\header.html"

# drawer.html
@"
<aside class="drawer">
    <h2>Modules</h2>
    <ul>
        {% for module in modules %}
            <li><a href="{{ url_for('module_page', module_name=module) }}?lang={{ lang }}">{{ module }}</a></li>
        {% endfor %}
    </ul>
</aside>
"@ | Set-Content -Path "q-pentest\templates\drawer.html"

# module.html
@"
{% extends 'base.html' %}
{% block content %}
    <h2>{{ module_name }}</h2>
    {% if function_name %}
        <form method="POST" class="form-container">
            {% for param in params %}
                <label>{{ param['name'] }} ({{ param['type'] }}):</label>
                <input type="{{ 'text' if param['type'] == 'str' else 'checkbox' if param['type'] == 'bool' else 'number' }}"
                       name="{{ param['name'] }}" {% if param['required'] %}required{% endif %}>
            {% endfor %}
            <input type="submit" value="Run {{ function_name }}">
        </form>
        {% if result %}
            <div id="result">{{ result | safe }}</div>
        {% endif %}
    {% else %}
        <ul>
            {% for function in module.xml.findall('.//function') %}
                <li><a href="{{ url_for('module_function', module_name=module_name, function_name=function.get('name')) }}?lang={{ lang }}">{{ function.get('name') }}</a></li>
            {% endfor %}
        </ul>
    {% endif %}
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="flash {{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
{% endblock %}
"@ | Set-Content -Path "q-pentest\templates\module.html"

# 404.html
@"
{% extends 'base.html' %}
{% block content %}
    <h2>404 - Page Not Found</h2>
    <p>Sorry, the page you are looking for does not exist.</p>
    <a href="{{ url_for('index') }}">Go back to Home</a>
{% endblock %}
"@ | Set-Content -Path "q-pentest\templates\404.html"

# 500.html
@"
{% extends 'base.html' %}
{% block content %}
    <h2>500 - Internal Server Error</h2>
    <p>Something went wrong on our end. Please try again later.</p>
    <a href="{{ url_for('index') }}">Go back to Home</a>
{% endblock %}
"@ | Set-Content -Path "q-pentest\templates\500.html"

# styles.css
@"
body.light { background: #fff; color: #000; }
body.dark { background: #333; color: #fff; }
header { padding: 10px; border-bottom: 1px solid #ccc; }
.drawer { float: left; width: 200px; padding: 10px; }
main { margin-left: 220px; padding: 20px; }
.form-container { margin: 20px 0; }
.form-container label { display: block; margin: 5px 0; }
.flash { padding: 10px; margin: 10px 0; }
.flash.success { background: #d4edda; color: #155724; }
.flash.error { background: #f8d7da; color: #721c24; }
"@ | Set-Content -Path "q-pentest\static\styles.css"

# script.js
@"
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('light');
    body.classList.toggle('dark');
    localStorage.setItem('theme', body.classList.contains('dark') ? 'dark' : 'light');
}

function changeLanguage(lang) {
    window.location.search = `?lang=\${lang}`;
}

window.onload = () => {
    const theme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(theme);
};
"@ | Set-Content -Path "q-pentest\static\script.js"

# manifest.json
@"
{
    "name": "Q-Pentest",
    "short_name": "QPentest",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "/static/icon.png",
            "sizes": "192x192",
            "type": "image/png"
        }
    ]
}
"@ | Set-Content -Path "q-pentest\static\manifest.json"

# service-worker.js
@"
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('q-pentest-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/static/styles.css',
                '/static/script.js'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
"@ | Set-Content -Path "q-pentest\static\service-worker.js"

# nmap.py
@"
def scan_network(hosts, ports=None):
    return f"Scanning {hosts} on ports {ports if ports else 'default'}"
"@ | Set-Content -Path "q-pentest\modules\nmap.py"

# nmap.EN.json
@"
{
    "description": "Network scanning module",
    "functions": {
        "scan_network": "Scans a network for open ports"
    }
}
"@ | Set-Content -Path "q-pentest\modules\nmap.EN.json"

# nmap.TR.json
@"
{
    "description": "Ağ tarama modülü",
    "functions": {
        "scan_network": "Ağı açık portlar için tarar"
    }
}
"@ | Set-Content -Path "q-pentest\modules\nmap.TR.json"

# nmap.xml
@"
<module name="nmap">
    <function name="scan_network">
        <param name="hosts" type="str" required="true">Target hosts</param>
        <param name="ports" type="str" required="false">Port range</param>
    </function>
</module>
"@ | Set-Content -Path "q-pentest\modules\nmap.xml"

Write-Host "Q-Pentest project generated successfully!"
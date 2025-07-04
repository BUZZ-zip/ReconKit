from flask import Flask, render_template, jsonify, send_from_directory , request
import os
import json
from urllib.parse import urlparse
import shutil
import re



app = Flask(__name__)



DATA_FOLDER = 'output/data'
SCREENSHOT_FOLDER = 'output'
CONFIG_PATH = os.path.join('page', 'static', 'config.json')

def load_alive_subdomains(domain):
    path = f'output/{domain}/{domain}_alive_urls.txt'
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def extract_subdomain(url):
   
    pattern = r'^(?:https?://)?([^:/]+)'
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    return url

def move_images_to_static(domain):
    src_folder = f'output/{domain}/screen_{domain}'
    dst_folder = f'page/static/img/{domain}/screens'

    if not os.path.exists(src_folder):
        print("Dossier source introuvable.")
        return

    os.makedirs(dst_folder, exist_ok=True)

    for filename in os.listdir(src_folder):
        if filename.endswith('.jpeg') or filename.endswith('.png'):
            shutil.copy2(os.path.join(src_folder, filename), os.path.join(dst_folder, filename))


def load_technologies(domain):
    path = f'output/{domain}/{domain}_tech_all.json'
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def format_url_for_filename(url):
    return url.replace('://', '---').rstrip('/')

def get_screenshot_path(domain, subdomain):
    folder = f'page/static/img/{domain}/screens'
    if not os.path.exists(folder):
        return None

    clean_sub = extract_subdomain(subdomain)


   
    for filename in os.listdir(folder):
   
        clean_filename = filename.replace('https---', '').replace('http---', '')
        clean_filename = re.sub(r'-\d+', '', clean_filename)  # enlève les ports (ex: -443)
        clean_filename = os.path.splitext(clean_filename)[0]  # enlève l'extension

        if clean_filename == clean_sub:
           
            return f"/static/img/{domain}/screens/{filename}"

    return None

def normalize_target(url):
    return url.rstrip('/').lower()
        
def get_subdomain_details(domain):
    subdomains = load_alive_subdomains(domain)
    raw_technologies = load_technologies(domain)
    result = []
    move_images_to_static(domain)

    for sub in subdomains:
        all_techs_for_sub = [
            tech for tech in raw_technologies 
            if normalize_target(tech.get('target', '')) == normalize_target(sub)
        ]

        seen = set()
        unique_techs = []
        for tech in all_techs_for_sub:
            plugins = tech.get('plugins', {})
            http_status = tech.get('http_status')
            http_server = plugins.get('HTTPServer', {}).get('string', [''])[0]
            country = plugins.get('Country', {}).get('string', [''])[0]
            ip = plugins.get('IP', {}).get('string', [''])[0]
            
            key = (http_status, normalize_target(tech.get('target', '')), http_server, country, ip)
            if key not in seen:
                seen.add(key)
                unique_techs.append(tech)

        result.append({
            "name": extract_subdomain(sub),
            "url": sub,
            "screenshot": get_screenshot_path(domain, sub),
            "technologies": unique_techs
        })

    return result

def load_alive_endpoints(domain):
    path = f'output/{domain}/{domain}_alive_endpoints.txt'
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def get_endpoints_details(domain):
    endpoints = load_alive_endpoints(domain)
    result = []
    pattern = re.compile(r'^(.*?)\s*\[(\d{3})\]$')
    
    for line in endpoints:
        match = pattern.match(line)
        if match:
            url = match.group(1)
            status_code = int(match.group(2))
            result.append({
                "url": url,
                "status_code": status_code
            })
        else:
            pass

    return result





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/domains')
def get_domains():
    domains = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith('.json'):
            with open(os.path.join(DATA_FOLDER, filename), 'r') as f:
                data = json.load(f)
                domains.append({
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "status": data.get("status"),
                    "dateAdded": data.get("dateAdded"),
                    "subdomains": data.get("subdomains"),
                    "endpoints": data.get("endpoints")
                })
    return jsonify(domains)

@app.route('/api/domain/<domain>/subdomains')
def get_subdomains(domain):
    subdomains = get_subdomain_details(domain)
    return jsonify(subdomains)


@app.route('/api/domain/<domain>/endpoints')
def get_endpoints(domain):
    endpoints = get_endpoints_details(domain)
    return jsonify(endpoints)




@app.route('/api/domain/<domain_id>')
def get_domain(domain_id):
    path = os.path.join(DATA_FOLDER, f"{domain_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "Not found"}), 404

    with open(path, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/screenshot/<path:path>')
def screenshot(path):
    # ex: /screenshot/tictac.com/screenshot_www_tictac_com.png
    return send_from_directory(SCREENSHOT_FOLDER, path)


@app.route('/load-config', methods=['GET'])
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        return jsonify(config)
    else:
        return jsonify({})


@app.route('/save-config', methods=['POST'])
def save_config():
    if os.path.exists(CONFIG_PATH): 
        print("connais pas ")
    else:
        print('ok')
    config = request.get_json()
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
            print(config)
        return 'Configuration enregistrée avec succès', 200
    except Exception as e:
        return f'Erreur lors de la sauvegarde : {str(e)}', 500




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)

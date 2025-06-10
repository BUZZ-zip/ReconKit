from modules.endpoint_enum.gau import gau
from modules.endpoint_enum.waybackurls import waybackurls
from modules.endpoint_enum.katana import katana
from modules.endpoint_enum.hakrawler import hakrawler
from modules.endpoint_enum.gospider import gospider
from modules.endpoint_enum.getjs import getjs
from modules.endpoint_enum.subjs import subjs
from modules.httpx_endpoint import httpx
import os
from urllib.parse import urlparse
import json
import threading
import re



def extract_js_urls(input_file, output_file, domain):
    js_urls = []

    with open(input_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        match = re.search(r'(https?://[^\s]+\.js(?:[^\s]*)?)', line)
        if match:
            js_url = match.group(1)
            if domain in js_url:
                js_urls.append(js_url)

    with open(output_file, 'w') as out:
        for js_url in js_urls:
            out.write(js_url + '\n')

    print(f"[+] {len(js_urls)} .js URLs extraites et enregistrées dans '{output_file}'.")

def save_results(domain, results, method):
    output_dir = os.path.expanduser(f"~/output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    if method == 'urls':
        filename = os.path.join(output_dir, f"{domain}_endpoints.txt")
    elif method == 'alive':
        filename = os.path.join(output_dir, f"{domain}_alive_endpoints.txt")
    elif method == 'ip':
        filename = os.path.join(output_dir, f"{domain}_ip.txt")
    else:
        print("[!] ERROR during save")
        return

    unique_sorted = sorted(set(results))
    with open(filename, "w") as f:
        for sub in unique_sorted:
            f.write(sub + "\n")

    print(f"[i] Saved {len(unique_sorted)} unique endpoint to {filename}")

def run_tools_endpoint(domain, config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)

    selected_tools = config.get("endpoint_tools", [])

    results = []
    results_lock = threading.Lock()

    js_results = []          
    js_lock = threading.Lock()

    def run_and_collect(tool_func):
        res = tool_func(domain)
        with results_lock:
            results.extend(res)

    def run_and_collect_js(tool_func):
        res = tool_func(domain)
        with js_lock:
            js_results.extend(res)

    threads = []

    if "gau" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(gau,)))

    if "waybackurls" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(waybackurls,)))

    if "katana" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(katana,)))

    if "hakrawler" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(hakrawler,)))

    if "gospider" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(gospider,)))

    

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique_sorted = sorted(set(results))
    print(f"[i] Total unique subdomains found: {len(unique_sorted)}")
    save_results(domain, unique_sorted, 'urls')

    output_dir = os.path.expanduser(f"~/output/{domain}")
    input_urls_file = os.path.join(output_dir, f"{domain}_endpoints.txt")
    js_output_file = os.path.join(output_dir, f"{domain}_js_urls.txt")
    extract_js_urls(input_urls_file, js_output_file,domain)

    threads = []

    if "getJS" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect_js, args=(getjs,)))

    if "subjs" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect_js, args=(subjs,)))



    for t in threads:
        t.start()
    for t in threads:
        t.join()

    js_file = sorted(set(js_results))
    print(f"[i] Total unique js found: {len(js_file)}")


        
    

    
    with open(os.path.join(output_dir, f"{domain}_js_urls.txt"), "r") as f:
        existing_urls = set(line.strip() for line in f if line.strip())

    merged_urls = set(js_file).union(existing_urls)

    with open(os.path.join(output_dir, f"{domain}_js_urls.txt"), "w") as f:
        for url in sorted(merged_urls):
            f.write(url + "\n")

    alive_subdomains = httpx(domain)
    save_results(domain, alive_subdomains, 'alive')

    
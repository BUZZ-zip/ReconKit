from modules.endpoint_enum.gau import gau
from modules.endpoint_enum.waybackurls import waybackurls
from modules.endpoint_enum.waymore1 import waymore
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
from colorama import init, Fore, Style



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


def save_results(domain, results, method):
    output_dir = os.path.expanduser(f"output/{domain}")
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
    
    print(f"{Fore.BLUE}[i]{Fore.RESET} Saved {len(unique_sorted)} subdomains to {filename}")


def read_config(config_path="page/static/config.json"):
    with open(config_path) as f:
        config = json.load(f)

    def get_enabled_tools(section_name):
        tools = config.get(section_name, {})
        enabled = []
        for tool_name, tool_config in tools.items():
            if isinstance(tool_config, dict) and tool_config.get("enabled"):
                enabled.append(tool_name)
        return enabled

    selected_tools_subdomain = get_enabled_tools("endpoint")
    return selected_tools_subdomain

def run_tools_endpoint(domain, custom_header=None, config_path="page/static/config.json"):
    print(f"\n{Fore.CYAN}[*]{Fore.RESET} Running endpoint enumeration\n")
    with open(config_path) as f:
        config = json.load(f)

    selected_tools = read_config()

    results = []
    results_lock = threading.Lock()

    js_results = []          
    js_lock = threading.Lock()

    def run_and_collect(tool_func):
        res = tool_func(domain, custom_header=custom_header)
        with results_lock:
            results.extend(res)

    def run_and_collect_js(tool_func):
        res = tool_func(domain, custom_header=custom_header)
        with js_lock:
            js_results.extend(res)

    threads = []

    if "gau" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(gau,)))

    if "waybackurls" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(waybackurls,)))

    if "waymore" in selected_tools:
        threads.append(threading.Thread(target=run_and_collect, args=(waymore,)))


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
    print(f"{Fore.BLUE}[i]{Fore.RESET} Total unique endpoints found: {len(unique_sorted)}")

    save_results(domain, unique_sorted, 'urls')

    output_dir = os.path.expanduser(f"output/{domain}")
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
    

    
    with open(os.path.join(output_dir, f"{domain}_js_urls.txt"), "r") as f:
        existing_urls = set(line.strip() for line in f if line.strip())

    merged_urls = set(js_file).union(existing_urls)

    print(f"{Fore.BLUE}[i]{Fore.RESET} Total unique js found: {len(merged_urls)}")

    with open(os.path.join(output_dir, f"{domain}_js_urls.txt"), "w") as f:
        for url in sorted(merged_urls):
            f.write(url + "\n")

    alive_endpoints = httpx(domain, custom_header=custom_header)
    save_results(domain, alive_endpoints, 'alive')

    return alive_endpoints
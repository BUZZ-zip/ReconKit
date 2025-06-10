from modules.subdomain_enum.subfinder import subfinder
from modules.subdomain_enum.findomain import findomain
from modules.subdomain_enum.assetfinder import assetfinder
from modules.subdomain_enum.crt import crtsh
from modules.subdomain_enum.amass import amass
from modules.subdomain_enum.sublist3r import sublist3r
from modules.subdomain_enum.chaos import chaos
from modules.httpx_subdomain import httpx
import os
import json
import threading
import dns.resolver


def save_results(domain,results,method):
    output_dir = os.path.expanduser(f"~/output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    if method =='urls':
        filename = os.path.join(output_dir, f"{domain}_urls.txt")
        unique_sorted = sorted(set(results))
        with open(filename, "w") as f:
            for sub in unique_sorted:
                f.write(sub + "\n")
    elif method == 'alive':
        filename = os.path.join(output_dir, f"{domain}_alive_urls.txt")
        unique_sorted = sorted(set(results))
        with open(filename, "w") as f:
            for sub in unique_sorted:
                f.write(sub + "\n")
    elif method == 'ip':
        filename = os.path.join(output_dir, f"{domain}_ip.txt")
        unique_sorted = sorted(set(results))
        with open(filename, "w") as f:
            for sub in unique_sorted:
                f.write(sub + "\n")
    else : 
        print("[!] ERROR during save")
        return

    print(f"[i] Saved {len(unique_sorted)} unique subdomains to {filename}")

def run_tools_subdomain(domain, config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)

    selected_tools = config.get("subdomain_tools", [])

    results = []
    results_lock = threading.Lock()

    def run_and_collect(tool_func):
        res = tool_func(domain)
        with results_lock:
            results.extend(res)

    threads = []

    if "subfinder" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(subfinder,))
        threads.append(t)

    if "findomain" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(findomain,))
        threads.append(t)

    if "assetfinder" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(assetfinder,))
        threads.append(t)

    if "crt.sh" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(crtsh,))
        threads.append(t)

    if "amass" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(amass,))
        threads.append(t)

    if "sublist3r" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(sublist3r,))
        threads.append(t)

    if "chaos" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(chaos,))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique_sorted = sorted(set(results))

    print(f"[i] Total unique subdomains found: {len(unique_sorted)}")
    save_results(domain,unique_sorted,'urls')

    alive_subdomain = httpx(domain)
    save_results(domain,alive_subdomain,'alive')


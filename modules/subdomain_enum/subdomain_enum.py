from modules.subdomain_enum.subfinder import subfinder
from modules.subdomain_enum.findomain import findomain
from modules.subdomain_enum.assetfinder import assetfinder
from modules.subdomain_enum.crt import crtsh
from modules.subdomain_enum.sublist3r import sublist3r
from modules.subdomain_enum.chaos import chaos
from modules.subdomain_enum.securitytrails import securitytrails
from modules.subdomain_enum.virustotal import virustotal
from modules.subdomain_enum.alienvault import alienvault
from modules.subdomain_enum.dnsdumpster import dnsdumpster
from modules.subdomain_enum.gowitness import gowitness
from modules.subdomain_enum.whatweb import whatweb
from modules.httpx_subdomain import httpx
import os
import json
import threading
from colorama import init, Fore, Style


def save_results(domain,results,method):
    output_dir = os.path.expanduser(f"output/{domain}")
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

    selected_tools_subdomain = get_enabled_tools("subdomain")
    return selected_tools_subdomain



def run_tools_subdomain(domain, config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)

    selected_tools = read_config()

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

    if "crtsh" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(crtsh,))
        threads.append(t)

    if "sublist3r" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(sublist3r,))
        threads.append(t)

    if "chaos" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(chaos,))
        threads.append(t)
    
    if "securitytrails" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(securitytrails,))
        threads.append(t)

    if "virustotal" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(virustotal,))
        threads.append(t)

    if "alienvault" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(alienvault,))
        threads.append(t)
    
    if "dnsdumpster" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(dnsdumpster,))
        threads.append(t)

    else:
        print(f"{Fore.RED}[!]{Fore.RESET} Pas d'outils selectioné")

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique_sorted = sorted(set(results))

    print(f"{Fore.BLUE}[i]{Fore.RESET} Total unique subdomains found: {len(unique_sorted)}")
    save_results(domain,unique_sorted,'urls')

    alive_subdomain = httpx(domain)
    save_results(domain,alive_subdomain,'alive')
    
    print(f"{Fore.MAGENTA}[~]{Fore.RESET} Alive Subdomain :")
    for subdomain in alive_subdomain:
        print(f"    - {subdomain}")
    

    t2_threads = []

    t2_threads.append(threading.Thread(target=run_and_collect, args=(gowitness,)))
    t2_threads.append(threading.Thread(target=run_and_collect, args=(whatweb,)))

    for t in t2_threads:
        t.start()
    for t in t2_threads:
        t.join()

    return alive_subdomain
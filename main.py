import argparse
import subprocess
import time
import webbrowser
import os
import sys
import json
from modules.subdomain_enum.subdomain_enum import * 
from modules.endpoint_enum.endpoint_enum import *
from modules.param_finder.param_finder import *
import shutil
from colorama import Fore, Style, init
from datetime import datetime
import logging

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
    selected_tools_endpoint = get_enabled_tools("endpoint")
    selected_tools_param = get_enabled_tools("param_tools")

    return selected_tools_subdomain, selected_tools_endpoint, selected_tools_param


def print_banner(domain, output_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    selected_tools_subdomain,selected_tools_endpoint,selected_tools_param=read_config()

    selected_tools_subdomain_str = ", ".join(selected_tools_subdomain)
    selected_tools_endpoint_str = ", ".join(selected_tools_endpoint)
    selected_tools_param_finder_str=", ".join(selected_tools_param)

    banner = f"""
╔════════════════════════════════════════════════╗
║             {Fore.MAGENTA}  ReconKit v1.0 {Fore.RESET}                   ║
╠════════════════════════════════════════════════╣
║ Reconnaissance Automation Tool                 ║
║ GitHub: https://github.com/BUZZ-zip/ReconKit   ║
╚════════════════════════════════════════════════╝

{Fore.BLUE}[i]{Fore.RESET} Selected tools:
    ├── Subdomain enumeration : {selected_tools_subdomain_str}
    ├── Endpoint discovery    : {selected_tools_endpoint_str}
    └── Param Finder          : {selected_tools_param_finder_str}
"""
    print(banner)

def ascii_art():
    banner = fr"""
{Fore.MAGENTA} 
{Fore.RESET}    ____                        {Fore.MAGENTA}__ __ _ __ {Fore.RESET}
   / __ \___  _________  ____ {Fore.MAGENTA} / //_/(_) /_{Fore.RESET}
  / /_/ / _ \/ ___/ __ \/ __ \{Fore.MAGENTA}/ ,<  / / __/{Fore.RESET}
 / _, _/  __/ /__/ /_/ / / / {Fore.MAGENTA}/ /| |/ / /_{Fore.RESET}
/_/ |_|\___/\___/\____/_/ /_{Fore.MAGENTA}/_/ |_/_/\__/ {Fore.RESET}
{Fore.RESET}
    """

    print(banner)



def load_existing_domain_data(domain):
    path = f"./output/data/{domain}.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return {}

def write_domain_data(domain, data):
    path = f"./output/data/{domain}.json"
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def save_domain_result(domain,new_subdomains=None, new_endpoints=None):


    data = load_existing_domain_data(domain)  # Charge depuis le fichier ou DB

    # Garde les anciens si pas de nouveaux fournis
    if new_subdomains is not None:
        data['subdomains'] = len(new_subdomains)
    if new_endpoints is not None:
        data['endpoints'] = len(new_endpoints)

    # Autres infos mises à jour si besoin
    data['id'] = domain
    data['name'] = domain
    data['status'] = 'analyzed'
    data['dateAdded'] = data['dateAdded'] = datetime.now().isoformat()

    # Enregistre les données mises à jour
    write_domain_data(domain, data)
   
def config():
    with open(os.devnull, 'w') as FNULL:
        subprocess.Popen(
            ["python3", "page/app.py"],
            stdout=FNULL,
            stderr=FNULL
        )
        webbrowser.open("http://127.0.0.1:5000/?tab=config")


def main(a):
    subdomains=''
    endpoints=''

    parser = argparse.ArgumentParser(description="Recon Tool - Pipeline de reconnaissance")
    parser.add_argument("-d", "--domain", help="Domaine cible (ex: example.com)")
    parser.add_argument("-open", "--open_page", action="store_true", help="Ouvre une page web avec les résultats")
    parser.add_argument("-c","--config", action="store_true", help="Ouvre un menu pour sélectionner les outils")
    parser.add_argument("-m","--module", choices=["subdomain", "endpoint","paramfinder"], help="Choix du module à exécuter")
    parser.add_argument("-H","--header", help="Choix du header à utiliser")
    args = parser.parse_args()

    domain = args.domain
    open_result = args.open_page
    config_menu=args.config
    custom_header = args.header
    output_dir = os.path.expanduser(f"output/{domain}")
    print_banner(domain, output_dir)

    if config_menu:
        print("[i] Ouverture de Flask depuis page/app.py ...")
        config()

    if domain:
        print(f"{Fore.BLUE}[i]{Fore.RESET} Domaine : {domain}")

        subdomains = None
        endpoints = None

        if args.module == "subdomain":
            subdomains = run_tools_subdomain(domain, custom_header=custom_header)
        elif args.module == "endpoint":
            endpoints = run_tools_endpoint(domain, custom_header=custom_header)
        elif args.module == "paramfinder":
            run_tools_paramfinder(domain, custom_header=custom_header)
        else:
                subdomains = run_tools_subdomain(domain, custom_header=custom_header)
                endpoints = run_tools_endpoint(domain, custom_header=custom_header)
                
        
        save_domain_result(domain,subdomains,endpoints)
    
    if open_result and a:
        a=False
        subprocess.Popen([sys.executable, "page/app.py"])
        time.sleep(1)
        

if __name__ == "__main__":
    a=True
    start_time = time.time()
    ascii_art()
    main(a)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n{Fore.BLUE}[i]{Fore.RESET} Total execution time: {elapsed_time:.2f} seconds")

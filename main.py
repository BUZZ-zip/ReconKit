import argparse
import subprocess
import time
import webbrowser
import os
import sys
from simple_term_menu import TerminalMenu
import json
from modules.subdomain_enum.subdomain_enum import * 
from modules.endpoint_enum.endpoint_enum import *
import shutil
from colorama import Fore, Style, init
from datetime import datetime

def read_config(config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)

    selected_tools_subdomain = config.get("subdomain_tools", [])
    selected_tools_endpoint = config.get("endpoint_tools", [])
    return selected_tools_subdomain,selected_tools_endpoint


def print_banner(domain, output_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    selected_tools_subdomain,selected_tools_endpoint=read_config()

    selected_tools_subdomain_str = ", ".join(selected_tools_subdomain)
    selected_tools_endpoint_str = ", ".join(selected_tools_endpoint)

    banner = f"""
╔════════════════════════════════════════════════╗
║             {Fore.MAGENTA}  ReconKit v1.0 {Fore.RESET}                   ║
╠════════════════════════════════════════════════╣
║ Reconnaissance Automation Tool                 ║
║ GitHub: https://github.com/BUZZ-zip/ReconKit   ║
╚════════════════════════════════════════════════╝

[+] Selected tools:
    ├── Subdomain enumeration : {selected_tools_subdomain_str}
    ├── Endpoint discovery    : {selected_tools_endpoint_str}
    └── JS & Link extraction  : LinkFinder, GetJS, SubJS (à venir)
"""
    print(banner)

def ascii_art():
    banner = fr"""
{Fore.MAGENTA} 
    ____                        __ __ _ __ 
   / __ \___  _________  ____  / //_/(_) /_
  / /_/ / _ \/ ___/ __ \/ __ \/ ,<  / / __/
 / _, _/  __/ /__/ /_/ / / / / /| |/ / /_  
/_/ |_|\___/\___/\____/_/ /_/_/ |_/_/\__/ 
{Fore.RESET}
    """

    print(banner)



def config():
    subdomain_tools_list = [
        "subfinder",
        "findomain",
        "assetfinder",
        "crt.sh",
        "amass",
        "sublist3r",
        "chaos"
    ]
    endpoint_tools_list = [
        "gau",
        "waybackurls",
        "waymore",
        "katana",
        "hakrawler",
        "gospider",
        "getJS",
        "subjs",
        "linkfinder"
        ]

    config_path = "config.json"
    selected_subdomains = []
    selected_endpoints = []
    api_keys = {}

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                old_config = json.load(f)
                selected_subdomains = old_config.get("subdomain_tools", [])
                selected_endpoints = old_config.get("endpoint_tools", [])
                old_api_keys = old_config.get("api_keys", {})
            except json.JSONDecodeError:
                old_api_keys = {}
    else:
        old_api_keys = {}

    def is_tool_installed(tool):
        return shutil.which(tool) is not None

    subdomain_tools_list = [
        tool for tool in subdomain_tools_list if is_tool_installed(tool) or tool == "crt.sh" or tool == "chaos"
    ]
    endpoint_tools_list = [
        tool for tool in endpoint_tools_list if is_tool_installed(tool)
    ]

    print("\rChoisis les outils de découverte de sous-domaines :")
    terminal_menu_subdomains = TerminalMenu(
        subdomain_tools_list,
        multi_select=True,
        show_multi_select_hint=True,
        title="Sous-domaines (utilise espace pour sélectionner, entrée pour valider)",
        preselected_entries=[
            subdomain_tools_list.index(tool)
            for tool in selected_subdomains if tool in subdomain_tools_list
        ]
    )
    selected_subdomains_indices = terminal_menu_subdomains.show()
    selected_subdomains = [subdomain_tools_list[i] for i in selected_subdomains_indices]

    print("\rChoisis les outils de découverte d'endpoints :")
    terminal_menu_endpoints = TerminalMenu(
        endpoint_tools_list,
        multi_select=True,
        show_multi_select_hint=True,
        title="Endpoints (utilise espace pour sélectionner, entrée pour valider)",
        preselected_entries=[
            endpoint_tools_list.index(tool)
            for tool in selected_endpoints if tool in endpoint_tools_list
        ]
    )
    selected_endpoints_indices = terminal_menu_endpoints.show()
    selected_endpoints = [endpoint_tools_list[i] for i in selected_endpoints_indices]


    if "chaos" in selected_subdomains:
        if "chaos" not in old_api_keys or not old_api_keys["chaos"].strip():
            api_keys["chaos"] = input("🔑 Entrez votre clé API pour Chaos : ").strip()
            os.environ["PDCP_API_KEY"] = api_keys["chaos"]
        else:
            print("Clé API Chaos déjà présente — utilisation de celle existante.")
            api_keys["chaos"] = old_api_keys["chaos"]


    if selected_subdomains or selected_endpoints:
        config_data = {
            "subdomain_tools": selected_subdomains,
            "endpoint_tools": selected_endpoints,
            "api_keys": api_keys
        }
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
        print("\nSélection sauvegardée dans 'config.json'")
    else:
        print("\nAucun outil sélectionné.")


def main():
    parser = argparse.ArgumentParser(description="Recon Tool - Pipeline de reconnaissance")
    parser.add_argument("-d", "--domain", help="Domaine cible (ex: example.com)")
    parser.add_argument("-open", "--open_page", action="store_true", help="Ouvre une page web avec les résultats")
    parser.add_argument("-c","--config", action="store_true", help="Ouvre un menu pour sélectionner les outils")
    parser.add_argument("--module", choices=["subdomain", "endpoint"], help="Choix du module à exécuter")
    args = parser.parse_args()

    domain = args.domain
    open_result = args.open_page
    config_menu=args.config
    output_dir = os.path.expanduser(f"~/output/{domain}")
    print_banner(domain, output_dir)

    if config_menu:
        config()

    if domain:
        print(f"[i] Domaine : {domain}")
        if args.module == "subdomain":
            run_tools_subdomain(domain)
        elif args.module == "endpoint":
            run_tools_endpoint(domain)
        else:
                run_tools_subdomain(domain)
                run_tools_endpoint(domain)
        

    if open_result:
        
        subprocess.Popen([sys.executable, "app.py"])
        
        time.sleep(1)

        webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    start_time = time.time()
    ascii_art()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n[i] Total execution time: {elapsed_time:.2f} seconds")

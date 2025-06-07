import argparse
import subprocess
import time
import webbrowser
import os
import sys
from simple_term_menu import TerminalMenu
import json
from modules.subdomain_enum.subdomain_enum import * 
from modules.endpoint_enum import *




def config():
    # Listes des outils
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
    "katana",
    "dirhunt",
    "hakrawler",
    "linkfinder",
    "getjs",
    "gospider",
    "subjs",
    "webanalyze",
    "nuclei"
]

    print("Choisis les outils de découverte de sous-domaines :")
    terminal_menu_subdomains = TerminalMenu(
        subdomain_tools_list,
        multi_select=True,
        show_multi_select_hint=True,
        title="Sous-domaines (utilise espace pour sélectionner, entrée pour valider)"
    )
    selected_subdomains_indices = terminal_menu_subdomains.show()
    selected_subdomains = [subdomain_tools_list[i] for i in selected_subdomains_indices]

    print("\nChoisis les outils de découverte d'endpoints :")
    terminal_menu_endpoints = TerminalMenu(
        endpoint_tools_list,
        multi_select=True,
        show_multi_select_hint=True,
        title="Endpoints (utilise espace pour sélectionner, entrée pour valider)"
    )
    selected_endpoints_indices = terminal_menu_endpoints.show()
    selected_endpoints = [endpoint_tools_list[i] for i in selected_endpoints_indices]

    if selected_subdomains or selected_endpoints:
        print("\nOutils sélectionnés :")
        print(" - Sous-domaines :", selected_subdomains)
        print(" - Endpoints :", selected_endpoints)

        config_data = {
            "subdomain_tools": selected_subdomains,
            "endpoint_tools": selected_endpoints
        }
        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4)
        print("\nSélection sauvegardée dans 'config.json'")
    else:
        print("\nAucun outil sélectionné.")





def main():
    parser = argparse.ArgumentParser(description="Recon Tool - Pipeline de reconnaissance")
    parser.add_argument("-d", "--domain", help="Domaine cible (ex: example.com)")
    parser.add_argument("-open", "--open_page", action="store_true", help="Ouvre une page web avec les résultats")
    parser.add_argument("-c","--config", action="store_true", help="Ouvre un menu pour sélectionner les outils")
    parser.add_argument("--all", action="store_true", help="Exécute tous les outils")
    args = parser.parse_args()

    domain = args.domain
    open_result = args.open_page
    config_menu=args.config


    if config_menu:
        config()

    if domain:
        print(f"[i] Domaine : {domain}")
        run_tools(args.domain)
        

    if open_result:
        
        subprocess.Popen([sys.executable, "app.py"])
        
        time.sleep(1)

        webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n[i] Total execution time: {elapsed_time:.2f} seconds")

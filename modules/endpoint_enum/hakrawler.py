import subprocess
import os
from colorama import Fore,Style

def run_command_input(cmd, input_value, output_list):
    """Exécute une commande shell avec une valeur en entrée (stdin) et stocke la sortie dans output_list."""
    try:
        result = subprocess.run(cmd, shell=True, input=input_value, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)

def hakrawler(domain, custom_header=None):
    """
    Enumère les endpoints d'un domaine à l'aide de hakrawler.
    Note: hakrawler supporte l'ajout de headers via l'option -h.
    """
    output_dir = os.path.expanduser(f"output/{domain}")
    input_file = os.path.join(output_dir, f"{domain}_alive_urls.txt")

    if not os.path.exists(input_file):
        print(f"[!] Input file not found: {input_file}")
        return []

    endpoints = []

    with open(input_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        header_part = f'-h "{custom_header}" ' if custom_header else ""
        cmd = f"hakrawler {header_part} -subs -d 7 -timeout 5 -t 20"
        run_command_input(cmd, url, endpoints)

    unique_sorted = sorted(set(endpoints))
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Hakrawler -> {len(unique_sorted)} unique endpoints found")
    return unique_sorted

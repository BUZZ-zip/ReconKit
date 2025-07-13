import subprocess
import os
import re
from colorama import init, Fore, Style

def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)

def strip_ansi(text):
    """Supprime les codes de couleur ANSI."""
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def is_valid_subdomain(line, domain):
    """Vérifie si la ligne ressemble à un sous-domaine valide du domaine donné."""
    line = line.strip()
    return re.match(rf'^([a-zA-Z0-9_-]+\.)+{re.escape(domain)}$', line)

def sublist3r(domain):
    """Enumère les sous-domaines à l'aide de Sublist3r et filtre la sortie."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    sublist3r_cmd = f'sublist3r -d {domain}'

    raw_output = []
    
    run_command(sublist3r_cmd, raw_output)

    cleaned = [strip_ansi(line) for line in raw_output]
    subdomains = sorted(set(line for line in cleaned if is_valid_subdomain(line, domain)))
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Sublis3r -> {len(subdomains)} unique subdomains found")

    return subdomains

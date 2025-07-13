import subprocess
import os
from colorama import init, Fore, Style


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def httpx(domain, custom_header=None):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    # Ajout du header personnalisé si fourni
    header_part = f'-H "{custom_header}" ' if custom_header else ""
    httpx_cmd = (
        f'httpx -l "{output_dir}/{domain}_urls.txt" {header_part} -threads 100 -silent '
    )

    httpx_res = []
    run_command(httpx_cmd, httpx_res)

    all_subs = set(httpx_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running HTTPX -> {len(all_subs)} unique subdomains found")
    return all_subs

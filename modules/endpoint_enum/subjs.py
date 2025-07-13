import subprocess
import os
from colorama import Fore,Style


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def subjs(domain, custom_header=None):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils.
    Note: subjs supporte l'ajout de headers via l'option -H."""


    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_endpoints.txt"
    header_part = f'-ua "{custom_header}" ' if custom_header else ""
    subjs_cmd = f"subjs -i {input_file} {header_part} -c 100"

    subjs_res = []
    run_command(subjs_cmd, subjs_res)



    filtered = {url for url in subjs_res if domain in url}
    all_subs = set(filtered)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running SubJS -> {len(all_subs)} unique Js files found")
    return all_subs
    return all_subs

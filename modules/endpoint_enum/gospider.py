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



def gospider(domain, custom_header=None):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils.
    Note: gospider supporte l'ajout de headers via l'option -H."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_alive_urls.txt"

    header_part = f'-H "{custom_header}" ' if custom_header else ""
    gospider_cmd = f"gospider -S {input_file} {header_part}-d 4 -c 20 -t 10 -q "

    gospider_res = []
    run_command(gospider_cmd, gospider_res)


    all_subs = set(gospider_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Gospider -> {len(all_subs)} unique endpoints found")
    return all_subs

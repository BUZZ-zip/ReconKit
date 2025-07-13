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



def assetfinder(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    assetfinder_cmd = f"assetfinder --subs-only {domain}"

    assetfinder_res=[]

   

    run_command(assetfinder_cmd,assetfinder_res)



  
    all_subs = set(assetfinder_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Assetfinder -> {len(all_subs)} unique subdomains found")
    return all_subs

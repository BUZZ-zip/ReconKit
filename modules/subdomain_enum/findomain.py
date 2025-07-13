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



def findomain(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    

    findomain_cmd = f"findomain -t {domain} -q"

    findomain_res=[]

   

    run_command(findomain_cmd,findomain_res)

  
    all_subs = set(findomain_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Chaos -> {len(all_subs)} unique subdomains found")
    return all_subs

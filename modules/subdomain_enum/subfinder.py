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



def subfinder(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    subfinder_cmd = f"subfinder -d {domain} -t 50 -silent"

    subfinder_res=[]
   

    run_command(subfinder_cmd,subfinder_res)



  
    all_subs = set(subfinder_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Subfinder -> {len(all_subs)} unique subdomains found")
    return all_subs

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



def gowitness(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    gowitness_cmd = f"gowitness scan file -f output/{domain}/{domain}_alive_urls.txt --screenshot-path output/{domain}/screen_{domain}/"

    gowitness_res=[]

   

    run_command(gowitness_cmd,gowitness_res)



  
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Gowitness -> Sreenshot saved output/{domain}/screen_{domain}/")

    return []
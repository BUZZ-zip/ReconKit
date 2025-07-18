import subprocess
import os
import json
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



def chaos(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    config_path = "page/static/config.json"

    with open(config_path, "r") as f:
        old_config = json.load(f)
   
    chaos_key = (
        old_config.get("subdomain", {})
        .get("chaos", {})
        .get("apiKeys", {})
        .get("chaos", None)
    )
    if chaos_key is None:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Clé API Chaos non trouvée dans config.json.")
        return []
    os.environ["PDCP_API_KEY"] = chaos_key
        

    chaos_cmd = f"chaos -d {domain} -silent"

    chaos_res=[]
   

    run_command(chaos_cmd,chaos_res)

    

  
    all_subs = set(chaos_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Chaos -> {len(all_subs)} unique subdomains found")
    return all_subs

import subprocess
import os

from colorama import Style,Fore


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def getjs(domain, custom_header=None):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils.
    Note: getJS supporte l'ajout de headers via l'option -h."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_endpoints.txt"
    
    header_part = f'-header "{custom_header}" ' if custom_header else ""
    getjs_cmd = f"getJS -input {input_file} {header_part} -complete -resolve -threads 100"

    getjs_res = []
    run_command(getjs_cmd, getjs_res)


    filtered = {url for url in getjs_res if domain in url}
    all_subs = set(filtered)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running getJS -> {len(all_subs)} unique Js files found")
    return all_subs
   

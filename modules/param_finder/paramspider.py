import subprocess
import os
import re


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def paramspider(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_urls.txt"
    paramspider_cmd = f"paramspider -l {input_file}  -s"

    paramspider_res=[]

   

    run_command(paramspider_cmd,paramspider_res)

    print("[+] Running Paramspider")

    urls = re.findall(r'https?://[^\s\'"]+', '\n'.join(paramspider_res))

    all_subs = set(urls)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

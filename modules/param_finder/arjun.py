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



def arjun(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_alive_endpoints.txt"
    arjun_cmd = f"arjun -i {input_file}"

    arjun_res=[]

   

    run_command(arjun_cmd,arjun_res)

    print("[+] Running Arjun")


    all_subs = set(arjun_res)
    all_subs = sorted(all_subs)
    print(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

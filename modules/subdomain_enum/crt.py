import subprocess
import os


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def crtsh(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"~/output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    crtsh_cmd = f'curl -s "https://crt.sh/?q=%.{domain}&output=json" | jq -r ".[].name_value" | sed "s/\\*\\.//g"'


    crtsh_res=[]

   

    run_command(crtsh_cmd,crtsh_res)

    print("[+] Running crt.sh")

  
    all_subs = set(crtsh_res)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs
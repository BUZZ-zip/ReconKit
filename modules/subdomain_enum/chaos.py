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



def chaos(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"~/output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    chaos_cmd = f"chaos -d {domain} -silent"

    chaos_res=[]
   

    run_command(chaos_cmd,chaos_res)

    print("[+] Running Chaos")

  
    all_subs = set(chaos_res)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

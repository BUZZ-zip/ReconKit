import subprocess
import os


def run_command_input(cmd, input_path, output_list):
    """Exécute une commande shell avec un fichier en entrée, envoie le contenu sur stdin."""
    try:
        with open(input_path, "r") as f:
            result = subprocess.run(cmd, shell=True, stdin=f, capture_output=True, text=True)
        if result.stderr:
            print(f"[stderr] {cmd}:\n{result.stderr.strip()}")
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def gau(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_alive_urls.txt"

    gau_cmd = f"gau --threads 100"

    gau_res=[]

   

    run_command_input(gau_cmd,input_file,gau_res)

    print("[+] Running Gau")

  
    all_subs = set(gau_res)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

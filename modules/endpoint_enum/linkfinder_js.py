import subprocess
import os
import jsbeautifier


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def katana(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_alive_urls.txt"
    linkfinder_path = os.path.abspath(os.path.expanduser("~/LinkFinder/linkfinder.py"))
    katana_cmd = f"python3 {linkfinder_path} -i http://tictac.com/fr/31d4e3d1-a05373943e1628fc85ba.js -o cli"

    katana_res=[]

   

    run_command(katana_cmd,katana_res)

    print("[+] Running Katana")

  
    all_subs = set(katana_res)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

katana("tictac.com")

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



def subjs(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_endpoints.txt"
    subjs_cmd = f"subjs -i {input_file} -c 100"

    subjs_res=[]

   

    run_command(subjs_cmd,subjs_res)

    print("[+] Running subJS")

    filtered = {url for url in subjs_res if domain in url}
    all_subs = set(filtered)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

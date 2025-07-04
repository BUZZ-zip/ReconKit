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



def getjs(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_endpoints.txt"
    getjs_cmd = f"getJS -input {input_file} -complete -resolve -threads 100"

    getjs_res=[]

   

    run_command(getjs_cmd,getjs_res)

    print("[+] Running getJS")

    filtered = {url for url in getjs_res if domain in url}
    all_subs = set(filtered)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

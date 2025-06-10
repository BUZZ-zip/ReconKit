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



def httpx(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    output_dir = os.path.expanduser(f"~/output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    httpx_cmd = f'httpx -l "{output_dir}/{domain}_urls.txt" -threads 100 -silent -mc 200,204,206,301,302,307,308,401,403,407,500,502,503,504'

    httpx_res=[]
   

    run_command(httpx_cmd,httpx_res)

    print("[+] Running HTTPX")

  
    all_subs = set(httpx_res)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")
    return all_subs

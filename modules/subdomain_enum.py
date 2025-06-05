import subprocess
import tempfile
import os
import threading

def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)

def get_subdomains(domain):
    """Enumère les sous-domaines d'un domaine à l'aide de plusieurs outils."""
    print(f"[*] Enumerating subdomains for {domain}")

    subfinder_cmd = f"subfinder -d {domain} -t 50 -silent"
    assetfinder_cmd = f"assetfinder --subs-only {domain}"
    findomain_cmd = f"findomain -t {domain} -q"
    crtsh_cmd = f'curl -s "https://crt.sh/?q=%.{domain}&output=json" | jq -r ".[].name_value" | sed "s/\\*\\.//g"'
    httpx_cmd = f'httpx -l "../output/{domain}_urls.txt" -threads 100 -silent -mc 200,302,403,401'

    subfinder_res=[]
    assetfinder_res=[]
    findomain_res=[]
    crtsh_res=[]



    threads = [
        threading.Thread(target=run_command, args=(subfinder_cmd, subfinder_res)),
        threading.Thread(target=run_command, args=(assetfinder_cmd, assetfinder_res)),
        threading.Thread(target=run_command, args=(findomain_cmd, findomain_res)),
        threading.Thread(target=run_command, args=(crtsh_cmd, crtsh_res)),
    ]


    print("[+] Running Subfinder / Assetfinder / Findomain / crt.sh")
    for t in threads:
        t.start()
    for t in threads:
        t.join()

  
    all_subs = set(subfinder_res + assetfinder_res + findomain_res + crtsh_res)
    all_subs = sorted(all_subs)
    print(f"  -> {len(all_subs)} unique subdomains found.")



    
    with open(f'../output/{domain}_urls.txt', "w") as f:
        for sub in all_subs:
            f.write(sub + "\n")

    print("[+] Running HTTPX...")
    httpx_res = []
    run_command(httpx_cmd,httpx_res)
    print(f"  -> {len(httpx_res)} alive subdomains found.")
    with open(f'../output/{domain}_alive_urls.txt', "w") as f:
        for sub in httpx_res:
            f.write(sub + "\n")
    


    print(f"[✓] Subdomains written to ../output/{domain}_alive_urls.txt")
    return httpx_res

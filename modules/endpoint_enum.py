import subprocess
import tempfile
import os
import threading

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


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
       
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)

    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)




def get_endpoints(domain):
    print(f"[*] Gathering endpoints for {domain}")

    input_file = f"../output/{domain}_alive_urls.txt"
    katana_cmd = f"katana -list {input_file} -d 2 -c 100"
    gau_cmd = f"gau --threads 200"
    waybackurl_cmd = f"waybackurls"
    httpx_cmd = f'httpx -l "../output/{domain}_endpoints.txt" -threads 100 -silent -mc 200,302,403,401 -title -fr'

    katana_res = []
    gau_res = []
    wayback_res = []



    threads = [
        threading.Thread(target=run_command, args=(katana_cmd, katana_res)),
        threading.Thread(target=run_command_input, args=(gau_cmd, input_file, gau_res)),
        threading.Thread(target=run_command_input, args=(waybackurl_cmd, input_file, wayback_res)),
    ]

    


    print("[+] Running Katana / GAU / WaybackURLs")
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    all_endpoints = sorted(set(katana_res + gau_res + wayback_res))
    print(f"  -> {len(all_endpoints)} unique endpoints found.")

    output_path = f'../output/{domain}_endpoints.txt'
    with open(output_path, "w") as f:
        for sub in all_endpoints:
            f.write(sub + "\n")

    print("[+] Running HTTPX...")
    httpx_res = []
    run_command(httpx_cmd, httpx_res)
    print(f"  -> {len(httpx_res)} alive subdomains found.")
    with open(f'../output/{domain}_alive_endpoints.txt', "w") as f:
        for sub in httpx_res:
            f.write(sub + "\n")

    print(f"[✓] Subdomains written to ../output/{domain}_alive_endpoints.txt")
    return httpx_res

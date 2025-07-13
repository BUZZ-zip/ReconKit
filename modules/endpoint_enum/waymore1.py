import subprocess
import os
from colorama import Fore,Style


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def waymore(domain, custom_header=None):
    
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_alive_urls.txt"

    waymore_cmd = f"waymore -i {input_file} -oU {output_dir}/{domain}_waymore.txt -mode U -p 5"

    waymore_res = []
    run_command(waymore_cmd, waymore_res)


    waymore_cmd = f"cat {output_dir}/{domain}_waymore.txt"

    waymore_res = []
    run_command(waymore_cmd, waymore_res)

    all_subs = set(waymore_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Waymore -> {len(all_subs)} unique endpoints found")
    return all_subs

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



def katana(domain, custom_header=None):
    
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    input_file = f"{output_dir}/{domain}_alive_urls.txt"

    header_part = f'-H "{custom_header}" ' if custom_header else ""

    katana_cmd = f"katana -list {input_file} {header_part}-d 4 -c 100"

    katana_res = []
    run_command(katana_cmd, katana_res)

  
    all_subs = set(katana_res)
    all_subs = sorted(all_subs)
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running Katana -> {len(all_subs)} unique endpoints found")
    return all_subs

import subprocess
import os
import json
from colorama import Fore, Style

def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)


def virustotal(domain):
    """Enumère les sous-domaines via l'API VirusTotal en curl avec header."""

    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    config_path = "page/static/config.json"
    with open(config_path, "r") as f:
        old_config = json.load(f)

        virustotal_key = (
        old_config.get("subdomain", {})
        .get("virustotal", {})
        .get("apiKeys", {})
        .get("virustotal", None)
    )

    if not virustotal_key:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Clé API VirusTotal non trouvée dans config.json.")
        return []

    # Exemple d'endpoint VirusTotal pour récupérer les sous-domaines (attention limite rate, vérifie l'API)
    virustotal_cmd = (
        f'curl -s -H "x-apikey: {virustotal_key}" '
        f'"https://www.virustotal.com/api/v3/domains/{domain}/subdomains" | '
        'jq -r \'.data[].id\''
    )

    virustotal_res = []
    run_command(virustotal_cmd, virustotal_res)

    all_subs = sorted(set(virustotal_res))
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running VirusTotal -> {len(all_subs)} unique subdomains found")
    return all_subs

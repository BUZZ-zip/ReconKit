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

def alienvault(domain):
    """Enumère les sous-domaines via l'API AlienVault OTX en curl avec header."""

    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    config_path = "page/static/config.json"
    with open(config_path, "r") as f:
        old_config = json.load(f)

        alienvault_key = (
        old_config.get("subdomain", {})
        .get("alienvault", {})
        .get("apiKeys", {})
        .get("alienvault", None)
    )

    if not alienvault_key:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Clé API AlienVault non trouvée dans config.json.")
        return []

    alienvault_cmd = (
        f'curl -s -H "X-OTX-API-KEY: {alienvault_key}" '
        f'"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns" | '
        'jq -r \'.passive_dns[]?.hostname\''
    )

    alienvault_res = []
    run_command(alienvault_cmd, alienvault_res)

    all_subs = sorted(set(alienvault_res))
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running AlienVault -> {len(all_subs)} unique subdomains found")
    return all_subs

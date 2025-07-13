import subprocess
import os
from colorama import init, Fore, Style
import json


def run_command(cmd, output_list):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        output_list.extend(lines)
    except Exception as e:
        print(f"[!] Error running command: {cmd}")
        print(e)



def dnsdumpster(domain):
    """Enumère les sous-domaines via l'API dnsdumpster en curl avec header."""

    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    config_path = "page/static/config.json"
    with open(config_path, "r") as f:
        old_config = json.load(f)
        dnsdumpster_key = (
        old_config.get("subdomain", {})
        .get("dnsdumpster", {})
        .get("apiKeys", {})
        .get("dnsdumpster", None)
    )

    dnsdumpster_cmd = (
        f'curl -H "X-API-Key: {dnsdumpster_key}" https://api.dnsdumpster.com/domain/{domain} | jq -r "[.a[].host, .cname[].host, .mx[].host, .ns[].host] | unique | .[]"'
    )

    
    dnsdumpster_res = []
    run_command(dnsdumpster_cmd, dnsdumpster_res)
    
    all_subs = sorted(set(dnsdumpster_res))
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running DNSdumpster -> {len(all_subs)} unique subdomains found")
    return all_subs
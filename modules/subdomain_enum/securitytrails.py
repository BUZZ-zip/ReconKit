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



def securitytrails(domain):
    """Enumère les sous-domaines via l'API SecurityTrails en curl avec header."""

    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    config_path = "page/static/config.json"
    with open(config_path, "r") as f:
        old_config = json.load(f)
        securitytrails_key = (
        old_config.get("subdomain", {})
        .get("securitytrails", {})
        .get("apiKeys", {})
        .get("securitytrails", None)
    )

    securitytrails_cmd = (
        f'curl -s -H "APIKEY: {securitytrails_key}" '
        f'"https://api.securitytrails.com/v1/domain/{domain}/subdomains" | '
        'jq -r \'.subdomains[] | "\(.)' + '.' + f'{domain}"\''
    )

    securitytrails_res = []
    run_command(securitytrails_cmd, securitytrails_res)

    all_subs = sorted(set(securitytrails_res))
    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running SecurityTrails -> {len(all_subs)} unique subdomains found")
    return all_subs
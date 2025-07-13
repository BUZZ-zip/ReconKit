import subprocess
import os
from colorama import init, Fore, Style
import json

def run_whatweb(url):
    try:
        result = subprocess.run(
            ["whatweb", "--log-json=-", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            text=True
        )
        parsed = []
        for line in result.stdout.strip().splitlines():
            try:
                parsed.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return parsed
    except Exception as e:
        print(f"[!] Erreur avec {url} : {e}")
        return []

def whatweb(domain):
    input_file = f"output/{domain}/{domain}_alive_urls.txt"
    output_file = f"output/{domain}/{domain}_tech_all.json"

    if not os.path.exists(input_file):
        print(f"[!] Fichier introuvable : {input_file}")
        return

    all_results = []

    with open(input_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Running WhatWeb -> {len(urls)} URLs to scan")

    for url in urls:
        res = run_whatweb(url)
        all_results.extend(res)

    with open(output_file, "w") as out:
        json.dump(all_results, out, indent=2)

    print(f"{Fore.BLUE}[i]{Fore.RESET} Saved results to : {output_file}")
    return []

from modules.param_finder.paramspider import paramspider
from modules.param_finder.arjun import arjun
import os
import json
import threading

def save_results(domain,results,method):
    output_dir = os.path.expanduser(f"output/{domain}")
    os.makedirs(output_dir, exist_ok=True)
    if method =='urls':
        filename = os.path.join(output_dir, f"{domain}_param_urls.txt")
        unique_sorted = sorted(set(results))
        with open(filename, "w") as f:
            for sub in unique_sorted:
                f.write(sub + "\n")
    elif method == 'alive':
        filename = os.path.join(output_dir, f"{domain}_alive_urls.txt")
        unique_sorted = sorted(set(results))
        with open(filename, "w") as f:
            for sub in unique_sorted:
                f.write(sub + "\n")
    elif method == 'ip':
        filename = os.path.join(output_dir, f"{domain}_ip.txt")
        unique_sorted = sorted(set(results))
        with open(filename, "w") as f:
            for sub in unique_sorted:
                f.write(sub + "\n")
    else : 
        print("[!] ERROR during save")
        return

    print(f"[i] Saved {len(unique_sorted)} unique subdomains to {filename}")

def run_tools_paramfinder(domain, config_path="config.json"):
    with open(config_path) as f:
        config = json.load(f)

    selected_tools = config.get("param_tools", [])

    results = []
    results_lock = threading.Lock()

    def run_and_collect(tool_func):
        res = tool_func(domain)
        with results_lock:
            results.extend(res)

    threads = []

    if "paramspider" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(paramspider,))
        threads.append(t)
    if "arjun" in selected_tools:
        t = threading.Thread(target=run_and_collect, args=(arjun,))
        threads.append(t)


    for t in threads:
        t.start()
    for t in threads:
        t.join()

    unique_sorted = sorted(set(results))

    print(f"[i] Total unique subdomains found: {len(unique_sorted)}")
    save_results(domain,unique_sorted,'urls')



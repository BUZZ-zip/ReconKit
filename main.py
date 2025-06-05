import argparse
from modules.subdomain_enum import *
from modules.endpoint_enum import * 
import time

def main():
    parser = argparse.ArgumentParser(description="Recon Tool - Pipeline de reconnaissance")
    parser.add_argument("-d", "--domain", required=True, help="Domaine cible (ex: example.com)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Nombre de threads (défaut: 10)")
    
    args = parser.parse_args()

    domain = args.domain
    threads = args.threads

    print(f"[i] Domaine : {domain}")
    print(f"[i] Threads : {threads}")

    subdomains = get_subdomains(domain)
    endpoints = get_endpoints(domain)


if __name__ == "__main__":
    start_time = time.time()

    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n[i] Total execution time: {elapsed_time:.2f} seconds")
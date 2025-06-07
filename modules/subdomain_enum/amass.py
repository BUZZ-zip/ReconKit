import subprocess
import os


def run_amass(domain):
    """Lance Amass en mode passive et récupère les sous-domaines en temps réel."""
    print("[+] Running Amass")
    subdomains = []
    try:
        cmd = ["amass", "enum", "-passive", "-d", domain]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

        for line in process.stdout:
            line = line.strip()

            # Ignore les relations du graphe (liens -->)
            if '-->' in line or line == "":
                continue

            print(line)  # Affiche en temps réel
            subdomains.append(line)

        process.wait()

    except KeyboardInterrupt:
        print("\n[!] Interrompu par l'utilisateur.")
    except Exception as e:
        print(f"[!] Erreur lors de l'exécution d'Amass: {e}")

    return subdomains


def amass(domain):
    """Exécute Amass et stocke les sous-domaines trouvés."""
    output_dir = os.path.expanduser(f"~/output/{domain}")
    os.makedirs(output_dir, exist_ok=True)

    results = run_amass(domain)

    # Supprimer les doublons, trier et afficher
    unique_subs = sorted(set(results))
    print("\n[+] Résultats uniques :")
    for sub in unique_subs:
        print(sub)

    print(f"\n  -> {len(unique_subs)} unique subdomains found by Amass.")

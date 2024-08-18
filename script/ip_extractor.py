import requests
import pandas as pd
import time
import os
import shutil

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'success':
            return data['country']
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return None

def display_progress_bar(current, total, bar_length=30):
    progress = current / total
    block = int(round(bar_length * progress))
    bar = "█" * block + "*" * (bar_length - block)  # Utilisation des étoiles pour la partie non remplie
    percentage = f"{progress * 100:.2f}%"
    bar_display = f"{percentage} [{bar}]"
    
    # Calculer l'espacement pour centrer la barre de progression
    term_width = shutil.get_terminal_size().columns
    padding = (term_width - len(bar_display)) // 2
    
    # Déplacer le curseur sur la dernière ligne et afficher la barre de progression centrée
    print(f"\033[{shutil.get_terminal_size().lines};1H", end="")
    print(" " * padding + bar_display, end="")

def process_ip_file(input_file):
    # Retirer les apostrophes autour du chemin du fichier, si elles existent
    if input_file.startswith("'") and input_file.endswith("'"):
        input_file = input_file[1:-1]
    
    # Génération des noms de fichiers de sortie basés sur le nom du fichier d'entrée
    base_name = os.path.splitext(input_file)[0]
    output_file_ips = f"{base_name}_with_countries.txt"
    output_file_summary = f"{base_name}_country_summary.csv"

    country_count = {}
    
    # Lire toutes les lignes pour compter le nombre total d'IP
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    total_ips = len(lines)
    
    print(f"Nombre total d'IP à traiter : {total_ips}\n")
    
    with open(input_file, 'r') as file, open(output_file_ips, 'w') as output_file:
        for index, line in enumerate(lines):
            ip = line.strip()
            country = get_ip_info(ip)
            if country:
                output_line = f"{ip} : {country}\n"
                output_file.write(output_line)
                if country in country_count:
                    country_count[country] += 1
                else:
                    country_count[country] = 1
            else:
                output_line = f"{ip} : UNKNOWN\n"
                output_file.write(output_line)
            
            # Afficher la ligne en temps réel dans le terminal
            print(output_line.strip())
            
            # Afficher la barre de progression
            display_progress_bar(index + 1, total_ips)
            
            time.sleep(1)  # Pour respecter les limites de taux de l'API

    # Création d'un DataFrame pour le résumé, tri par nombre d'IP, et sauvegarde dans un fichier CSV
    df = pd.DataFrame(list(country_count.items()), columns=['Country', 'IP Count'])
    df = df.sort_values(by='IP Count', ascending=False)  # Trier par nombre d'IP de manière décroissante
    df.to_csv(output_file_summary, index=False)

    # Fin de la barre de progression
    display_progress_bar(total_ips, total_ips)
    print(f"\nRésultats enregistrés dans :\n- {output_file_ips}\n- {output_file_summary}")

# Demander le nom du fichier d'entrée à l'utilisateur
input_file = input("Veuillez entrer le nom du fichier contenant les adresses IP : ")

# Appeler la fonction pour traiter le fichier
process_ip_file(input_file)

import requests
import pandas as pd
import time
import os
import matplotlib.pyplot as plt

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

def process_ip_file(input_file):
    # Retirer les apostrophes autour du chemin du fichier, si elles existent
    if input_file.startswith("'") and input_file.endswith("'"):
        input_file = input_file[1:-1]
    
    # Génération des noms de fichiers de sortie basés sur le nom du fichier d'entrée
    base_name = os.path.splitext(input_file)[0]
    output_file_ips = f"{base_name}_with_countries.txt"
    output_file_summary = f"{base_name}_country_summary.csv"
    output_file_pie_chart = f"{base_name}_country_pie_chart.png"

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
            
            # Afficher l'avancement
            print(f"Avancement : {index + 1}/{total_ips} IPs traitées ({((index + 1) / total_ips) * 100:.2f}%)\n")
            
            time.sleep(1)  # Pour respecter les limites de taux de l'API

    # Création d'un DataFrame pour le résumé, tri par nombre d'IP, et sauvegarde dans un fichier CSV
    df = pd.DataFrame(list(country_count.items()), columns=['Country', 'IP Count'])
    df = df.sort_values(by='IP Count', ascending=False)  # Trier par nombre d'IP de manière décroissante
    df.to_csv(output_file_summary, index=False)

    # Filtrer les pays avec moins de 2.5% des IPs
    threshold = 0.025 * total_ips
    df_filtered = df[df['IP Count'] >= threshold]
    other_count = df['IP Count'][df['IP Count'] < threshold].sum()

    if other_count > 0:
        # Création d'un DataFrame pour les "Others"
        others_df = pd.DataFrame({'Country': ['Others'], 'IP Count': [other_count]})
        # Concaténation des DataFrames
        df_filtered = pd.concat([df_filtered, others_df], ignore_index=True)

    # Création du graphique en camembert
    plt.figure(figsize=(12, 8))
    plt.pie(df_filtered['IP Count'], labels=df_filtered['Country'], autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10}, pctdistance=0.85, labeldistance=1.2)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis('equal')  # Assure que le graphique est un cercle parfait
    plt.savefig(output_file_pie_chart)
    plt.close()

    print(f"Résultats enregistrés dans :\n- {output_file_ips}\n- {output_file_summary}\n- {output_file_pie_chart}")

# Demander le nom du fichier d'entrée à l'utilisateur
input_file = input("Veuillez entrer le nom du fichier contenant les adresses IP : ")

# Appeler la fonction pour traiter le fichier
process_ip_file(input_file)

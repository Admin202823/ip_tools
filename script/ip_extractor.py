import re

# Fonction pour extraire les adresses IP du fichier de log
def extract_ips(log_file, output_file):
    # Expression régulière pour capturer une adresse IP (IPv4)
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    try:
        with open(log_file, 'r') as f:
            log_content = f.read()
        
        # Recherche des adresses IP dans le contenu du fichier de log
        ips = re.findall(ip_pattern, log_content)
        
        # Écriture des IP extraites dans le fichier de sortie
        with open(output_file, 'w') as output:
            for ip in set(ips):  # Utilisation de set pour éviter les doublons
                output.write(ip + '\n')
        
        print(f"Les adresses IP ont été extraites et enregistrées dans {output_file}")
    
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{log_file}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Demande du nom du fichier de log
log_file = input("Entrez le nom du fichier de log à partir duquel extraire les IPs : ")

# Nom du fichier de sortie pour les adresses IP extraites
output_file = 'ip_extracted'

# Appel de la fonction pour extraire les IP
extract_ips(log_file, output_file)

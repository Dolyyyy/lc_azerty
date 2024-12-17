# Générer le fichier .exe : pyinstaller --onefile --icon=lastcountry.ico lastcountry_azerty.py

import os
import requests
import json
from pathlib import Path

CONFIG_FILE = "redm_config.json"
DEFAULT_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "RedM", "RedM.app", "citizen", "platform", "data", "control")
FILE_URL = "https://lastcountryrp.fr/default.meta"
FILE_NAME = "default.meta"

def save_config(path):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"path": path}, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get("path")
    return None

def download_file(url, destination):
    try:
        print(f"✅ Téléchargement du fichier depuis {url}...")
        response = requests.get(url)
        response.raise_for_status()
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"✅ Fichier téléchargé avec succès : {destination}")
    except requests.RequestException as e:
        print(f"❌ Erreur lors du téléchargement : {e}")

def get_valid_redm_path():
    saved_path = load_config()
    if saved_path and os.path.exists(saved_path):
        print("🔄 Utilisation du chemin sauvegardé :", saved_path)
        return saved_path

    if os.path.exists(DEFAULT_PATH):
        print("✅ Chemin RedM par défaut trouvé :", DEFAULT_PATH)
        return DEFAULT_PATH

    while True:
        print("❓ Impossible de trouver RedM. Merci de préciser le chemin d'installation.")
        custom_path = input("Entrez le chemin complet jusqu'à 'control' : ").strip()
        if os.path.exists(custom_path):
            save_config(custom_path)
            print("✅ Chemin sauvegardé !")
            return custom_path
        else:
            print("❌ Chemin invalide. Veuillez réessayer.")

def main():
    print("=== Script pour passer RedM en AZERTY par Doly pour https://lastcountryrp.fr ===")
    redm_path = get_valid_redm_path()
    file_destination = os.path.join(redm_path, FILE_NAME)

    confirm = input("Voulez-vous télécharger et installer le fichier ? (oui/non) : ").strip().lower()
    if confirm in ["oui", "o", "yes", "y"]:
        download_file(FILE_URL, file_destination)
        print("🚀 Fichier copié dans le dossier RedM. Redémarrez RedM pour appliquer les changements.")
    else:
        print("❌ Installation annulée.")
    input("\nAppuie sur Entrée pour fermer l'application...")

if __name__ == "__main__":
    main()
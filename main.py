import sys
import os
import tkinter as tk
import msvcrt


def get_clipboard_content():
    """Recupere le contenu du presse-papiers"""
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale
    clipboard_content = root.clipboard_get()  # Récupère le contenu du presse-papiers
    root.destroy()  # Ferme la fenêtre Tkinter
    return clipboard_content

# Récupère et affiche le contenu du presse-papiers
clipboard_content = get_clipboard_content()

if len(clipboard_content) <= 12:
    print("Contenu du presse-papiers:", clipboard_content)
    # Stocker le contenu dans un fichier texte
    with open("pp.txt", "w") as file:
        file.write(clipboard_content)
        print("Le contenu du presse-papiers a été sauvegardé dans 'presse_papiers.txt'")
else:
    print("Presse-papiers trop long")



def enregistrer_touches_windows(nom_fichier="clavier_log.txt"):
    """
    Enregistre les touches du clavier dans un fichier texte sous Windows.

    Args:
        nom_fichier (str): Chemin du fichier où les touches sont enregistrées.
    """
    
    print(f"Enregistrement des touches dans {nom_fichier} (appuyez sur 'Esc' pour arrêter).")

    with open(nom_fichier, "a") as fichier:
        while True:
            # Récupère la touche pressée
            touche = msvcrt.getch()

            # Arrête si 'Esc' est pressé
            if touche == b'\x1b':  # Code pour la touche 'Esc'
                print("Arrêt de l'enregistrement.")
                break

            # Convertit en format lisible et écrit dans le fichier
            try:
                fichier.write(touche.decode("utf-8"))
            except UnicodeDecodeError:
                fichier.write(f"[{touche}]")

            # Vide la sortie standard pour éviter d'afficher les touches dans le terminal
            fichier.flush()

# Utilisation de la fonction sous Windows
enregistrer_touches_windows()


import sys
import os
import tkinter as tk

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

import main


start_time = main.time.time()

def mise_en_veille_toutes_les_1_minutes():
    while True:
        # Mettre le PC en veille
        main.os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        
        # Attendre 2 minutes avant la prochaine mise en veille
        main.time.sleep(60)

def Main():
    while main.time.time() - start_time < 120:
        mise_en_veille_toutes_les_1_minutes()


if __name__ == "__main__":
    Main()
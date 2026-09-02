import os
import pomozne_funkcije

ZACETNO_LETO = 1956
KONCNO_LETO = 2026
OSNOVNI_URL = "https://eurovisionworld.com/eurovision/"
MAPA_PODATKOV = "zajeti_podatki"
CSV_IZHOD = "podatki/evrovizija.csv"

def shrani_html ():
    """Funkcija prenese in shrani HTML za vsa definirana leta."""
    print ("--- 1. prenos spletnih strani ---")
    for leto in range (ZACETNO_LETO, KONCNO_LETO + 1):
        pot_datoteke = os.path.join (MAPA_PODATKOV, f"evrovizija_{leto}.html")

        if not os.path.exists (pot_datoteke):
            url = f"{OSNOVNI_URL}{leto}"
            vsebina = pomozne_funkcije.prenos_strani (url)
            if vsebina:
                pomozne_funkcije.shranjevanje_niza (vsebina, pot_datoteke)
                print (f"Shranil sem leto {leto}.")
        else:
            print (f"Leto {leto} že obstaja lokalno.")

def obdelaj_podatke ():
    """Funkcija obdela podatke: jih prebere, izlušči potrebno in podatke shrani v CSV."""
    print ("\n--- 2. obdelava HTML datotek ---")
    vsi_rezultati = []

    for leto in range (ZACETNO_LETO, KONCNO_LETO + 1):
        pot_datoteke = os.path.join (MAPA_PODATKOV, f"evrovizija_{leto}.html")

        if os.path.exists (pot_datoteke):
            vsebina = pomozne_funkcije.branje_datoteke (pot_datoteke)
            podatki_leta = pomozne_funkcije.izluscevanje_podatkov (vsebina, leto)
            vsi_rezultati.extend (podatki_leta)
    print (f"Skupno število izluščenih vrstic je {len (vsi_rezultati)}.")


# Definiramo seznam polj, ki ustreza ključem v slovarju.

    polja = [
        'leto',
        'mesto',
        'drzava',
        'pesem',
        'izvajalec',
        'tocke',
        'tocke_publike',
        'tocke_zirije',
        'startna_stevilka',
    ]

    pomozne_funkcije.zapisovanje_v_csv (vsi_rezultati, polja, CSV_IZHOD)
    print (f"Podatki so uspešno shranjeni v datoteko: {CSV_IZHOD}!")

def glavna ():
    shrani_html ()
    obdelaj_podatke ()

if __name__ == "__main__":
    glavna ()
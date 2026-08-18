import os
import csv
from selenium import webdriver
import time
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def ustvari (pot):
    """Funkcija ustvari mapo, če ta še ne obstaja."""
    os.makedirs (pot, exist_ok = True)

def prenos_strani (url):
    """Funkcija prenese HTML z uporabo brskalnika Safari, da se izvede JavaScript."""
    try:
        driver = webdriver.Safari ()
        driver.get (url)
    
        time.sleep (1)
        
        html_vsebina = driver.page_source
        driver.quit ()
        return html_vsebina
    except Exception as e:
        print (f"Zgodila se je napaka pri prenosu preko Safarija: {e}")
        return None

def shranjevanje_niza (text, pot_datoteke):
    """Funkcija shrani tekstovni niz v datoteko."""
    ustvari (os.path.dirname (pot_datoteke))
    with open (pot_datoteke, 'w', encoding = 'utf-8') as dat:
        dat.write (text)

def branje_datoteke (pot_datoteke):
    """Funkcija prebere dano datoteko in vrne njeno vsebino."""
    with open (pot_datoteke, 'r', encoding = 'utf-8') as dat:
        return dat.read ()

def zapisovanje_v_csv (podatki, polja, pot_datoteke):
    """Funkcija zapiše seznam slovarjev v CSV datoteko."""
    ustvari (os.path.dirname (pot_datoteke))
    with open (pot_datoteke, 'w', newline = '', encoding = 'utf-8') as dat:
        zapisovanje = csv.DictWriter (dat, fieldnames = polja)
        zapisovanje.writeheader ()
        zapisovanje.writerows (podatki)

def ciscenje_niza (niz):
    """Funkcija počisti in prečisti niz ter uredi besedilo."""
    if not niz:
        return ""
    else:
        return " ".join (niz.strip ().split ())

def izluscevanje_podatkov (html_vsebina, leto):
    """Funkcija izlušči podatke o pesmi in izvajalcih za posamezno leto."""
    soup = BeautifulSoup (html_vsebina, 'html.parser')
    podatki = []

    tabela = soup.find ('table', class_ = 'v_table')
    if not tabela:
        return podatki

    vrstice = tabela.find_all ('tr')

    for vrstica in vrstice:
        celice = vrstica.find_all (['td', 'th'])

        if len (celice) < 4:
            continue

        teksti = [ciscenje_niza (celica.get_text ()) for celica in celice]

        uvrstitev = teksti [0]

        if uvrstitev.isdigit ():
            koncna_pozicija = int (uvrstitev)                       # 1. stolpec: uvrstitev
            drzava = teksti [1] if len (teksti) > 1 else ""         # 2. stolpec: država izvajalca
            izvajalec = teksti [2] if len (teksti) > 2 else ""      # 3. stolpec: izvajalec pesmi
            pts = teksti [3] if len (teksti) > 3 else ""
            tocke = int (pts) if pts.isdigit () else None           # 4. stolpec: končno št. točk
            startna_stevilka = None
            if len (teksti) > 4 and teksti [4].isdigit ():          # 5. stolpec: running order pesmi
                startna_stevilka = int (teksti [4])             
            dvanajstke = None
            if len (teksti) > 5 and teksti [5].isdigit ():          # 6. stolpec: kolikokrat je izvajalec prejel 12 točk
                dvanajstke = int (teksti [5])

            podatki.append ({
                'leto': leto,
                'mesto': koncna_pozicija,
                'drzava': drzava,
                'izvajalec': izvajalec,
                'tocke': tocke,
                'startna_stevilka': startna_stevilka,
                'st_dvanajstk': dvanajstke
            })
    return podatki
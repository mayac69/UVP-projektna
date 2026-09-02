import os
import csv
from selenium import webdriver
import time
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

POPRAVKI__IMEN = {
    "United Kingdom UK": "United Kingdom",
    "Bosnia & Herz egovina .": "Bosnia & Herzegovina",
    "North Macedonia N.Macedonia": "North Macedonia"
}

def popravi_ime_drzave (napacno_ime):
    """Če je ime napačno prenešeno in obstaja popravek v slovarju, ga funkcija popravi."""
    return POPRAVKI__IMEN.get (napacno_ime, napacno_ime)

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

        teksti = [ciscenje_niza (celica.get_text (separator = " ")) for celica in celice]

        uvrstitev = teksti [0]

        if uvrstitev.isdigit ():
            koncna_pozicija = int (uvrstitev)                       # 1. stolpec: uvrstitev
            drzava_1 = teksti [1] if len (teksti) > 1 else ""       # 2. stolpec: država izvajalca
            drzava = popravi_ime_drzave (drzava_1)

            pesem_v_celici = celice [2]
            isci_a = pesem_v_celici.find ('a')
            if isci_a:
                # Avtor pesmi
                izvajalec_v_celici = pesem_v_celici.find ('span', class_ = 'v_artist')
                izvajalec = ciscenje_niza (izvajalec_v_celici.get_text ())
                # Odstrani izvajalca in dobi pesem kot preostali tekst
                izvajalec_v_celici.extract ()
                pesem = ciscenje_niza (isci_a.get_text ())
            else: # Če nimamo povezave
                vrstice_pesem = [ciscenje_niza (vsebina) for vsebina in pesem_v_celici.get_text (separator = "\n").split ("\n") if ciscenje_niza (vsebina)]
                pesem = vrstice_pesem [0] if len (vrstice_pesem) > 0 else ""
                izvajalec = vrstice_pesem [1] if len (vrstice_pesem) > 1 else ""      # 3. stolpec: izvajalec pesmi

            pts = teksti [3].split () [0] if len (teksti) > 3 and teksti [3] else ""
            tocke = int (pts) if pts.isdigit () else None           # 4. stolpec: končno št. točk


            # Po letu 2016 se način točkovanja spremeni: loči se žirija od publike.
            if leto >= 2016:
                publika_deli = teksti [4].split () if len (teksti) > 4 else []
                tocke_publike = int (publika_deli [0]) if publika_deli and publika_deli [0].isdigit () else None       # 5. stolpec: žirija/publika
                zirija_deli = teksti [5].split () if len (teksti) > 5 else []
                tocke_zirije = int (zirija_deli [0]) if zirija_deli and zirija_deli [0].isdigit () else None
                start_deli = teksti [6].split () if len (teksti) > 6 else []                      # 6. stolpec: running order pesmi
                startna_stevilka = int (start_deli [0]) if start_deli and start_deli [0].isdigit () else None
            else:
                tocke_publike = None
                tocke_zirije = None
                start_deli = teksti [4].split () if len (teksti) > 4 else []                      # 5. stolpec: running order pesmi
                startna_stevilka = int (start_deli [0]) if start_deli and start_deli [0].isdigit () else None
                
            podatki.append ({
                'leto': leto,
                'mesto': koncna_pozicija,
                'drzava': drzava,
                'pesem': pesem,
                'izvajalec': izvajalec,
                'tocke': tocke,
                'tocke_publike': tocke_publike,
                'tocke_zirije': tocke_zirije,
                'startna_stevilka': startna_stevilka,
            })
    return podatki
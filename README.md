# **Projektna naloga iz Uvoda v programiranje**
## Analiza podatkov o tekmovanju za pesem Evrovizije

**Avtor**: Maj Komac

Za namen projektne naloge sem uporabil podatke o rezultatih tekmovanja za pesem Evrovizije s spletne strani [Eurovision World](https://eurovisionworld.com/eurovision/).
Cilj projektne naloge je bil raziskati in analizirati zgodovinske podatke Evrovizije od leta 1956 naprej. Analiza se osredotoča na točke zmagovalcev, vpliv štartne številke na končno uvrstitev, primerjavo med točkami žirije in publike, uspešnost posameznih držav skozi čas in pevcev ter pevk, ki so nastopili.

## Navodila za uporabo

Uporabnik potrebuje naslednje knjižnice:

* `os` (delo z datotečnim sistemom in ustvarjanje map),
* `csv` (zapisovanje izluščenih podatkov v datoteko CSV),
* `selenium` (prenos dinamičnih spletnih strani z izvajanjem JavaScripta),
* `time` (upravljanje s časovnimi zamiki pri zajemu),
* `bs4` / `BeautifulSoup` (parsiranje HTML vsebine in izluščevanje podatkov),
* `pandas` (obdelava in analiza podatkov v Jupyter Notebooku),
* `matplotlib.pyplot` (za risanje grafov),
* `seaborn` (naprednejša statistična vizualizacija in estetski izris grafov),
* `numpy` (numerični izračuni in matematične operacije nad podatki).

Za pridobitev podatkov s spleta poženemo datoteko `glavna.py`. Program v mapo `zajeti_podatki/` prenese HTML datoteke za vsa leta, iz njih izlušči podatke (uvrstitev, država, izvajalec, pesem, točke žirije/publike, štartna številka) ter ustvari končno datoteko `podatki/evrovizija.csv` za nadaljnjo analizo.

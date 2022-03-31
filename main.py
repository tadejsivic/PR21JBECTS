import time

import numpy as np
#import Orange
import pandas as pd


# Spremenljivke za uporabljene stolpce
prva_reg = '2A-Datum prve registracije vozila v SLO'
status = 'Status vozila (id)'
enota_prve_reg = 'Izvajalna enota prve registracije'
reg_obmocje_tablice = '4A-Registrsko obmocje tablice prve registracije'
starost_upoabnika = 'C-Starost uporabnika vozila'
uporabnik_pravna_ali_fizicna = 'C-Ali je uporabnik pravna ali fizicna oseba'
spol_uporabnika = 'C-Spol uporabnika (ce gre za fizicno osebo)'
ali_je_uporabnik_lastnik = 'C-Ali je uporabnik tudi lastnik vozila'
upravna_enota_uporabnika = 'C13-Upravna enota uporabnika vozila (opis)'
obcina_uporabnika = 'C13-Obcina uporabnika vozila (opis)'
starost_lastnika = 'C2-Starost lastnika vozila'
lastnik_pravna_ali_fizicna = 'C2-Ali je lastnik pravna ali fizicna oseba'
spol_lastnika = 'C2-Spol lastnika (ce gre za fizicno osebo)'
znamka = 'D1-Znamka'
komerc_oznaka = 'D3-Komerc oznaka'
drzava = 'D42-Drzava (koda)'
ndm = 'F1-Najvecja tehnicno dovoljena masa vozila'
ndm_skupine = 'F3-Najvecja dovoljena masa skupine vozil pri registraciji'
masa = 'G-Masa vozila'
kategorija_in_vrsta = 'J-Kategorija in vrsta vozila (opis)'
delovna_prostornina = 'P11-Delovna prostornina'
moc = 'P12-Nazivna moc'
vrsta_goriva = 'P13-Vrsta goriva (oznaka)'
vrtilna_frekvenca = 'P14-Nazivna vrtilna frekvenca'
barva = 'R-Barva vozila (opis)'
st_sedezev = 'S1-Stevilo sedezev (vkljucno z vozniskim)'
najvisja_hitrost = 'T-Najvisja hitrost'
co = 'V1-CO'
nox = 'V3-Nox'
delci_pri_dizel = 'V5-Delci pri dizel motorjih'
co2 = 'V7-CO2'
poraba = 'V8-Kombinirana poraba goriva'
okoljevarstvena_oznaka = 'Okoljevarstvena oznaka'
oblika_nadgradnje = 'X-Oblika nadgradnje (opis)'
dolzina = 'Y1-Dolzina'
sirina = 'Y2-Sirina'
visina = 'Y3-Visina'
prevozeni_km = 'Prevozeni kilometri milje' # V MILJAH!!!




def main():
    print("____________ WELCOME TO DATA ANALYZER ____________")
    print("Reading data.....")
    data = load_data()

    print("Shape",data.shape)
    print("First few rows:")
    print(data.head())




def load_data():
    s_time = time.time()
    data = pd.read_csv("podatki.csv", sep=';', low_memory=False)
    e_time = time.time()
    print("Done!")
    print("Data loaded in",e_time-s_time,"seconds.")
    return data


if __name__ == '__main__':
    main()


# TODO:
# -Vizualizacija
# -Kakšna uporabna povprečja (poraba goriva, starost vozil, starost uporabnikov, moč vozil, hitrosti, dimenzije, ...)
# -Extensive big data time research xd -> morda analiza po časovnih obdobjih (kdaj se najpogosteje registrirajo avtomobili, ali uniformno čez leto, ali peak, ...)
# -Interpretacijski podatki -> katera vozila kupujejo kateri ljudje (študenti, ženske, starejši ljudje, ...),
#                           -> kako zeleni smo slovenci (co, co2, poraba, nox, euro6, in to v razmislek)
# -Povezovalni podatki -> kaj vpliva na porabo, kaj vpliva na najvisjo hitrost, ...












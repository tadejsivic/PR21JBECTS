import time

from operator import itemgetter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import Orange

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
prevozeni_km = 'Prevozeni kilometri milje'  # V MILJAH!!!


def main():
    print("____________ WELCOME TO DATA ANALYZER ____________")
    print("Reading data.....")
    data = load_data()
    # avg_calculations(data)
    # popular_car_brands(data)
    people_analysis(data)


def load_data():
    s_time = time.time()
    data = pd.read_csv("podatki.csv", sep=';', low_memory=False)
    e_time = time.time()
    print("Done!")
    print("Data loaded in", e_time - s_time, "seconds.")
    return data


def people_analysis(data):
    # age groups 16-24, 25-34, 35-44, 45-54, 55-64, 65+
    age_data = data[starost_upoabnika].to_numpy()
    brand_data = data[znamka].to_numpy()
    result = np.column_stack((age_data, brand_data))
    result = result[~np.isnan(age_data)]

    young = np.array([x for x in result if 16 <= x[0] < 25])
    popular_car_brands(young[:, 1], "mlade (16-24)")
    young_adult = np.array([x for x in result if 25 <= x[0] < 35])
    adult = np.array([x for x in result if 35 <= x[0] < 45])
    middle_aged = np.array([x for x in result if 45 <= x[0] < 55])
    senior = np.array([x for x in result if 55 <= x[0] < 65])
    elder = np.array([x for x in result if 65 <= x[0] < 90])
    popular_car_brands(elder[:, 1], "starejse (65+)")

    age_groups = ["16-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    number_of_drivers = [len(young) / len(result), len(young_adult) / len(result), len(adult) / len(result), len(middle_aged) / len(result), len(senior) / len(result), len(elder) / len(result)]

    plt.bar(age_groups, number_of_drivers)
    plt.xlabel("Starostne skupine")
    plt.ylabel("Delez voznikov")
    plt.title("Delez voznikov posamezne starostne skupine")
    plt.show()


def popular_car_brands(data, bar_title):
    # Load all car brands data and replace 'MERCEDES-BENZ' with 'MERCEDEZ BENZ' to remove duplicate columns
    car_brands = [x if (x != "MERCEDES-BENZ") else "MERCEDES BENZ" for x in data]
    car_brands = np.array(car_brands, dtype="object")
    unique, counts = np.unique(car_brands, return_counts=True)
    result = np.column_stack((unique, counts))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    result = [x for x in result if x[1] > 0.01*len(car_brands)]  # Only use the more popular brands for a nice graph
    fig = plt.figure(figsize=(10, 10))
    brands = [x[0] for x in result]
    brand_count = [x[1] / len(car_brands) for x in result]  # turn the numbers into %
    plt.bar(brands, brand_count)
    plt.gca().set_xticklabels(brands, rotation=90)
    plt.xlabel("Znamke")
    plt.ylabel("Delez vozil")
    plt.title("Delez registriranih vozil posamezne znamke za " + bar_title)
    plt.show()

    print("---------10 najbolj popularnih znamk v sloveniji za " + bar_title +"-----------")
    for index, element in enumerate([x[0] for x in result[:10]]):
        print(str(index + 1) + ".", element)


def avg_calculations(data):
    poraba_data = data[poraba].to_numpy()
    komerc_oznaka_data = data[komerc_oznaka].to_numpy()
    skupaj = np.array(list(zip(poraba_data, komerc_oznaka_data)))
    skupaj = skupaj[~np.isnan(poraba_data)]
    data_sorted = sorted(skupaj, key=lambda x: float(x[0]), reverse=True)
    avg_poraba = np.mean([float(x[0]) for x in data_sorted[200:]])

    plt.figure(figsize=(12, 12))
    plt.hist([float(x[0]) for x in data_sorted[200:]], label="Poraba avtov", density=False, bins=20)
    plt.xlabel("poraba")
    plt.ylabel("število vozil")
    plt.axvline(avg_poraba, color='k', linestyle='dashed', linewidth=2)
    plt.show()


if __name__ == '__main__':
    main()

# TODO:
# -Vizualizacija
# -Kakšna uporabna povprečja (poraba goriva, starost vozil, starost uporabnikov, moč vozil, hitrosti, dimenzije, ...)
# -Extensive big data time research xd -> morda analiza po časovnih obdobjih (kdaj se najpogosteje registrirajo avtomobili, ali uniformno čez leto, ali peak, ...)
# -Interpretacijski podatki -> katera vozila kupujejo kateri ljudje (študenti, ženske, starejši ljudje, ...),
#                           -> kako zeleni smo slovenci (co, co2, poraba, nox, euro6, in to v razmislek)
# -Povezovalni podatki -> kaj vpliva na porabo, kaj vpliva na najvisjo hitrost, ...

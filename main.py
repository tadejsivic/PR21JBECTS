import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    consumption_data = data[poraba].to_numpy()
    power_data = data[moc].to_numpy()

    result = np.array((age_data, brand_data, consumption_data, power_data), dtype="object")

    # TODO:fix this shit
    mask = ~np.isnan(age_data)
    age_data = result[0][mask]
    brand_data = result[1][mask]
    consumption_data = result[2][mask]
    power_data = result[3][mask]
    result = np.array((age_data, brand_data, consumption_data, power_data), dtype="object")

    age_groups = ["16-24", "25-34", "35-44", "45-54", "55-64", "65+"]

    # Getting data by age group
    young = result[:, (12 <= result[0]) & (result[0] < 25)]
    young_adult = result[:, (25 <= result[0]) & (result[0] < 34)]
    adult = result[:, (35 <= result[0]) & (result[0] < 44)]
    middle_aged = result[:, (45 <= result[0]) & (result[0] < 54)]
    senior = result[:, (55 <= result[0]) & (result[0] < 64)]
    elder = result[:, (65 <= result[0]) & (result[0] < 90)]

    # Showing data of popular car brands by age group
    popular_car_brands(young[1], "mlade (12-24)")
    popular_car_brands(elder[1], "starejse (65+)")

    # calculating average consumption by age group and visualizing it
    avg_consumption_by_age_group = [avg_consumption(young[2], False), avg_consumption(young_adult[2], False),
                                    avg_consumption(adult[2], False), avg_consumption(middle_aged[2], False),
                                    avg_consumption(senior[2], False), avg_consumption(elder[2], False)]
    plt.bar(age_groups, avg_consumption_by_age_group)
    plt.xlabel("Starostne skupine")
    plt.ylabel("povprecna poraba")
    plt.title("povprecna poraba posamezne starostne skupine")
    plt.axhline(np.mean(avg_consumption_by_age_group), color='k', linestyle='dashed', linewidth=2)
    plt.show()

    # calculating average vehicle power by age group
    avg_power_by_age_group = [avg_power(young[3]), avg_power(young_adult[3]), avg_power(adult[3]), avg_power(middle_aged[3]), avg_power(senior[3]), avg_power(elder[3])]
    plt.bar(age_groups, avg_power_by_age_group)
    plt.xlabel("Starostne skupine")
    plt.ylabel("povprecna moc vozil (kW)")
    plt.title("povprecna moc vozil posamezne starostne skupine")
    plt.axhline(np.mean(avg_power_by_age_group), color='k', linestyle='dashed', linewidth=2)
    plt.show()


    number_of_drivers = [len(young[0]) / len(result[0]), len(young_adult[0]) / len(result[0]),
                         len(adult[0]) / len(result[0]),
                         len(middle_aged[0]) / len(result[0]), len(senior[0]) / len(result[0]),
                         len(elder[0]) / len(result[0])]

    plt.bar(age_groups, number_of_drivers)
    plt.xlabel("Starostne skupine")
    plt.ylabel("Delez voznikov")
    plt.title("Delez voznikov posamezne starostne skupine")
    plt.show()


def avg_power(data):
    data = data.astype('float64')
    power_data = data[~np.isnan(data)]
    power_data = [x for x in power_data if 0 < x < 1000]
    return np.mean(power_data)

def popular_car_brands(data, bar_title):
    # Load all car brands data and replace 'MERCEDES-BENZ' with 'MERCEDEZ BENZ' to remove duplicate columns
    car_brands = [x if (x != "MERCEDES-BENZ") else "MERCEDES BENZ" for x in data]
    car_brands = np.array(car_brands, dtype="object")
    unique, counts = np.unique(car_brands, return_counts=True)
    result = np.column_stack((unique, counts))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    result = [x for x in result if x[1] > 0.01 * len(car_brands)]  # Only use the more popular brands for a nice graph
    fig = plt.figure(figsize=(10, 10))
    brands = [x[0] for x in result]
    brand_count = [x[1] / len(car_brands) for x in result]  # turn the numbers into %
    plt.bar(brands, brand_count)
    plt.gca().set_xticklabels(brands, rotation=90)
    plt.xlabel("Znamke")
    plt.ylabel("Delez vozil")
    plt.title("Delez registriranih vozil posamezne znamke za " + bar_title)
    plt.show()

    print("---------10 najbolj popularnih znamk v sloveniji za " + bar_title + "-----------")
    for index, element in enumerate([x[0] for x in result[:10]]):
        print(str(index + 1) + ".", element)


def avg_consumption(data, show_graph):
    data = data.astype('float64')
    consumption_data = data[~np.isnan(data)]
    data_sorted = sorted(consumption_data, reverse=True)
    avg_poraba = np.mean([x for x in data_sorted if x < 15])
    if show_graph:
        plt.figure(figsize=(12, 12))
        plt.hist([x for x in data_sorted if x < 15], label="Poraba avtov", density=False)
        plt.xlabel("poraba")
        plt.ylabel("število vozil")
        plt.axvline(avg_poraba, color='k', linestyle='dashed', linewidth=2)
        plt.show()
    return avg_poraba


if __name__ == '__main__':
    main()

# TODO:
# -Vizualizacija
# -Kakšna uporabna povprečja (poraba goriva, starost vozil, starost uporabnikov, moč vozil, hitrosti, dimenzije, ...)
# -Extensive big data time research xd -> morda analiza po časovnih obdobjih (kdaj se najpogosteje registrirajo avtomobili, ali uniformno čez leto, ali peak, ...)
# -Interpretacijski podatki -> katera vozila kupujejo kateri ljudje (študenti, ženske, starejši ljudje, ...),
#                           -> kako zeleni smo slovenci (co, co2, poraba, nox, euro6, in to v razmislek)
# -Povezovalni podatki -> kaj vpliva na porabo, kaj vpliva na najvisjo hitrost, ...

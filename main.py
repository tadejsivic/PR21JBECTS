import time
from builtins import type

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

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
prevozeni_km = 'Prevozeni kilometri milje'  # V MILJAH - ne vem več če je v miljah, zdaj dvomim


def main():
    print("____________ WELCOME TO DATA ANALYZER ____________")
    print("Reading data.....")
    data = load_data()
    people_analysis(data)
    CO2(data)
    ManufactureCO2(data)
    TrdiDelci(data)
    avto(data)



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
    car_age_data = data[prva_reg].to_numpy()
    reg_obmocje_tablice_data = data[reg_obmocje_tablice].to_numpy()
    lastnik_age_data = data[starost_lastnika].to_numpy()
    uporabnik_age_data = data[starost_upoabnika].to_numpy()
    lastnik_spol_data = data[spol_lastnika].to_numpy()
    uporabnik_spol_data = data[spol_uporabnika].to_numpy()
    drzava_data = data[drzava].to_numpy()
    color_data = data[barva].to_numpy()
    milje_data = data[prevozeni_km].to_numpy()

    # Creating and applying mask to data, so we get only legal values
    mask = ~np.isnan(age_data)
    age_data = age_data[mask]
    brand_data = brand_data[mask]
    consumption_data = consumption_data[mask]
    power_data = power_data[mask]
    reg_obmocje_tablice_data = reg_obmocje_tablice_data[mask]
    lastnik_age_data = lastnik_age_data[mask]
    uporabnik_age_data = uporabnik_age_data[mask]
    lastnik_spol_data = lastnik_spol_data[mask]
    uporabnik_spol_data = uporabnik_spol_data[mask]
    color_data = color_data[mask]
    drzava_data = drzava_data[mask]
    car_age_data = car_age_data[mask]
    milje_data = milje_data[mask]

    result = np.array((age_data,
                       brand_data,
                       consumption_data,
                       power_data,
                       reg_obmocje_tablice_data,
                       lastnik_age_data,
                       uporabnik_age_data,
                       lastnik_spol_data,
                       uporabnik_spol_data,
                       drzava_data,
                       color_data,
                       car_age_data,
                       milje_data),
                      dtype="object")

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
    avg_consumption_by_age_group = [avg_consumption(young[2], False),
                                    avg_consumption(young_adult[2], False),
                                    avg_consumption(adult[2], False),
                                    avg_consumption(middle_aged[2], False),
                                    avg_consumption(senior[2], False),
                                    avg_consumption(elder[2], False)]

    plt.bar(age_groups, avg_consumption_by_age_group)
    plt.xlabel("Starostne skupine")
    plt.ylabel("Povprecna poraba")
    plt.title("Povprecna poraba avta posamezne starostne skupine")
    plt.axhline(np.mean(avg_consumption_by_age_group), color='k', linestyle='dashed', linewidth=2)
    plt.show()

    avg_car_age_data = [np.mean(avg_car_age(young[-2])),
                        np.mean(avg_car_age(young_adult[-2])),
                        np.mean(avg_car_age(adult[-2])),
                        np.mean(avg_car_age(middle_aged[-2])),
                        np.mean(avg_car_age(senior[-2])),
                        np.mean(avg_car_age(elder[-2]))]

    plt.bar(age_groups, avg_car_age_data)
    plt.xlabel("Starostne skupine")
    plt.ylabel("Povprecna starost avta")
    plt.title("Povprecna starost avta posamezne starostne skupine")
    plt.axhline(np.mean(avg_car_age_data), color='k', linestyle='dashed', linewidth=2)
    plt.show()

    print("Average car age by age group")
    print(np.mean(avg_car_age(car_age_data)))

    # Showin data of km/year driven
    miles = [
        miles_analysis((young[-1], avg_car_age(young[-2]))),
        miles_analysis((young_adult[-1], avg_car_age(young_adult[-2]))),
        miles_analysis((adult[-1], avg_car_age(adult[-2]))),
        miles_analysis((middle_aged[-1], avg_car_age(middle_aged[-2]))),
        miles_analysis((senior[-1], avg_car_age(senior[-2]))),
        miles_analysis((elder[-1], avg_car_age(elder[-2])))]

    plt.bar(age_groups, miles)
    plt.xlabel("Starostne skupine")
    plt.ylabel("Povprecna letna prevozena razdalja")
    plt.title("Povprecna letna prevozena razdalja po starostnih skupinah")
    plt.axhline(miles_analysis((result[-1], avg_car_age(result[-2]))), color='k', linestyle='dashed', linewidth=2)
    plt.show()

    # calculating average vehicle power by age group
    avg_power_by_age_group = [avg_power(young[3]), avg_power(young_adult[3]), avg_power(adult[3]),
                              avg_power(middle_aged[3]), avg_power(senior[3]), avg_power(elder[3])]
    plt.bar(age_groups, avg_power_by_age_group)
    plt.xlabel("Starostne skupine")
    plt.ylabel("povprecna moc vozil (kW)")
    plt.title("povprecna moc vozil posamezne starostne skupine")
    plt.axhline(np.mean(avg_power_by_age_group), color='k', linestyle='dashed', linewidth=2)
    plt.show()

    number_of_drivers = [(len(young[0]) / len(result[0])) * 100,
                         (len(young_adult[0]) / len(result[0])) * 100,
                         (len(adult[0]) / len(result[0])) * 100,
                         (len(middle_aged[0]) / len(result[0])) * 100,
                         (len(senior[0]) / len(result[0])) * 100,
                         (len(elder[0]) / len(result[0])) * 100]

    plt.bar(age_groups, number_of_drivers)
    plt.xlabel("Starostne skupine")
    plt.ylabel("Delez voznikov")
    plt.title("Delez voznikov posamezne starostne skupine")
    plt.show()

    reg_območje(reg_obmocje_tablice_data)
    color_analysis(result[-3])
    uvoz_vozil(result[-4])

    owners = [
        owner_analysis(young[5:9]),
        owner_analysis(young_adult[5:9]),
        owner_analysis(adult[5:9]),
        owner_analysis(middle_aged[5:9]),
        owner_analysis(senior[5:9]),
        owner_analysis(elder[5:9])
    ]

    plt.bar(age_groups, owners)
    plt.xlabel("Starostne skupine")
    plt.ylabel("delez izposojenih avtov")
    plt.title("Delez ljudi, ki si izposoja avto")
    plt.show()



def gender_analysis(data):
    gender_data = data[spol_uporabnika].to_numpy()
    brand_data = data[znamka].to_numpy()
    consumption_data = data[poraba].to_numpy()
    power_data = data[moc].to_numpy()
    car_age_data = data[prva_reg].to_numpy()
    milje_data = data[prevozeni_km].to_numpy()

    male_mask = gender_data == "M"
    female_mask = gender_data == "Z"

    brand_data_m = brand_data[male_mask]
    consumption_data_m = consumption_data[male_mask]
    power_data_m = power_data[male_mask]
    car_age_data_m = car_age_data[male_mask]
    milje_data_m = milje_data[male_mask]

    brand_data_f = brand_data[female_mask]
    consumption_data_f = consumption_data[female_mask]
    power_data_f = power_data[female_mask]
    car_age_data_f = car_age_data[female_mask]
    milje_data_f = milje_data[female_mask]

    print(avg_consumption(consumption_data_m, False), avg_consumption(consumption_data_f, False))
    print(avg_power(power_data_m), avg_power(power_data_f))
    print(avg_car_age(car_age_data_m), avg_car_age(car_age_data_f))
    popular_car_brands(brand_data_m, "kaj vozijo moški")
    popular_car_brands(brand_data_f, "kaj vozijo ženske")

    miles_analysis((milje_data_m, avg_car_age(car_age_data_m)))
    miles_analysis((milje_data_f, avg_car_age(car_age_data_f)))


def legal_entities_analysis(data):
    None


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
    result = sorted(result, key=lambda x: x[1])
    result = result[-10:]  # Only use the more popular brands for a nice graph
    brands = [x[0] for x in result]
    brand_count = [(x[1] / len(car_brands)) * 100 for x in result]  # turn the numbers into %
    fig, ax = plt.subplots()
    fig.tight_layout(pad=7)
    plt.barh(brands, brand_count)
    plt.xlabel("Delez vozil")
    plt.ylabel("Znamke")
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


def avg_car_age(data):
    CURRENT_YEAR = 2021
    data = [x for x in data if type(x) is str]
    data = [CURRENT_YEAR - int(x.split(".")[2]) for x in data if type(x) is str]
    return data


def car_category_analysis(data):
    unique, counts = np.unique(data, return_counts=True)
    result = np.column_stack((unique, counts))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    result = [x for x in result if x[1] > 2500]  # Only use the more popular brands for a nice graph
    brands = [x[0] for x in result]
    brand_count = [x[1] / len(data) for x in result]  # turn the numbers into %
    fig, ax = plt.subplots()
    fig.tight_layout(pad=10)
    plt.bar(brands, brand_count)
    plt.xticks(rotation="vertical")
    plt.xlabel("Znamke")
    plt.ylabel("Delez vozil")
    plt.title("Delez registriranih vozil posamezne znamke za ")
    plt.show()


def reg_območje(data):
    unique, counts = np.unique(data, return_counts=True)
    result = np.column_stack((unique, counts))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    result = result[0:-4]

    reg_oznaka = [x[0] for x in result]
    st_pojavitev = [(x[1] / len(data)) * 100 for x in result]

    # Podatki o populaciji v regijah iz SURS
    population = 1700000
    st_prebivalcev = [
        452097 / population * 100,
        273649 / population * 100,
        212095 / population * 100,
        171562 / population * 100,
        98868 / population * 100,
        97571 / population * 100,
        117819 / population * 100,
        96600 / population * 100,
        62427 / population * 100,
        58471 / population * 100,
        43539 / population * 100]

    fig, ax = plt.subplots()
    fig.tight_layout(pad=10)

    x_axis = np.arange(len(reg_oznaka))

    plt.bar(x_axis - 0.2, st_pojavitev, 0.4, label="regijske oznake")
    plt.bar(x_axis + 0.2, st_prebivalcev, 0.4, label="st. prebivalcev")

    plt.xticks(x_axis, reg_oznaka, rotation="vertical")
    plt.xlabel("Registerska oznaka")
    plt.ylabel("Delež registerskih")
    plt.title("Delež registerskih oznak")
    plt.legend()
    plt.show()


def uvoz_vozil(data):
    unique, counts = np.unique(data, return_counts=True)
    result = np.column_stack((unique, counts))
    result = sorted(result, key=lambda x: x[1])
    result = result[-10:]  # Only use the top 10 import countries
    country_codes = [x[0] for x in result]
    number_of_imports = [(x[1] / len(data)) * 100 for x in result]  # turn the numbers into %
    fig, ax = plt.subplots()
    fig.tight_layout(pad=4)
    plt.barh(country_codes, number_of_imports)
    plt.ylabel("Države izvora")
    plt.xlabel("Delež uvoženih avtov")
    plt.title("Delež uvoženih avtov glede na državo")
    plt.show()


def owner_analysis(data):
    lastnik_age_data = data[0]
    uporabnik_age_data = data[1]
    lastnik_spol_data = data[2]
    uporabnik_spol_data = data[3]
    count = 0

    for i in range(0, len(lastnik_spol_data)):
        if lastnik_age_data[i] != uporabnik_age_data[i] or lastnik_spol_data[i] != uporabnik_spol_data[i]:
            count += 1

    return (count / len(lastnik_spol_data)) * 100


def color_analysis(data):
    data = data.astype(str)
    data = [x.split("-")[1].strip() for x in data if x != "nan"]
    unique, counts = np.unique(data, return_counts=True)
    result = np.column_stack((unique, counts))
    result = sorted(result, key=lambda x: int(x[1]))

    colors = [x[0] for x in result]
    percentage_of_cars = [(int(x[1]) / len(data)) * 100 for x in result]  # turn the numbers into %

    fig, ax = plt.subplots()
    fig.tight_layout(pad=5)
    plt.barh(colors, percentage_of_cars,
             color=['grey', 'white', 'black', 'red', 'blue', 'green', 'brown', 'orange', 'yellow', 'purple'][::-1],
             edgecolor='black')
    plt.xlabel("Delez avtov s to barvo")
    plt.ylabel("Barva")
    plt.title("Delež uporabljene barve")
    plt.show()


def miles_analysis(data):
    miles_data = data[0]
    car_age_data = data[1]
    answer = (np.nansum(miles_data) / np.nansum(car_age_data)) / 1.6
    return answer

def avto(data):
    brand_data = data[znamka].to_numpy()
    FirstReg_data = data[reg_obmocje_tablice].to_numpy()
    enota = data[enota_prve_reg].to_numpy()
    datum = data[prva_reg].to_numpy()
    model = data[komerc_oznaka].to_numpy()
    leta = data[starost_upoabnika].to_numpy()
    spol = data[spol_lastnika].to_numpy()
    lastnik = data[ali_je_uporabnik_lastnik].to_numpy()
    barvaa = data[barva].to_numpy()
    maxSpeed = data[najvisja_hitrost].to_numpy()
    kilometri = data[prevozeni_km].to_numpy()
    gorivo = data[vrsta_goriva].to_numpy()

    result = np.array((FirstReg_data, brand_data, enota, datum, model, leta, spol, lastnik, barvaa, maxSpeed, kilometri, gorivo), dtype="object")
   # print(result[:,0])
 #   for x in result[:,:]:
 #       print(x);
    #for x in data[reg_obmocje_tablice]:
    #    print(x)

 #   koper = [x for x in FirstReg_data if x == "KOPER"]
    koper = result[:,(result[1] == "FORD") & (result[4] == "C-MAX / 1.5 / SCTi EcoBoost 110 M6 S") & (result[5] == 49)]
 #   young_adult = result[:, (25 <= result[0]) & (result[0] < 34)]
    print()
    print()
    print()
    for x in koper.transpose():
        for y in x:
            print(y)
    print()
    print()
    print()


def CO2(data):
    FirstReg = data[prva_reg].to_numpy()
    Co = data[co2].to_numpy()
    result = np.array((FirstReg, Co), dtype="object")
    mask = ~np.isnan(Co)
    FirstReg = result[0][mask]
    Co = result[1][mask]
    result = np.array((FirstReg, Co), dtype="object")
    result = result.transpose()
    result = [x for x in result if x[1] < 441]
    result = [x for x in result if x[0] == x[0]]  # x!=x to naj bi nane dalo stran
    result = np.array(result)
    Date = result[:, 0]
    FirstRegYear = []
    for a in Date:
        FirstRegYear.append(int(a.split(".")[2]))
    FirstRegYear = np.array(FirstRegYear)
    result[:,0] = FirstRegYear
    letna_povprecja = dict()
    for leto in range(2010, 2021):
        letna_povprecja[leto] = result[result[:, 0] == leto, 1].mean()

    leta, CO2 = zip(*sorted(letna_povprecja.items()))
    plt.figure()
    plt.plot(leta, CO2)
    plt.xlabel("leto")
    plt.ylabel("Povprečen izpust CO2")
    plt.title("Povprečni izpusti CO2 za novo registrirana vozila")
    plt.show()


def ManufactureCO2(data):
    vrsta = data[kategorija_in_vrsta].to_numpy()
    brand = data[znamka].to_numpy()
    FirstReg = data[prva_reg].to_numpy()
    Co = data[co2].to_numpy()
    result = np.array((FirstReg, Co, brand, vrsta), dtype="object")
    mask = ~np.isnan(Co)
    FirstReg = result[0][mask]
    Co = result[1][mask]
    brand = result[2][mask]
    vrsta = result[3][mask]
    result = np.array((FirstReg, Co, brand, vrsta), dtype="object")
    result = result.transpose()
    result = [x for x in result if x[1] < 300]
    result = [x for x in result if x[0] == x[0]]  # x!=x to naj bi nane dalo stran
    result = np.array(result)
    Date = result[:, 0]
    FirstRegYear = []
    for a in Date:
        FirstRegYear.append(int(a.split(".")[2]))
    FirstRegYear = np.array(FirstRegYear)
    result[:, 0] = FirstRegYear

    Renault = list()
    for b in result:
        if b[2] == "RENAULT" and b[3] == "osebni avtomobil":
            Renault.append(b)
    Renault = np.array(Renault)
    letna_povprecjaRENAULT = dict()
    for leto in range(2010, 2021):
        letna_povprecjaRENAULT[leto] = Renault[Renault[:, 0] == leto, 1].mean()
    leta, CO2 = zip(*sorted(letna_povprecjaRENAULT.items()))
    plt.plot(leta, CO2, label="RENAULT")

    Volkswagen = list()
    for b in result:
        if b[2] == "VOLKSWAGEN" and b[3] == "osebni avtomobil":
            Volkswagen.append(b)
    Volkswagen = np.array(Volkswagen)
    letna_povprecjaVOLKSWAGEN = dict()
    for leto in range(2010, 2021):
        letna_povprecjaVOLKSWAGEN[leto] = Volkswagen[Volkswagen[:, 0] == leto, 1].mean()
    leta, CO2 = zip(*sorted(letna_povprecjaVOLKSWAGEN.items()))
    plt.plot(leta, CO2, label="VOLKSWAGEN")

    BMW = list()
    for b in result:
        if b[2] == "BMW" and b[3] == "osebni avtomobil":
            BMW.append(b)
    BMW = np.array(BMW)
    letna_povprecjaBMW = dict()
    for leto in range(2010, 2021):
        letna_povprecjaBMW[leto] = BMW[BMW[:, 0] == leto, 1].mean()
    leta, CO2 = zip(*sorted(letna_povprecjaBMW.items()))
    plt.plot(leta, CO2, label="BMW")

    AUDI = list()
    for b in result:
        if b[2] == "AUDI" and b[3] == "osebni avtomobil":
            AUDI.append(b)
    AUDI = np.array(AUDI)
    letna_povprecjaAUDI = dict()
    for leto in range(2010, 2021):
        letna_povprecjaAUDI[leto] = AUDI[AUDI[:, 0] == leto, 1].mean()
    leta, CO2 = zip(*sorted(letna_povprecjaAUDI.items()))
    plt.plot(leta, CO2, label="AUDI")

    AUDI = list()
    for b in result:
        if b[2] == "AUDI" and b[3] == "osebni avtomobil":
            AUDI.append(b)
    AUDI = np.array(AUDI)
    letna_povprecjaAUDI = dict()
    for leto in range(2010, 2021):
        letna_povprecjaAUDI[leto] = AUDI[AUDI[:, 0] == leto, 1].mean()
    leta, CO2 = zip(*sorted(letna_povprecjaAUDI.items()))
    plt.plot(leta, CO2, label="AUDI")

    TOYOTA = list()
    for b in result:
        if b[2] == "TOYOTA" and b[3] == "osebni avtomobil":
            TOYOTA.append(b)
    TOYOTA = np.array(TOYOTA)
    letna_povprecjaTOYOTA = dict()
    for leto in range(2010, 2021):
        letna_povprecjaTOYOTA[leto] = TOYOTA[TOYOTA[:, 0] == leto, 1].mean()
    leta, CO2 = zip(*sorted(letna_povprecjaTOYOTA.items()))
    plt.plot(leta, CO2, label="TOYOTA")

    ax = plt.gca()
    ax.set_ylim([90, 170])
    ax.set_xlim([2009, 2021])

    plt.xlabel("leto")
    plt.ylabel("Povprečen izpust CO2")
    plt.title("Povprečni izpusti CO2 za novo registrirana vozila")
    plt.legend(loc=1);
    plt.show()

def TrdiDelci(data):
    brand = data[znamka].to_numpy()
    gorivo = data[vrsta_goriva].to_numpy()
    vrsta = data[kategorija_in_vrsta].to_numpy()
    FirstReg = data[prva_reg].to_numpy()
    Delci = data[delci_pri_dizel].to_numpy()
    result = np.array((FirstReg, Delci, vrsta, gorivo, brand), dtype="object")
    mask = ~np.isnan(Delci)
    FirstReg = result[0][mask]
    Delci = result[1][mask]
    vrsta = result[2][mask]
    gorivo = result[3][mask]
    brand = result[4][mask]
    result = np.array((FirstReg, Delci, vrsta, gorivo, brand), dtype="object")
    result = result.transpose()
    result = [x for x in result if x[0] == x[0]] #x!=x to naj bi nane dalo stran
    result = [x for x in result if x[3] == "D"]  #avti na dizel
    result = [x for x in result if x[2] == "osebni avtomobil"]  # gledamo samo osebne avtomobile
    result = [x for x in result if x[1] != 0] #ne sme bit nič  #avti na dizel ne morejo imeti nič
    result = [x for x in result if x[1] < 1]  #nima smisla več ko to delcev, če je več kot 1 sklepam kot napačen vnos
    result = np.array(result)
    Date = result[:, 0]
    FirstRegYear = []
    for a in Date:
        FirstRegYear.append(int(a.split(".")[2]))

    FirstRegYear = np.array(FirstRegYear)
    result[:,0] = FirstRegYear
    letna_povprecja = dict()
    for leto in range(2010, 2021):
        letna_povprecja[leto] = result[result[:, 0] == leto, 1].mean()

    leta, Delci = zip(*sorted(letna_povprecja.items()))
    plt.figure()
    plt.plot(leta, Delci)
    plt.xlabel("leto")
    plt.ylabel("Povprečen izpust trdih delcev")
    plt.title("Povprečni izpusti TRDIH DELCEV za novo registrirana vozila")
    plt.show()


if __name__ == '__main__':
    main()

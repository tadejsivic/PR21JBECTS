# PR21JBECTS
Data Mining project at University of Ljubljana

## Vmesno poročilo:

### Problem

Problem predstavlja analizo registriranih vozil, torej uporabnike določenih vozil, lastnosti teh vozil, parametre odločanja nakupa.
To je predstavljeno kot več manjših ugotovitev, z nekim zaokroženim zaključkom na koncu. Ta bo upošteval:
- Analizo starostnih skupin uporabnikov[^1] (fizične osebe) - kaj kdo kupuje
- Analizo pravnih oseb (podjetja) - kakšne tipe vozil v glavnem kupujejo podjetja
- Analizo lastnosti vozil  - upoštevano po porabi goriva, moči motorja, starosti vozila, prevoženi razdalji, ...
- Analizo vpliva na okolje - električni avtomobili, porabo co2, co, okoljevarstveno oznako motorja (npr. euro6), ...

[^1]: v zbirki so ljudje ločeni v uporabnike ter lastnike. Lastnik je človek, ki je zapisan na listu kot lastnik, ni pa nujno uporabnik. Uporabnik je človek, kateri vozilo letno registrira in ga uporablja.

### Podatki

Podatki so bili v veliki zbirki (3 datotekah csv, vsaka po 650 000 vrstic, vsaka 108 stolpcev).
Podatke smo izluščili iz ene datoteke, saj jih je bilo veliko. Če bi obravnavali vse podatke, bi porabili veliko več časa, razultati pa bi bili precej podobni (650 000 je reprezentativno za Slovenijo).
Uporabili smo le 38 pomembnejših stolpcev, tako smo si količino podatkov še zmanjšali.

Kljub temu, da je zbirka uradna z ministrstva za infrastukturo, je še vedno ogromno napak. Poleg manjkajočih vrednosti (katere so razumljive), je veliko več človeških napak.

Ponekod so bile porabe goriva nenormalne, kar 40 000 L/100km (fiat punto, morda predelan), neko vozilo je imelo 1160 sedežev (bil je traktor), nekateri Slovenci vozijo super traktorje z 2500 kW moči, ponekod so avte vozili  4-letniki, nekje pa 114-letniki.
Predpriprava podatkov nam je torej vzela večino časa. Poleg priprave zbrike, je bilo ogromno filtriranja manjkajočih vrednosti ter nesmiselnih vrednosti.

### Ugotovitve in analize

Najprej smo vse uporabnike razdelili na fizične in pravne osebe. Trenutno smo obravnavali le fizične osebe (pravne še pridejo na vrsto).
Fizične osebe smo razdelili v starostne skupine. Te so sledeče:
- Young [12-24][^2]
- Young Adults [25-34]
- Adults [35-44]
- Middle Aged [45-55]
- Senior [55-64]
- Elder [65+]

[^2]: Prvotno je bila starost od 16 naprej, vendar lahko tudi 12-letniki s kolesarskim izpitom vozijo motorna kolesa, zato smo prilagodili meje.

Porazdelitev je nekoliko pričakovana.

![Delež voznikov posameznih starostnih skupin](/img/vozniki_starostne_skupine.png)

#### Popularnost vozil
Nato smo si pogledali katera znamka avtomobila je najbolj priljubljena za mlade  in katera za starejše ljudi. Tu smo pričakovali največjo razliko.

10 najbolj popularnih znamk v sloveniji za mlade (12-24)
1. VOLKSWAGEN
2. RENAULT
3. AUDI
4. BMW
5. PEUGEOT
6. OPEL
7. CITROEN
8. ŠKODA
9. FORD
10. FIAT

![Najbolj popularni avti za mlade](/img/delez_vozil_mladi.png)


10 najbolj popularnih znamk v sloveniji za starejše (65+)
1. RENAULT
2. VOLKSWAGEN
3. OPEL
4. CITROEN
5. PEUGEOT
6. FORD
7. HYUNDAI
8. TOYOTA
9. MERCEDES BENZ
10. FIAT

![Najbolj popularni avti za starejše](/img/delez_vozil_stari.png)

Razvidno je, da sta VolksWagen in Renault najbolja popularna (to je podprto tudi iz drugih analiz, najbolj splošno priljubljen avto...).
Mlajši tudi vozijo več Audi-jev in BMW-jev, medtem ko starejši ostanejo pri preprostejših *Oplih* in *Citroenih*.
Iz slike mladih se tudi prebere, da je veliko motorjev/motornih koles (sym, piaggio, tomos), medtem ko starešji posegajo bolj po traktorjih.

#### Moč in poraba vozil
Za vsako starostno skupino smo tudi analizirali, kako močna[^3] vozila uporabljajo.
Tu so vzeta vsa vozila, torej električna vozila in tovornjaki skupaj z motornimi kolesi. Podrobnejša analiza pod vrstah vozil in vrstah goriv pride kasneje.

[^3]: Moč je v kilo-vatih [kW]

![Povprečna moč za starostne skupine](/img/moc_starostne_skupine.png)

Črtkana črta predstavlja globalno povprečno moč vozila, da si je lažje predstavljati, kdo je pod/nad povprečjem.
Najmočnejša vozila so imeli odrasli (okoli 30 let). Morda jih potrebujejo za delo, oz. so najbolj premožni.

Izračunali smo tudi povprečno porabo vozil. Poraba je bila precej uniformno porazdeljena. 

![Povprečna poraba za starostne skupine](/img/poraba_starostne_skupine.png)

Slika kaže, da imajo starejši ljudje nekoliko višjo porabo.
Kar je zelo zanimivo, saj imajo starejši ljudje najraje avtomobile znamke Renault.
Poleg tega, so na prejšnji sliki imeli tudi najšibkejše avtomobile.

Morda pa ni vse v eko avotmobilih, ampak tudi voznikih ?!


V nadaljevanju projekta  bomo podrobneje analizirali take značilne statistike, vendar le za določene vrste vozil, določene vrste ljudi (morda po spolih), statisike za pravne osebe.

## Kako pognati kodo
Koda je napisana v python-u. Izvorna koda je v datoteki *main.py*.

Uporabili smo tudi knjižnico *numpy* , *matplotlib* in *pandas* (za uvoz podatkov).

Za pravilno delovanje programa so potrebne vse navedene knjižnice.

## Seznam opravil
- [x] Predpriprava podatkov
- [x] Začetna analiza in vizualizacija starostnih skupin
- [ ] Analiza pravnih oseb
- [ ] Analiza vpliva vozil na okolje












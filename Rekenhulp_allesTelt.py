import pandas as pd
import datetime
import os

# importeren csv bestand
inventory = pd.read_csv("alles_telt.csv", header=1)

# selecteren van kolommen en naamgeving makkelijker maken
inventory['blok_1'] = inventory['Blok 1']
studenten = inventory[['Naam', 'Totaal', 'blok_1']]
studenten = studenten.drop(studenten.index[-2:])

# omzetten naar bruikbare cijfers
studenten.Totaal = studenten['Totaal'].replace('[\%,]', '', regex=True)
studenten.Totaal = pd.to_numeric(studenten.Totaal)
studenten.blok_1 = studenten['blok_1'].replace('[\%,]', '', regex=True)
studenten.blok_1 = pd.to_numeric(studenten.blok_1)

# uitrekenen nieuw totaal (Totaal * 8 - Toets 1) * 7
studenten['totaal_n'] = studenten.apply(lambda row:(row['Totaal'] * 8 - row['blok_1'])/ 7, axis=1)
studenten['totaal_n'] = studenten.totaal_n.round().astype(int)

# uitrekenen rapportcijfer met functie

def rapport_cijfer(totaal_n):
    if totaal_n <= 50:
        return 3
    elif totaal_n == 100:
        return 100
    elif totaal_n < 100 and totaal_n >= 80:
        c = (100 - totaal_n ) * 0.2
        g = round((10 - c), 1)
        return g
    elif totaal_n < 80 and totaal_n > 50:
        c = (80 - totaal_n ) * 0.1
        g = round((6 - c), 1)
        return g


studenten['rapport'] = studenten.totaal_n.apply(rapport_cijfer)

# Opschonen dataframe / beter leesbaar maken

Nieuw_rapport = studenten[['Naam', 'rapport', 'totaal_n', 'Totaal', 'blok_1']]
Nieuw_rapport.rename(columns={
    'rapport': 'Rapportcijfer',
    'totaal_n': 'Nieuw percentage',
    'Totaal': 'Oud totaal',
    'blok_1': 'Cijfer blok 1'},
    inplace=True)

# Opslaan Resultaten
snapshotdata = datetime.datetime.today().strftime('%m-%d-%Y')
os.chdir('/home/trees/Documents')
Nieuw_rapport.to_csv(open('Alles_Telt_' + snapshotdata + '.csv','w'),index='Naam')
Nieuw_rapport.close()



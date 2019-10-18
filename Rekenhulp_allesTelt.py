import pandas as pd
import datetime
# import os

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


def rapport_cijfer(totaal_n):
    """Omrekenen nieuw totaal naar rapportcijfer"""
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
studenten['rToets1'] = studenten.blok_1.apply(rapport_cijfer)

# Opschonen dataframe / beter leesbaar maken

Nieuw_rapport = studenten[['Naam', 'blok_1', 'rToets1', 'rapport', 'totaal_n']]
Nieuw_rapport.rename(columns={
    'rapport': 'Rapportcijfer',
    'totaal_n': 'Nieuw totaal %',
    'rToets1': 'Toets 01 Rapport',
    'blok_1': 'Uitslag Toets 01'},
    inplace=True)

# Opslaan Resultaten
snapshotdata = datetime.datetime.today().strftime('%d-%m-%Y')
#os.chdir('/home/svenja/Rapport_AT')

with open('Alles_Telt_' + snapshotdata + '.csv', 'w') as RapportN:
    Nieuw_rapport.to_csv(RapportN, index='Naam')




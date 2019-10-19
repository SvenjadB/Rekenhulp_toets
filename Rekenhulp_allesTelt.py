#!/usr/bin/env python3
import easygui as gui
import pandas as pd

# TODO Juiste csv kolomtitels; het is niet blok 1 maar toets 1:
#  automatisering of iets dergelijks

# Vraag om bestand dat verwerkt moet worden
input_path = gui.fileopenbox(
    title="Choose a file...", default="*.csv")
if input_path is None:
    exit()
overzicht = pd.read_csv(input_path, header=1)

# selecteren van kolommen en naamgeving makkelijker maken
overzicht['blok_1'] = overzicht['Blok 1']
studenten = overzicht[['Naam', 'Totaal', 'blok_1']]
studenten = studenten.drop(studenten.index[-2:])

# omzetten naar bruikbare cijfers
studenten.Totaal = studenten['Totaal'].replace('[\%,]', '', regex=True)
studenten.Totaal = pd.to_numeric(studenten.Totaal)
studenten.blok_1 = studenten['blok_1'].replace('[\%,]', '', regex=True)
studenten.blok_1 = pd.to_numeric(studenten.blok_1)

# uitrekenen nieuw totaal (Totaal * 8 - Toets 1) * 7
studenten['totaal_n'] = studenten.apply(lambda row: (row['Totaal'] * 8 - row['blok_1']) / 7, axis=1)
studenten['totaal_n'] = studenten.totaal_n.round().astype(int)


def rapport_cijfer(totaal_n):
    """Omrekenen nieuw totaal naar rapportcijfer"""
    if totaal_n <= 50:
        return 3
    elif totaal_n == 100:
        return 100
    elif 100 > totaal_n >= 80:
        c = (100 - totaal_n ) * 0.2
        g = round((10 - c), 1)
        return g
    elif 80 > totaal_n > 50:
        c = (80 - totaal_n ) * 0.1
        g = round((6 - c), 1)
        return g


studenten['rapport'] = studenten.totaal_n.apply(rapport_cijfer)
studenten['rToets1'] = studenten.blok_1.apply(rapport_cijfer)

# CSV leesbare kolomtitels
Nieuw_rapport = studenten[['Naam', 'blok_1', 'rToets1', 'rapport', 'totaal_n']]
Nieuw_rapport.rename(columns={
    'rapport': 'Rapportcijfer',
    'totaal_n': 'Nieuw totaal %',
    'rToets1': 'Toets 01 Rapport',
    'blok_1': 'Uitslag Toets 01'},
    inplace=True)

# Vraag locatie en naam waar nieuw bestand opgeslagen moet worden
output_path = gui.filesavebox(
        title="Choose a file...", default="*.csv")
if output_path is None:
    exit()
with open(output_path, 'w') as RapportN:
    Nieuw_rapport.to_csv(RapportN, index='Naam')

### IMPORT DELLE LIBRERIE NECESSARIE AL FUNZIONAMENTO DEL BOT ###

import os
import re
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = '' # TOKEN DEL BOT

discordClient = discord.Client()  # Creazione dell'oggetto discordClient per l'ascolto degli eventi

### CONNESSIONE ALLE API GOOGLE PER ACCEDERE AL GOOGLE SHEET ###

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
googleClient = gspread.authorize(creds)


### FUNZIONE UTILE ALL'INSERIMENTO DEI DATI SUL GOOGLE SHEET ###

def insert(registro, sheet):
    str_list = list(filter(None, sheet.col_values(1)))
    next_row = int(len(str_list)+1)
    cliente = registro[1].upper()
    targa = registro[3].upper()
    modello = registro[5].upper()
    modifiche = registro[7].upper()
    prezzo = registro[9]
    sheet.update_cell(next_row, 1, cliente)
    sheet.update_cell(next_row, 2, targa)
    sheet.update_cell(next_row, 3, modello)
    sheet.update_cell(next_row, 4, modifiche)
    sheet.update_cell(next_row, 5, prezzo)


### MESSAGGIO VISUALIZZABILE IN CONSOLE PER AVVISARE CHE IL BOT E' CONNESSO AL SERVER E IN ASCOLTO ###

@discordClient.event
async def on_ready():
    print(f'{discordClient.user.name} si è connesso al server')


### FUNZIONE CHE SI ATTIVA NON APPENA VIENE INVIATO UN MESSAGGIO ###

@discordClient.event
async def on_message(message):

    print(message.author) # Prelievo dell'autore del messaggio
    print(message.content) # Prelievo del messaggio
    print(message.created_at) # Prelievo del momento di invio del messaggio

    if str(message.author)=='User#0000':
        registro=re.split(': |\n',message.content)
        sheet = googleClient.open("File").worksheet("Foglio")
        insert(registro, sheet)

discordClient.run(TOKEN) # Funzione per avviare il bot
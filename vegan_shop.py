import json
from vegan_shop_functions import *

def start_inventory():
    inventory =  load_inventory()
    command_list()
    while True:
        command = input("Inserisci un comando: ").lower()
        if command == "aiuto":
            command_list()
        elif command == "aggiungi":
            add_product(inventory)
        elif command == "elenca":
            list_inventory(inventory)
        elif command == "vendita":
            selling_product(inventory)
        elif command == "profitti":
            total_profits(inventory) 
        elif command == "chiudi":
            print("Programma in chiusura, bye bye")
            break
        else: 
            print("Comando non valido")
            command_list()
    
    save_inventory(inventory)

            
    return

if __name__ == "__main__":
    start_inventory()

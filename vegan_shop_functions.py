import json
def save_inventory(inventory,file_path="inventory.json"):
    """
    This function saves the inventory into a JSON file, by default called inventory.json
    Args:
        inventory (dict) : A dictionary where the keys are the product's names (str), each product is also a dictionary with the following keys:
        - "quantità" (int): quantity of the product
        - "prezzo di vendita" (float): selling price of the product
        file_path(str): A string containing the inventory file's path.
    Returns:
        None
    """
    with open (file_path,"w") as json_file:
        json.dump(inventory,json_file,indent=6)
        
def load_inventory(file_path="inventory.json"):
    """
    This function loads the inventory JSON file and initializes an empty inventory if the file does not exist.
    Args:
        file_path(str): A string containing the inventory file's path.
    Returns:
        inventory (dict) : A dictionary where the keys are the product's names (str).
    """
    try:
        with open (file_path,"r") as json_file:
            inventory = json.load(json_file)
    except FileNotFoundError: 
        inventory = {}
    return inventory
    
def command_list():
    """
    This function lists all the available commands.
    Args: 
        None
    Returns:
        None
    """
    print("I comandi disponibili sono i seguenti: ")
    print("aggiungi: aggiungi un prodotto al magazzino")
    print("elenca: elenca i prodotto in magazzino")
    print("vendita: registra una vendita effettuata")
    print("profitti: mostra i profitti totali")
    print("aiuto: mostra i possibili comandi")
    print("chiudi: esci dal programma")

def list_inventory(inventory):
    """
    This function lists all the item in the inventory with their quantity and selling price.
    Args: 
        inventory (dict) : A dictionary where the keys are the product's names (str), each product is also a dictionary with the following keys:
        - "quantità" (int): quantity of the product
        - "prezzo di vendita" (float): selling price of the product
    Returns: 
        None
    """
    print("%s\t%s\t%s\t" % ("Prodotto","Quantità","Prezzo vendita"))
    for product in inventory:
        print("%s\t\t%s\t\t%s\t\t" % (product,inventory[product]["quantità"],inventory[product]["prezzo di vendita"]))
    print("\n")
    
def add_product(inventory):
    """
    This function allows to add an item in the inventory.
    If the product already exists in the inventory only the quantity is updated. Otherwise the user will be asked to 
    enter also the buying and selling price.
    Args:
        inventory (dict): a dictionary where the keys are the product's names (str), each product is also a dictionary with the following keys:
        - "quantità" (int): quantity of the product
        - "prezzo di vendita" (float): selling price of the product
        - "prezzo di acquisto" (float): buying price of the product
    Returns:
        None
    """        
    product = input("Inserire nome del prodotto: ").lower()
    while True:
        try:
            quantity = int(input("Inserire la quantità: "))
            assert quantity > 0
            break
        except:
            print("La quantità deve essere un numero intero maggiore di 0.")   
            
    if product in inventory:
        inventory[product]["quantità"] += quantity
    else:
        while True: 
            try:
                buying_price = float(input("Inserire prezzo di acquisto: "))
                assert buying_price > 0
                break
            except:
                print("Il prezzo di acquisto deve essere un numero positivo.")
        while True: 
            try:
                selling_price = float(input("Inserire prezzo di vendita: "))
                assert selling_price > 0
                break
            except:
                print("Il prezzo di vendita deve essere un numero positivo.")
                
        inventory[product] = {"quantità":quantity,"prezzo di acquisto":buying_price,"prezzo di vendita":selling_price}
        
    save_inventory(inventory)
        
    print(f"Prezzo di acquisto: {inventory[product]['prezzo di acquisto']:.2f} €")
    print(f"Prezzo di vendita: {inventory[product]['prezzo di vendita']:.2f} €")
    print(f"Aggiunto {quantity} X {product}\n")
    # print(f"Inventario aggiornato:")
    # list_inventory(inventory)
  
    return inventory
    
def selling_product(inventory):
    
    """
    This function collects the products and the respective quantities the user wants to sell. check the availability in the inventory,
    updates the inventory and prints the sales summary.
    Args:
        inventory(dict)
    Return:
        None
    """
    
    sells = []
    while True:
        product_to_sell = input("Prodotto da vendere: ").lower()
        if product_to_sell not in inventory:
            print("Prodotto non trovato") # Skip this product because it is not in the inventory
        else:
            try:
                quantity_to_sell = int(input("Quantità da vendere: "))
                assert quantity_to_sell>0
                sells.append({"product":product_to_sell,"quantity":quantity_to_sell})                          
            except: 
                print("Quantità errata")            
        check = input("Aggiungere altro prodotto da vendere? (Si/No): ").lower()
        if check != "si":
            break

    profits = load_profits()
    sales_total = 0
    cost_total = 0
    
    for item in sells:
        name = item["product"]
        quantity = item["quantity"]
        available_quantity = inventory[name]["quantità"]
        if available_quantity < quantity:
            print(f"Errore, solo {available_quantity} X {name} disponibili")
        else:
            sales_return = inventory[name]["prezzo di vendita"] * quantity
            cost_price = inventory[name]["prezzo di acquisto"] * quantity
            sales_total += sales_return
            cost_total += cost_price
            inventory[name]["quantità"] -= quantity
            
    print("Vendita Registrata")
    for item in sells:
        name = item["product"]
        quantity = item["quantity"]
        print(f"- {quantity} X {name}: €{inventory[name]['prezzo di vendita']:.2f}")

    
    profits["lordo"] += sales_total
    profits["costi"] += cost_total
    print(f"Totale: €{sales_total:.2f}")
    save_inventory(inventory)
    save_profits(profits)


def load_profits(file_path="profits.json"):
    """
    This function loads the profits JSON file and initializes an empty profits dictionary if the file does not exist.
    Args:
        file_path(str): A string containing the profits file's path.
    Returns:
        profits (dict) : A dictionary where the keys are the "lordo" and "costi" values.
    """
    try:
        with open(file_path, "r") as json_file:
            profits = json.load(json_file)
    except FileNotFoundError:
        profits ={"lordo":0,"costi":0}
    return profits
    
def save_profits(profits,file_path="profits.json"):
    """
    This function saves the profits into a JSON file, by default called profits.json
    Args:
        profits (dict) : A dictionary where the keys are the "lordo" and "costi" values:
        - "lordo" (float): gross amount of sold products.       
        - "costi" (float): total costs of sold products.
        file_path(str): A string containing the profits file's path.
    Returns:
        None
    """
    with open (file_path,"w") as json_file:
        json.dump(profits,json_file,indent=6)
        
def total_profits(file_path="profits.json"):
    """
    This function prints the gross and the net revenue of sold products.
    Args:
        file_path(str): A string containing the profits file's path.
     Returns:
        None
    """
    profits = load_profits()
    gross = profits["lordo"]
    costs = profits ["costi"]
    net_revenue = gross - costs
    print(f"Profitto: lordo = {gross:.2f}€, netto = {net_revenue:.2f}€")
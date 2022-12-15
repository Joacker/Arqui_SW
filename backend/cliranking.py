from clients.Client import Client
from database.session import session
from database.models import Cotizacion
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Ranking")
    keep_alive = True
    try:
        while(keep_alive):
            print("Ingrese cuantos productos mas vendidos quiere ver")
            numero = input("Ingrese opcion: ")
            try:
                token = getpass("Token: ")
                climsg = {
                    "token": token,
                    "numero":  numero
                }
                a = Client("brrnk")
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)

    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
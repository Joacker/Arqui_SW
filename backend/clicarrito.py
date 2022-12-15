from clients.Client import Client
from database.session import session
from database.models import Cotizacion
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Carrito actual")
    keep_alive = True
    try:
        while(keep_alive):
            try:
                token = getpass("Token: ")
                climsg = {
                    "token": token
                }
                a = Client("brcar")
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)

    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
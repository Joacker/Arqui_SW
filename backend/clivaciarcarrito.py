from clients.Client import Client
from database.session import session
from database.models import Cotizacion
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Vaciar Carrito")
    keep_alive = True
    try:
        while(keep_alive):
            try:
                print("Está seguro que desea eliminar el carrito?")
                print("(1) Si")
                print("(2) No")
                opcion = input("Ingrese opcion: ")
                if (opcion=="1"):
                    token = getpass("Token: ")
                    climsg = {
                        "token": token
                    }
                    a = Client("brdel")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                    print("###################################\n\n", msg, "\n\n###################################")
                elif (opcion=="2"):
                    print("\nCerrando cliente, hasta pronto ....")
                    keep_alive = False
                    exit()
                else:
                    print ("Opción incorrecta")

                
            except Exception as e:
                print("Error: ", e)

    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
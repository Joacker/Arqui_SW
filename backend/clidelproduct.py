from clients.Client import Client
from database.session import session
from database.models import Cotizacion
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Eliminar Producto")
    keep_alive = True
    try:
        while(keep_alive):
            print("Ingrese el nombre del producto a eliminar de la cotizacion")
            nombre = input("Ingrese: ")
            print("¿Desea eliminar todos las unidades?")
            print("(1) Sí")
            print("(2) No")
            opcion = input("Ingrese opcion: ")
            if (opcion == "1"):
                try:
                    token = getpass("Token: ")
                    climsg = {
                        "token": token,
                        "nombre": nombre,
                        "cantidad": "total"
                    }
                    a = Client("bdelp")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                    print("###################################\n\n", msg, "\n\n###################################")
                except Exception as e:
                   print("Error: ", e)
                    
            if (opcion == "2"):
                try:
                    token = getpass("Token: ")
                    cantidad = int(input("Ingrese cantidad: "))
                    climsg = {
                        "token": token,
                        "nombre": nombre,
                        "cantidad": cantidad
                    }
                    a = Client("bdelp")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                    print("###################################\n\n", msg, "\n\n###################################")
                except Exception as e:
                   print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
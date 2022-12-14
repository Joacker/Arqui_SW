from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Registro")
    keep_alive = True
    try:
        while(keep_alive):
            print("¿Tiene alguna cotizacion actual para añadir productos?")
            print("(1) Sí")
            print("(2) No")
            opcion = input("Ingrese opcion: ")
            if (opcion == "1"):
                try:
                    token = getpass("Token: ")
                    nombre_producto = input("Ingrese nombre producto: ")
                    cantidad = int(input("Ingrese cantidad: "))
                    climsg = {
                        "token": token,
                        "nombre_producto": nombre_producto,
                        "cantidad": cantidad
                    }
                    a = Client("bregi")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                    print("###################################\n\n", msg, "\n\n###################################")
                except Exception as e:
                   print("Error: ", e)
                    
            if (opcion == "2"):
                try:
                    token = getpass("Token: ")
                    nombre_producto = input("Ingrese nombre producto: ")
                    cantidad = int(input("Ingrese cantidad: "))
                    climsg = {
                        "token": token,
                        "nombre_producto": nombre_producto,
                        "cantidad": cantidad
                    }
                    a = Client("bregi")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))                  
                    print("###################################\n\n", msg, "\n\n###################################")
                except Exception as e:
                   print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
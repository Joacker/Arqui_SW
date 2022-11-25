from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Login")
    keep_alive = True
    try:
        while(keep_alive):
            email = input("Ingrese email: ")
            password = getpass("Ingrese contraseña: ")
            try: 
                climsg = {
                    "email": email,
                    "password": password
                }
                a = Client("blogi")
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
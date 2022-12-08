from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Catalogo")
    keep_alive = True
    try:    
        a = Client("bgrup")
        msg = a.exec_client(debug=True, climsg="Hola")
        print("###################################")
        parse_msg = msg.split(",")
        for i in parse_msg:
            print(i)
        print("###################################")
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
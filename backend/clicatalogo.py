from clients.Client import Client
import json
        
if __name__ == "__main__":
    print("Service: Catalogo")
    keep_alive = True
    try:
        while (keep_alive):
            print("(1) Consultar catálogo")
            print("(2) Filtrar catálogo")
            print("(3) Salir")
            choice = input("Ingrese opcion: ")
            if(choice == "1"):
                try:
                    climsg = {
                        "choice": choice,
                        "ID": 0
                    }
                    a = Client("bgrup")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                    print("###################################")
                    parse_msg = msg.split(",")
                    for i in parse_msg:
                        print(i)
                    print("###################################")
                except Exception as e:
                    print("Error: ", e)
            elif(choice == "2"):
                try:
                   ID = input("Ingrese ID: ")
                   climsg = {
                        "choice": choice,
                        "ID": ID
                    }
                   a = Client("bgrup")
                   msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                   print("###################################")
                   parse_msg = msg.split(",")
                   for i in parse_msg:
                       print(i)
                   print("###################################")
                except Exception as e:
                    print("Error: ", e)
            elif(choice == "3"):
                keep_alive = False
                print("\nCerrando cliente, hasta pronto ....")
                exit()
        
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
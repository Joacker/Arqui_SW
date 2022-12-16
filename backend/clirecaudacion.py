from clients.Client import Client
import json
        
if __name__ == "__main__":
    print("Service: Informe sobre Recaudación")
    keep_alive = True
    try:
        while (keep_alive):
            print("(1) Informe sobre recaudación Histórico")
            print("(2) Informe sobre recaudación en un Rango de Fechas")
            print("(3) Informe sobre recaudación por Vendedor")
            #print("(4) Informe sobre pagos vía Transferencia")
            print("(4) Salir")

            choice = input("Ingrese opcion: ")
            if(choice == "1"):
                try:
                    climsg = {
                        "choice": choice
                    }
                    a = Client("breca")
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
                    fecha1 = input("Ingrese fecha de inicio (YYYY-MM-DD): ")
                    fecha2 = input("Ingrese fecha de fin (YYYY-MM-DD): ")
                    climsg = {
                        "choice": choice,
                        "fecha1": fecha1,
                        "fecha2": fecha2
                    }
                    a = Client("recau")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                    print("###################################")
                    
                    parse_msg = msg.split(",")
                    for i in parse_msg:
                        print(i)
                    
                    
                    print("###################################")
                except Exception as e:
                    print("Error: ", e)
            elif(choice == "3"):
                try:
                    rut = input("Ingrese rut del vendedor: ")
                    climsg = {
                        "choice": choice,
                        "rut": rut
                    }
                    a = Client("recau")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                    print("###################################")
                    print("Recaudaciones del vendedor: ", rut)
                    
                    parse_msg = msg.split(",")
                    for i in parse_msg:
                        print(i)
                    
                    
                    print("###################################")
                except Exception as e:
                    print("Error: ", e)

            elif(choice == "4"):
                keep_alive = False
                print("\nCerrando cliente, hasta pronto ....")
                exit()
        
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
from clients.Client import Client
import json
        
if __name__ == "__main__":
    print("Service: Editar y/o Agregar producto en bodega")
    keep_alive = True
    try:
        while (keep_alive):
            print("###################################")
            print("(1) Editar Producto")
            print("(2) Agregar Producto")
            print("(3) Salir")
            choice = input("Ingrese opcion: ")
            if(choice == "1"):
                try:
                    
                    ID = input("Ingrese ID: ")
                    print("###################################")
                    print("Ingrese variable que desea modificar")
                    print("(1) Stock")
                    print("(2) Valor Unidad")
                    choice2 = input("Ingrese opción: ")
                    print("###################################")
                    
                    if(choice2 == "1"):
                        try:
                            stock = input("Ingrese Stock nuevo: ")
                            climsg = {
                                "choice": choice,
                                "choice2": choice2,
                                "stock": stock,
                                "ID": ID
                            }
                            a = Client("bedit")
                            msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                            parse_msg = msg.split(",")
                            for i in parse_msg:
                                print(i)
                            print("###################################")
                            print("Stock modificado correctamente")
                        except Exception as e:
                            print("Error: ", e)
                    elif(choice2 == "2"):
                        try:
                            valor_unidad = input("Ingrese Valor Unidad nuevo: ")
                            climsg = {
                                "choice": choice,
                                "choice2": choice2,
                                "valor_unidad": valor_unidad,
                                "ID": ID
                            }
                            a = Client("aebdd")
                            msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                            parse_msg = msg.split(",")
                            for i in parse_msg:
                                print(i)
                            print("###################################")
                            print("Valor Unidad modificado correctamente")
                        except Exception as e:
                            print("Error: ", e)
                    a = Client("aebdd")
                except Exception as e:
                    print("Error: ", e)
            elif(choice == "2"):
                try:
                    print("###################################")
                    stock = int(input("Ingrese Stock: "))
                    nombre_producto = input("Ingrese Nombre de Producto: ")
                    valor_unidad = int(input("Ingrese Valor del Producto: "))
                    costo_unidad = int(input("Ingrese Costo por Unidad: "))
                    print("###################################")
                    climsg = {
                        "choice": choice,
                        "stock": stock,
                        "nombre_producto": nombre_producto,
                        "valor_unidad": valor_unidad,
                        "costo_unidad": costo_unidad
                    }
                    a = Client("aebdd")
                    msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                    parse_msg = msg.split(",")
                    for i in parse_msg:
                        print(i)
                    print("Producto agregado correctamente a la bodega")
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
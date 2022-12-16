from clients.Client import Client
from getpass import getpass
import json
        
if __name__ == "__main__":
    print("Service: Compra")
    keep_alive = True
    try:
        while(keep_alive):
            token = getpass("Token: ")
            rut = input("Rut cliente: ")
            print('Medios de pago:, {"1": "Efectivo",\n "2": "Debito", "3": \n "Credito"}')
            medio_pago = input("Medio de pago: ")
            
            try: 
                a = Client("bcomp")
                if medio_pago == "1":
                    medio_pagoi = "efectivo"
                    climsg = {
                    "token": token,
                    "rut": rut,
                    "medio_pago": medio_pagoi
                    }
                elif medio_pago == "2":
                    medio_pagoi = "debito"
                    climsg = {
                    "token": token,
                    "rut": rut,
                    "medio_pago": medio_pagoi
                    }
                elif medio_pago == "3":
                    medio_pagoi = "credito"
                    climsg = {
                    "token": token,
                    "rut": rut,
                    "medio_pago": medio_pagoi
                    }
                msg = a.exec_client(debug=True, climsg=json.dumps(climsg))
                print("###################################\n\n", msg, "\n\n###################################")
            except Exception as e:
                print("Error: ", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente, hasta pronto ....")
        keep_alive = False
        exit()
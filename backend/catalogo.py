from clients.Service import Service
from database.session import session
from database.models import Vendedor, Bodega
import json, sys, os, datetime
from time import sleep

class Catalogo(Service):
    def __init__(self):
        print("Servicio de catalogo de productos")
        super().__init__("bgrup")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            choice = climsg["choice"]
            if (choice == "1"): 
                catalogo = db.query(Bodega).filter(Bodega.stock > 0).all()
                print("Lista de productos:")
                list_products = ""
                index = 0
                for c in catalogo:
                    if (index == (len(catalogo)-1)):
                        list_products = list_products + "#ID: "+str(c.id)+" ;; Nombre: "+str(c.nombre_producto)+" ;; Precio: "+str(c.valor_unidad)+" ;; Stock: "+str(c.stock)
                    else:
                        list_products = list_products + "#ID: "+str(c.id)+" ;; Nombre: "+str(c.nombre_producto)+" ;; Precio: "+str(c.valor_unidad)+" ;; Stock: "+str(c.stock)+","
                    index = index + 1
                index = 0
                return list_products
            elif (choice == "2"):
                ID = climsg["ID"]
                catalogo = db.query(Bodega).filter(Bodega.stock > 0, Bodega.id == ID).all()
                print("Lista de productos:")
                list_products = ""
                index = 0
                for c in catalogo:
                    if (index == (len(catalogo)-1)):
                        list_products = list_products + "#ID: "+str(c.id)+" ;; Nombre: "+str(c.nombre_producto)+" ;; Precio: "+str(c.valor_unidad)+" ;; Stock: "+str(c.stock)
                    else:
                        list_products = list_products + "#ID: "+str(c.id)+" ;; Nombre: "+str(c.nombre_producto)+" ;; Precio: "+str(c.valor_unidad)+" ;; Stock: "+str(c.stock)+","
                    index = index + 1
                index = 0
                return list_products
            elif (choice == "3"):
                return "Cerrando catalogo de productos"
                
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return "Error: " + str(e) + " " + fname + " " + str(exc_tb.tb_lineno)


def main():
    try:
        Catalogo()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

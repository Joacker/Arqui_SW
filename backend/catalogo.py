from clients.Service import Service
from database.session import session
from database.models import Vendedor, Bodega
import json, sys, os, jwt, datetime
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
            #climsg = json.loads(climsg)
            catalogo = db.query(Bodega).filter(Bodega.stock > 0).all()
            print("Lista de productos:")
            for c in catalogo:
                print("#ID: "+str(c.id)+" Nombre: "+str(c.nombre_producto)+" Precio: "+str(c.valor_unidad)+" Stock: "+str(c.stock))
            return "Visualizacion de catalogo de productos"
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

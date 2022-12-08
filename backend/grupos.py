from clients.Service import Service
from database.session import session
from database.models import Vendedor, Bodega
import json, sys, os, jwt, datetime
from time import sleep

class Catalogo(Service):
    def __init__(self):
        print("Servicio de grupos de usuarios")
        super().__init__("bgrup")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            catalogo = db.query(Bodega).all()
                
            return "Grupo creado con id: " + catalogo
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

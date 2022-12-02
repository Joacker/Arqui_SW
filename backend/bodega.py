from clients.Service import Service
from database.session import session
from database.models import Bodega, Boleta, Producto, Cotizacion, Vendedor, Medio_Pago, to_dict
import json, sys, os, jwt, datetime
from time import sleep

class Bodegas(Service):
    def __init__(self):
        print("Servicio de bodega")
        super().__init__("bbodega")
        self.start_service(debug=True)
    
    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            
        except Exception as e:
            return "Error: "+str(e)
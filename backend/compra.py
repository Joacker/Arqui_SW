from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Bodega, Producto, Medio_Pago, to_dict
import json, sys, os, jwt, datetime
from time import sleep

class Compra(Service):
    def __init__(self):
        print("Servicio para concretar compra")
        super().__init__("buser")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        try:
            climsg = json.loads(climsg)
            token = climsg["token"]
            decoded = jwt.decode(
                token, os.environ['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.query(Vendedor).filter_by(id=decoded['id']).first()
            valid_cotizacion = db.query(Cotizacion).join(Boleta).filter(current_user.id == Boleta.vendedor_id2).first()
            if current_user is None:
                return "Vendedor no encontrado"
            if(valid_cotizacion is None):
                '''No hay cotizaciones creadas'''
                return "No hay cotizaciones creadas, favor crear una"
            elif(valid_cotizacion is not None):
                rut_i = climsg["rut"]
                medio_pago_i = climsg["medio_pago"]
                fecha_i = datetime.datetime.now()
                print(rut_i, medio_pago_i, fecha_i)
                find_product_to_update =  db.query(Bodega, Producto).join(Producto).filter(Producto.cotizacion_id == valid_cotizacion.id).all()
                suma = 0
                for bodega, producto in find_product_to_update:
                    #print(producto.bodega_id, producto.cantidad, bodega.nombre_producto, bodega.valor_unidad)
                    suma = suma + (producto.cantidad * bodega.valor_unidad)
                valid_boleta = db.query(Boleta).join(Cotizacion).filter(current_user.id == Boleta.vendedor_id2).first()
                valid_boleta.rut = rut_i
                valid_boleta.mediopago = medio_pago_i
                valid_boleta.fecha = fecha_i
                valid_boleta.monto = suma
                if (medio_pago_i == "efectivo"):
                    medio_pago_concludes_efectivo = Medio_Pago(efectivo = suma, boleta_id2 = valid_boleta.id)
                    db.add(medio_pago_concludes_efectivo)
                    db.commit()
                if (medio_pago_i == "debito"):
                    medio_pago_concludes_debito = Medio_Pago(debito = suma, boleta_id2 = valid_boleta.id)
                    db.add(medio_pago_concludes_debito)
                    db.commit()
                if (medio_pago_i == "credito"):
                    medio_pago_concludes_credito = Medio_Pago(credito = suma, boleta_id2 = valid_boleta.id)
                    db.add(medio_pago_concludes_credito)
                    db.commit()
                
                return "Compra realizada con exito"
                
        except Exception as e:
            print(e)
            return "Error: " 

def main():
    try:
        Compra()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()


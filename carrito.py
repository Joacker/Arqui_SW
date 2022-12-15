from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Producto
import bcrypt, json, os, jwt, datetime
from time import sleep

class Add_product(Service):
    def __init__(self):
        print("Servicio de Carrito")
        super().__init__("brcar")
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
            if current_user is None:
                return "Usuario no encontrado"

            carrito = db.execute("SELECT producto.bodega_id,bodega.nombre_producto,producto.cantidad FROM producto,bodega,cotizacion WHERE cotizacion.concludes=0 AND producto.cotizacion_id=cotizacion.id AND bodega.id=producto.bodega_id ORDER BY producto.cantidad DESC").fetchall()

            if carrito:
                list_products = ""
                index = 0
                for r in carrito:
                    if (index == (len(carrito)-1)):
                        list_products = list_products + "#ID: "+str(r.bodega_id)+" ;; Nombre: "+str(r.nombre_producto)+" ;; Cantidad en carrito: "+str(r.cantidad)
                    else:
                        list_products = list_products + "#ID: "+str(r.bodega_id)+" ;; Nombre: "+str(r.nombre_producto)+" ;; Cantidad en carrito: "+str(r.cantidad)+","
                    index = index + 1
                return list_products
            else:
                return "No hay cotización creada y/o no hay productos en cotizacion"
            

            
            
        except Exception as e:
            db.close()
            return str(e)
        
        
def main():
    try:
        Add_product()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

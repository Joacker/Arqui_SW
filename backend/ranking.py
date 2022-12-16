from clients.Service import Service
from database.session import session
from database.models import Bodega, Producto, Vendedor
import bcrypt, json, os, jwt, datetime
from time import sleep

class Add_product(Service):
    def __init__(self):
        print("Servicio de Ranking")
        super().__init__("brrgk")
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
            lineas = db.execute("SELECT COUNT (*) as cant from bodega WHERE nombre_producto NOT LIKE ''").fetchall()
            prods=lineas[0].cant
            numero = climsg["numero"]
            if(int(numero)>int(prods)):
                print("El sistema solo cuenta con: "+str(prods)+" productos")
                tops = db.execute("SELECT producto.bodega_id, bodega.nombre_producto, SUM(producto.cantidad) as suma FROM producto,bodega WHERE bodega.id=producto.bodega_id GROUP BY producto.bodega_id, bodega.nombre_producto ORDER BY suma desc LIMIT "+str(prods)).fetchall()
                list_products = ""
                index = 0
                for r in tops:
                    if (index == (prods-1)):
                        list_products = list_products + "#ID: "+str(r.bodega_id)+" ;; Nombre: "+str(r.nombre_producto)+" ;; Cantidad vendida: "+str(r.suma)
                    else:
                        list_products = list_products + "#ID: "+str(r.bodega_id)+" ;; Nombre: "+str(r.nombre_producto)+" ;; Cantidad vendida: "+str(r.suma)+","
                    index = index + 1
                return list_products
            else:
                tops = db.execute("SELECT producto.bodega_id, bodega.nombre_producto, SUM(producto.cantidad) as suma FROM producto,bodega WHERE bodega.id=producto.bodega_id GROUP BY producto.bodega_id, bodega.nombre_producto ORDER BY suma desc LIMIT "+str(numero)).fetchall()
                list_products = ""
                index = 0
                for r in tops:
                    if (index == (int(numero)-1)):
                        list_products = list_products + "#ID: "+str(r.bodega_id)+" ;; Nombre: "+str(r.nombre_producto)+" ;; Cantidad vendida: "+str(r.suma)
                    else:
                        list_products = list_products + "#ID: "+str(r.bodega_id)+" ;; Nombre: "+str(r.nombre_producto)+" ;; Cantidad vendida: "+str(r.suma)+","
                    index = index + 1
                return list_products


            
            
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

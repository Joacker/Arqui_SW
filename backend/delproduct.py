from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Producto
import bcrypt, json, os, jwt, datetime
from time import sleep

class Add_product(Service):
    def __init__(self):
        print("Servicio de Eliminar Productos")
        super().__init__("bdelp")
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

            buscar=current_user.id
            numero=int(0)
            #existmodi = db.query(Cotizacion).filter(vendedor_id==buscar, concludes==numero).all()
            existmodi = db.execute("SELECT * FROM cotizacion WHERE vendedor_id = "+str(buscar)+" AND concludes="+str(numero)).fetchall()
            if(existmodi is None):
                '''No existe cotizacion'''
                return "No existe cotizacion, por favor primero crea una en servicio de agregar producto"
            else:
                #casos
                cantidad = climsg["cantidad"]
                nombre = climsg["nombre"]
                coti=existmodi[0].id
                exists= db.execute("SELECT * FROM producto,bodega WHERE bodega.nombre_producto='"+str(nombre)+"' AND cotizacion_id="+str(coti)+" AND producto.bodega_id=bodega.id").fetchall()
                if (exists is None):
                    return "Producto no existente en carrito"
                else:
                    if(str(cantidad)=="total"):
                        idprod=exists[0].bodega_id
                        eliminar=db.execute("DELETE FROM producto WHERE bodega_id='"+str(idprod)+"' AND cotizacion_id="+str(coti))
                        if eliminar:
                            db.commit()
                            return "Eliminado del carrito"
                        else:
                            return "F manito"
                    else:
                        idprod=exists[0].bodega_id
                        cantdb=exists[0].cantidad
                        print("hay algo raro")
                        if((cantdb-cantidad)<=0):
                            print("Numero ingresado invalido, reintente")
                        else:
                            print("cantidad: "+str(cantidad))
                            cantdb=cantdb-cantidad
                            afectada=db.execute("UPDATE producto SET cantidad='"+str(cantdb)+"' WHERE bodega_id='"+str(idprod)+"' AND cotizacion_id="+str(coti))
                            if afectada:
                                db.commit()
                                print("Carrito actualizado")
                            else:
                                print("Error")
                        print("no todos")
                            
                    print("fallo")
                return "Con cotizacion"

            
            
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

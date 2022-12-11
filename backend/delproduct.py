from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Producto
import bcrypt, json, os, jwt, datetime
from time import sleep

class Add_product(Service):
    def __init__(self):
        print("Servicio de Eliminar Productos")
        super().__init__("brgdp")
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
            existmodi = db.query(Cotizacion).join(Boleta).filter(current_user.id == Boleta.vendedor_id2).first()
            if(existmodi is None):
                '''No existe cotizacion'''
                return "No existe cotizacion, por favor primero crea una en servicio de agregar producto"
            else:
                idprod = climsg["idprod"]
                buscar_prod = db.query(Producto).filter(Producto.vendedor_id=current_user.id, Producto.bodega_id=idprod).first()
                if(buscar_prod is None):
                    return "Producto no existente en carrito"
                else:
                    cantidad = climsg["cantidad"]
                    if((buscar_prod.cantidad-cantidad)<0):
                        return "Numero ingresado invalido, reintente"
                    else:
                        buscar_prod.cantidad=buscar_prod.cantidad-cantidad
                        db.session.commit()
                        return "Carrito actualizado"

            
            
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

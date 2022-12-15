from clients.Service import Service
from database.session import session
from database.models import Cotizacion, Vendedor, Boleta, Producto
import bcrypt, json, os, jwt, datetime
from time import sleep

class Add_product(Service):
    def __init__(self):
        print("Servicio para Vaciar Carrito")
        super().__init__("brdel")
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
            search = db.execute("SELECT * FROM cotizacion WHERE concludes=0 AND vendedor_id="+str(buscar)).fetchall()
            if search:
                coti=search[0].id
                lists = db.execute("SELECT * FROM producto WHERE cotizacion_id="+str(coti)).fetchall()
                if lists:
                    productos = db.execute("DELETE FROM producto WHERE cotizacion_id="+str(coti))
                    if productos:
                        db.commit()
                        return "Productos eliminados"
                    else:
                        return "Error"
                else:
                    return "No hay productos en la cotización"
                
            else:
                return "No existe cotización abierta"



            

            
            
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

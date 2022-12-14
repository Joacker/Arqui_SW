from clients.Service import Service
from database.session import session
from database.models import Vendedor
import bcrypt, os, json, jwt, datetime
from time import sleep

class Login(Service):
    def __init__(self):
        print("Servicio de login de vendedores")
        super().__init__("bloci")
        self.start_service(debug=True)

    def service_function(self, climsg):
        '''Funcion temporal, sera reemplazada en los distintos servicios'''
        db = session()
        
        try:
            climsg = json.loads(climsg)
            rut = climsg["rut"]
            password = climsg["password"]
            vendedor = db.query(Vendedor).filter(Vendedor.rut == rut).first()
            if bcrypt.checkpw(password.encode('utf-8'), vendedor.password.encode('utf-8')):
                token = jwt.encode({
                    'id': vendedor.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                    os.environ['SECRET_KEY'])
                return token
            else:
                db.close()
                return "Contraseña incorrecta"
        except Exception as e:
            db.close()
            return str(e)

def main():
    try:
        Login()
    except Exception as e:
        print(e)
        sleep(30)
        main()

if __name__ == "__main__":
    main()

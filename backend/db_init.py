from database.models import Base
from sqlalchemy import create_engine
from database.config import Config
from database.models import Base, Bodega, Vendedor, Producto, Cotizacion, Boleta, Medio_Pago, to_dict
from database.session import session
import csv

def init_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    
    return True

def load_data():
    db = session()
    try:
        with open("./database/load.csv", "r") as file:
            csvreader = csv.reader(file, delimiter=";")
            cont = 0
            for row in csvreader:
                if cont == 0:
                    print("HEADER")
                else:
                    print(row)       
                    bodega = Bodega(stock=100, nombre_producto="Coca Cola", valor_unidad=1000, costo_unidad=500)
                    db.add(bodega)
                    db.commit()
                    print("AGREGADO EN BODEGA")
                cont = cont + 1
        vendedor = Vendedor(rut="12345678-9", nombre="Juan", apellido="Perez")
        db.add(vendedor)
        db.commit()
        db.close()
        return True
    
    except Exception as e:
        print("Error: "+str(e))
        return False

init_db()
load_data()


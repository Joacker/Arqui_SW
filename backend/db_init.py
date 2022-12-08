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
                    stocki = 0; nombre_productoi = ""; valor_unidadi = 0 ;costo_unidadi = 0
                    for i in range(len(row)):
                        if i == 1:
                            stocki = row[i]
                        if i == 2:
                            nombre_productoi = row[i]
                        if i == 3:
                            valor_unidadi = row[i]
                        if i == 4:
                            costo_unidadi = row[i]   
                    bodega = Bodega(stock=stocki, nombre_producto=nombre_productoi, valor_unidad=valor_unidadi, costo_unidad=costo_unidadi)
                    print(stocki)
                    db.add(bodega)
                    db.commit()
                    print("AGREGADO EN BODEGA")
                cont = cont + 1
        with open("./database/vendedores.csv", "r") as file2:
            csvreader2 = csv.reader(file2, delimiter=";")
            cont = 0
            for row in csvreader2:
                if cont == 0:
                    print("HEADER")
                else:
                    rutv = ""; nombrev = ""; apellidov = ""; passwordv = ""
                    for i in range(len(row)):
                        if i == 1:
                            rutv = row[i]
                        if i == 2:
                            passwordv = row[i]
                        if i == 3:
                            nombrev = row[i]
                        if i == 4:
                            apellidov = row[i]
                    print(rutv, nombrev, apellidov)
                    vendedor = Vendedor(rut=rutv,password=passwordv, nombre=nombrev, apellido=apellidov)
                    print(rutv)
                    db.add(vendedor)
                    db.commit()
                    print("AGREGADO EN VENDEDOR")
                cont = cont + 1
        db.close()
        return True
    
    except Exception as e:
        print("Error: "+str(e))
        return False

init_db()
load_data()


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from clientedefault import client  
from trazos import trace  
from paquetedefault import packages  
from uuid import uuid4 as uuid  

app = FastAPI()

facturas = []  


# modelo del cliente
class Cliente(BaseModel):
    id: int
    nombre: str
    apellido: str
    direccion: str
    cedula:int


class Paquetes(BaseModel):
    id: int
    nombre: str
    precio: float
    trayectoria: int


class Factura(BaseModel):
    id: str
    total: float
    fecha: datetime = datetime.now()
    cliente: dict
    items: list


@app.get('/')
def read_root():
    return {"Bienvenid@s a Farcel!,¿Qué harás el día de hoy?"}


@app.get('/cliente')
def get_cliente():
    return client  


@app.get('/cliente/{client_id}')
def get_clienteID(client_id: int):
    for cli in client:  
        if cli["id"] == client_id:
            return cli  
    raise HTTPException(status_code=404, detail="Client Not Found")


@app.post('/cliente')  
def save_cliente(Cliente: Cliente):
    for cli in client:
        if Cliente.id == cli["id"]:  
            return "Not recieved"
    client.append(
        Cliente.dict())  
    raise HTTPException(status_code=200, detail="recieved")


@app.put('/cliente/{client_id}')  
def update_cliente(client_id: int, updatedcliente: Cliente):  #
    for index, cli in enumerate(client):
        if cli["id"] == client_id:  
            client[index]["nombre"] = updatedcliente.nombre
            client[index]["apellido"] = updatedcliente.apellido
            client[index]["direcccion"] = updatedcliente.direccion
            client[index]["cedula"] = updatedcliente.cedula
            return {"message": "client updated succesfully"}
    raise HTTPException(status_code=404, detail="Not Found")



@app.delete('/cliente/{client_id}')
def delete_cliente(client_id: int):
    for index, cli in enumerate(client):
        if cli["id"] == client_id:
            client.pop(index)
            raise HTTPException(status_code=200,
                                detail="client has been deleted")
    raise HTTPException(status_code=404, detail="Client Not Found")


@app.get('/paquetes')  
def get_paquetes():
    return packages


@app.post('/paquetes')  
def save_paquetes(paquete: Paquetes):
    for pack in packages:  
        if pack["id"] == paquete.id:
            return "not recived"
    packages.append(paquete.dict())  
    raise HTTPException(status_code=200, detail="paquete has been recieved")


@app.get('/paquetes/{pack_id}')
def get_paqueteID(pack_id: int):
    for pack in packages:
        if pack["id"] == pack_id:
            return pack
    raise HTTPException(status_code=404, detail="Paquete Not Found")


@app.put('/paquete/{paquete_id}')
def update_paquete(paquete_id: int, updatedpaquete: Paquetes):
    for index, pack in enumerate(packages):
        if pack["id"] == paquete_id:
            packages[index]["nombre"] = updatedpaquete.nombre
            packages[index]["precio"] = updatedpaquete.precio
            return {"message": "package updated succesfully"}
    raise HTTPException(status_code=404, detail="Not Found")


@app.delete('/Paquetes/{pack_id}')
def delete_paquetes(pack_id: int):
    for index, pack in enumerate(packages):
        if pack["id"] == pack_id:
            packages.pop(index)
            return {"message": "Factura has been deleted"}
    raise HTTPException(status_code=404, detail="Paquete Not Found")


@app.get('/facturas')
def get_facturas():
    return facturas



@app.post('/facturas')
def save_facturas(client_id: int, pack_id: int, NewFactura: Factura):
    NewFactura.id = str(uuid())
    for cli in client:
        if client_id == cli["id"]:
            print(str(cli))
            NewFactura.cliente = cli
        else:
            raise HTTPException(status_code=404, detail="client Not Found")
    for pack in packages:
        if pack_id == pack["id"]:
            for trac in trace:
                print(trac["id"])
                print(pack["trayectoria"])
                if pack["trayectoria"] == trac["id"]:
                    total = trac["costo"] + pack["precio"]
                    NewFactura.total = total
                    break
                else:
                    raise HTTPException(status_code=404,
                                        detail="Trace Not Found")
            NewFactura.items = pack
            break
        else:
            raise HTTPException(status_code=404, detail="packete Not Found")
    facturas.append(NewFactura.dict())
    return {"message": "facture added succesfully"}


@app.get('/factura/{factura_id}')
def get_facturaID(factura_id: str):
    for fact in facturas:
        if fact["id"] == factura_id:
            return fact
    raise HTTPException(status_code=404, detail="factura Not Found")


@app.delete('/factura/{factura_id}')
def delete_factura(factura_id: str):
    for index, fact in enumerate(facturas):
        if fact["id"] == factura_id:
            facturas.pop(index)
            return {"message": "Factura has been deleted"}
    raise HTTPException(status_code=404, detail="factura Not Found")

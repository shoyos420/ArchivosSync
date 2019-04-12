#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import hashlib
import os
CHUNK_SIZE =  1024 * 1024
DICT = {
    "a1e433a8d8bdc48624e097e8327b0483b8de9281" : "prueba2.mp4"

}




#objetohash = hashlib.sha1(b'hola mundo')
#cadena = objetohash.hexdigest()
#print(cadena)


def descarga(nombreArchivo):
	pass


def subida(FILE,data):
    
    with open(FILE, "a") as f:        
        #f.seek(CHUNK_SIZE)
        f.write(data)
    #print leerArchivo(FILE)
    socket.send(leerArchivo(FILE))

def sha1Hash(data):
    objetohash = hashlib.sha1(data)
    cadena = objetohash.hexdigest()
    ##print(cadena)
    return cadena 
	
def leerArchivo(FILE):
    with open(FILE, 'rb') as f:
         data = f.read()
    
    return sha1Hash(data) 

def envioParte(FILE, data, clave, contador):
    socket.send_multipart([FILE.encode(),data, clave,bin(contador)])## enviar multiparte : (nombreArchivo, datosArchivo, hashArchivo, parteArchivo)
     

def particionarArchivo(FILE,clave,posicion):
   
    
    with open(FILE, 'rb') as f:
        data = f.seek(CHUNK_SIZE*posicion) 
        data = f.read(CHUNK_SIZE)
        print int(posicion)
	envioParte(FILE,data,clave,posicion)
         

def encontrarHash(sha1):
    return DICT[sha1]

def escribirDict(nombre, sha1):
    global DICT
    DICT [sha1] = nombre

def leerArchivo(FILE):
    with open(FILE, 'rb') as f:
         data = f.read()
    
    return sha1Hash(data) 


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

##print 
#print leerArchivo("prueba3.mp4")
while True:
   
    
    
    message = socket.recv_multipart()
    print(message[0].decode())
    if (message[0].decode() == "subida"):
        subida(message[1].decode(),message[2])
	escribirDict(message[1].decode(), leerArchivo(message[1].decode()))
	print DICT	
	
    elif (message[0].decode() == "bajada"):
        #descarga()
	##print int(message[2], 2)
	print  encontrarHash(message[1])       
	particionarArchivo(encontrarHash(message[1]),message[1],int(message[2], 2))
    
    

     #  Do some 'work'
    
     #  Send reply back to client
     



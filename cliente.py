#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import hashlib
import sys
CHUNK_SIZE =  1024 *1024
newSha1= ""



def sha1Hash(data):
    objetohash = hashlib.sha1(data)
    cadena = objetohash.hexdigest()
    #print(cadena)
    return cadena




def envioParte(nombre,data, clave, contador):
    global newSha1
    print "enviando parte " + str(contador + 1)
    socket.send_multipart([b"subida",nombre.encode(),data, clave,bin(contador)])## enviar multiparte : (accion,nombreArchivo, datosArchivo, hashArchivo, parteArchivo)
    message = socket.recv()
    newSha1= message


def recibirParte(clave, contador):
   
    socket.send_multipart([b"bajada",clave,bin(contador)])## enviar multiparte : (accion,hashArchivo, parteArchivo)
    
    nombreArchivo, datosArchivo, hashArchivo, parteArchivo = socket.recv_multipart()
    print "recibiendo parte " + str(contador + 1)
    while(datosArchivo):
	
        with open(nombreArchivo, "a") as f:
	    #f.seek(CHUNK_SIZE)
	    f.write(datosArchivo)
        print int(parteArchivo, 2)
	socket.send_multipart([b"bajada",clave, bin (int(parteArchivo, 2)+1) ])## enviar multiparte : (accion,hashArchivo, parteArchivo)
        nombreArchivo, datosArchivo, hashArchivo, parteArchivo = socket.recv_multipart()

    if (hashArchivo == clave):
        print "comprobacion exitosa sha1"



def particionarArchivo(nombre,clave):
    i=0
    
    with open(nombre, 'rb') as f:
         data = f.read(CHUNK_SIZE)
         while data:
            aux= envioParte(nombre,data,clave,i)
	    i+=1
            data = f.read(CHUNK_SIZE)
   


def leerArchivo(arg):
    
    with open(arg, 'rb') as f:
         data = f.read()
    
    return sha1Hash(data)    

def upload(op,arg):
    clave = leerArchivo(arg)
    particionarArchivo(arg, clave)   
          
def download(op,arg):
   
    recibirParte(arg,0)


def main(op,arg):
    if(op=="upload"):
        upload(op,arg)
	print "Comparte esta clave Sha1 para Download: " + newSha1
    elif(op=="download"):
         download(op,arg)

def instrucciones():
    print "ERROR: error en los argumentos"
    print "argumentos validos [1] : Upload, Download"
    print "argumentos validos [2] : nombreArchivo.extension , sha1 code"


if (len(sys.argv)==3) :
    ###__________________________/ SOCKET CONETTION INIT \____________________________________###
    context = zmq.Context()
    print("conectando a server de archivos...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    main(sys.argv[1],sys.argv[2])



else : 
    instrucciones()



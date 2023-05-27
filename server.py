import socket
from _thread import *
import pickle
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
server = "localhost"
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def EncryptKey(key, public_keyStr):
    public_key=RSA.import_key(public_keyStr)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher.encrypt(key)
    return encrypted_key
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen()
print("Waiting for a connection, Server Started")
def threaded_client(conn):
    while True:
        try:
            conn.send(pickle.dumps('1'))
            ServerDBFile = 'ServerDataBase.txt'
            data = pickle.loads(conn.recv(2048))
            print('Data Received')
            print(data)
            if not data:
                print("Disconnected")
                break
            else:
                info = data.split('|', 6)
                if info[0] == '1':
                    key=get_random_bytes(16)
                    with open(ServerDBFile,"r") as file:
                        s=file.read()
                        count= s.split(",")
                        for i in range(len(count)):
                            if count[i] == info[1]:
                                SenderPublicKey= count[i+1]
                    with open(ServerDBFile,"r") as file:
                        s=file.read()
                        count= s.split(",")
                        for i in range(len(count)):
                            if count[i] == info[2]:
                                ReceiverPublicKey= count[i+1]


                    SenderEncKeyreply = EncryptKey(key,SenderPublicKey)
                    ReceiverEncKeyreply1 = EncryptKey(key,ReceiverPublicKey)

                else:
                  print('not an encryption request')
                print(SenderEncKeyreply)
                print(ReceiverEncKeyreply1)
                conn.send(pickle.dumps(SenderEncKeyreply))
                conn.send(pickle.dumps(ReceiverEncKeyreply1))
        except:
            break
    conn.close()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))
import socket
import pickle
from aes import *
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def DecryptKey(encrypted_key, private_keyStr):
    private_key = RSA.import_key(private_keyStr)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_key = cipher.decrypt(encrypted_key)
    return decrypted_key

class senderNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 9090
        self.addr = (self.server, self.port)
        self.port = self.connect()

    def connect(self):
        try:
            print('connect')
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass


    def send(self, data):
         try:
             with open("SenderPrivateKey.txt", "r") as file:
                 SenderPrivateStr = file.read()
             Msg = data.split('|', 6)
             self.client.send(pickle.dumps(str(data)))
             SenderEncryptedkey = pickle.loads(self.client.recv(2048))
             RecieverEncryptedkey = pickle.loads(self.client.recv(2048))
             print(f"Received from server  Senderkey: {SenderEncryptedkey}")
             print(f"Received from server  Reciverkey: {RecieverEncryptedkey}")
             key = DecryptKey(SenderEncryptedkey, SenderPrivateStr)
             msgOrgBodyFile = open('msgOrgSubject.txt', 'w')
             msgOrgBodyFile.write(Msg[3])
             msgOrgBodyFile.close()
             msgOrgBodyFile = open('msgOrgBody.txt', 'w')
             msgOrgBodyFile.write(Msg[4])
             msgOrgBodyFile.close()
             encrypt_file(key, 'msgOrgSubject.txt', 'msgEncryptedSubejct.txt')
             encrypt_file(key, 'msgOrgBody.txt', 'msgEncryptedBody.txt')
             with open('msgEncryptedSubejct.txt', 'rb') as file:
                 subject = file.read()
             with open('msgEncryptedBody.txt', 'rb') as file:
                 body = file.read()
             return subject, body, RecieverEncryptedkey,
         except socket.error as e:
             print("error")
             print(e)
import socket
import numpy as np
import pickle
import os
from enum import Enum
from cryptography.fernet import Fernet

class publicKey: #TODO: accept random values for encryption
    def __init__(self, p = 53, q = 59, e = 3):
        self.p = p
        self.q = q
        self.n = p*q
        self.e = e

class privateKey: #TODO: accept random values for encryption
    def __init__(self, k = 2):
        self.phi = 0
        self.k = k
        self.d = 0
        self.n = 0
    def genPrivKey(self,p,q,e):
        self.phi = (p - 1) * (q -1)
        self.d = ((self.k * self.phi) + 1) / e
        self.n = p*q

class BellLaPedula:
    def __init__(self, level, ID):
        self.__level = level
        self.__ID = ID
    
    def setLevel(self, level):
        self.__level = level
    
    def getLevel(self):
        return self.__level
    
    def getID(self):
        return self.__ID
    
    def RequestRead(self, msg, cipher_suite):
        print "Checking read access level for user with ID #", self.__ID,"..."
        print "Found access level: ", self.__level,"..."
        if self.__level >= msg.getLevel():
            print "Access approved. Decrypting message..."
            #temp = msg.getMessage()
            #temp = temp.decode('rot13')
            print "Request for read completed: ",cipher_suite.decrypt(msg.getMessage()).decode('rot13')
        
        else:
            print "You should not be trying to look at this message! Your attempted breach has been logged and reported!"

    def RequestWrite(self, msg, newMsg, cipher_suite):
        print "Checking write access level for user with ID #", self.__ID,"..."
        if self.__level == msg.getLevel():
            print "Access approved. Writing and encrypting new message..."
            print "New message is: ", newMsg
            newMsg = newMsg.encode('rot13')
            msg.setMessage(cipher_suite.encrypt(newMsg))
            print "Encrypted to: ", msg.getMessage()
        
        else:
            print "You should not be trying to write to this message! Your attempted breach has been logged and reported!"

class messageAccess:
    def __init__(self, level, msg):
        self.__level = level
        self.__message = msg
    
    def setMessage(self,msg):
        self.__message = msg
    
    def getMessage(self):
        return self.__message
    
    def setLevel(self, level):
        self.__level = level
    
    def getLevel(self):
        return self.__level


def decrypt(key, msg):
    return int(((msg ** key.d)% key.n))

def swap(msg, i, j):
    c = list(msg)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)

def secretKeyEncryption(message):
    key = os.urandom(32)
    iv = os.urandom(16)
    obj = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = obj.encrypt(message)
    print(ciphertext)

pubKey = publicKey()
privKey = privateKey()
privKey.genPrivKey(pubKey.p, pubKey.q, pubKey.e)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 47777))
s.listen(1)
conn, addr = s.accept()

while 1:
    data = conn.recv(4096) #Message from client for the public key
    if not data:
        break
    
    print(data)
    #Send public key info off to client
    conn.sendall(str(pubKey.n))
    conn.sendall(str(pubKey.e))

    data2 = conn.recv(4096) #Encrypted data

    encryptedmsg = pickle.loads(data2) #Convert garbage data into numpy array
    encryptedmsg = encryptedmsg.tolist()

    print "Recieved message: ", encryptedmsg
    raw_input("Press Enter to continue...")

    decryptedmsg=""
    for i in encryptedmsg:
        decryptedmsg += chr(decrypt(privKey, i))

    print "Decrypted message: ",decryptedmsg
    raw_input("Press Enter to continue...")

    msg = messageAccess(5, decryptedmsg)

    decryptedmsg = None
    del decryptedmsg

    print "Obfuscating data..."
    msg.setMessage(msg.getMessage().encode('rot13'))
    print "Obfuscated data: ", msg.getMessage()
    raw_input("Press Enter to continue...")

    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    print "Encrypting obfuscated message..."
    msg.setMessage(cipher_suite.encrypt(msg.getMessage()))
    print "Encryped message to : ", msg.getMessage()
    raw_input("Press Enter to continue...")

    print "Defining 6 users with 6 different access levels..."
    UserList = []
    UserList.append(BellLaPedula(0,123))
    UserList.append(BellLaPedula(1,234))
    UserList.append(BellLaPedula(2,456))
    UserList.append(BellLaPedula(3,789))
    UserList.append(BellLaPedula(4,567))
    UserList.append(BellLaPedula(5,987))

    print "Attempting reads with each user..."

    for i in range(0,len(UserList)):
        UserList[i].RequestRead(msg, cipher_suite)
        raw_input("Press Enter to continue...")

    print "Attempting writes with each user..."
    for i in range (0,len(UserList)):
        UserList[i].RequestWrite(msg, "I have changed the message", cipher_suite)
        raw_input("Press Enter to continue...")

conn.close()

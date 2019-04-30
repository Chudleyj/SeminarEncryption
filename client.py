import socket
import sys
import pickle
import numpy as np

class publicKey:
    def __init__(self, n, e):
        self.n = n
        self.e = e

def encrypt(key, msg):
    return((msg ** key.e) % key.n)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 47777))
s.sendall('Connected to client... Passing public key')

data = s.recv(1024) #Get first part of public key (n)
n = int(data)

data = s.recv(1024) #Get second part of public key (e)
e = int(data)

pubKey = publicKey(n,e)

#TODO: define method for converting chars to numbers
#So characters may also be encrypted
#E.G 'H' = 8, 'I' = 9 --> 'HI' = 89

message = raw_input('Enter message to encrypt: ')
msgarr = np.array([ord(i) for i in message])

encryptedmsg = encrypt(pubKey, msgarr)

print "Encryped message to: ", ' '.join(map(str, encryptedmsg))
print "Sending encrypted message to server from client..."
raw_input("Press Enter to continue...")
#We used the public key to encrypt our message...now send it back to server
s.send(pickle.dumps(encryptedmsg))


s.close()
data = 0 #Don't ask my why but the program hangs if you dont clear this var
#OR print out repr(data)



import socket
import sys

class publicKey:
    def __init__(self, n, e):
        self.n = n
        self.e = e

def encrypt(key, msg):
    return((msg ** key.e) % key.n)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 37000))
s.sendall('Connected to client... Passing public key')

data = s.recv(1024) #Get first part of public key (n)
n = int(data)

data = s.recv(1024) #Get second part of public key (e)
e = int(data)

pubKey = publicKey(n,e)

#TODO: define method for converting chars to numbers
#So characters may also be encrypted
#E.G 'H' = 8, 'I' = 9 --> 'HI' = 89

print ("Encrypting message '89'")
encryped = encrypt(pubKey,89)
print("Encryped message to: ", encryped)

#We used the public key to encrypt our message...now send it back to server
s.sendall(str(encryped))


s.close()
data = 0 #Don't ask my why but the program hangs if you dont clear this var
#OR print out repr(data)



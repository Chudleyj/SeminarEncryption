import socket

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

def decrypt(key, msg):
    return int(((msg ** key.d)% key.n))



pubKey = publicKey()
privKey = privateKey()
privKey.genPrivKey(pubKey.p, pubKey.q, pubKey.e)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 37000))
s.listen(1)
conn, addr = s.accept()

while 1:
    data = conn.recv(1024)
    if not data:
        break
    
    print(data)

    #Send public key info off to client
    conn.sendall(str(pubKey.n))
    conn.sendall(str(pubKey.e))

    data = conn.recv(1024) #Recieve Encryped message
    print('Recieved encrypted message: ', data)

    decrypted = decrypt(privKey, int(data))
    print("Decrypted message: ", decrypted)



conn.close()

import socket
p,q = 151,43
n = p*q

csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#establishing connection with the server
csocket.connect(("localhost", 8000))
res = csocket.recv(4096).decode()
print(res)
serverKey = int(csocket.recv(4096).decode())
print(serverKey)
csocket.send((str(n)).encode()) #sent its public key to the server  

def encryption(strVal, n):
    c = (strVal**2)%n
    return c

def mod(k, b, m):
    i = 0
    a = 1
    d = list()
    while(k>0):
        d.append(k%2)
        k = (k-d[i])//2
        i=i+1

    for j in range(0, i):
        if(d[j] == 1):
            a = (a*b)%m
        b = (b*b)%m
    return a       

def modulo(a, b):
    if(a>=0):
        return (a%b)
    return ((b-abs(a%b))%b) 

def extendedEuclidian(a, b):
    if(b>a):
        temp=a
        a=b
        b=temp
    i,j,x,y = 0,1,1,0
    while(b!=0):
        q = a//b
        temp1 = a%b
        a = b
        b = temp1
        temp2 = i
        i = x-q*i
        x=temp2
        temp3 = j
        j = y-q*j
        y=temp3
    d = list()
    d.append(x)
    d.append(y)
    return d

def decrypt(c, p, q):
    r = mod((p+1)//4, c, p)
    s = mod((q+1)//4, c, q)
    d = extendedEuclidian(p, q)
    rootp = d[0]*p*s 
    rootq = d[1]*q*r
    r1 = modulo((rootp+rootq), n)
    if(r1<128):
        return r1
    negative_r = n-r1
    if(negative_r<128):
        return negative_r
    s1 = modulo((rootp-rootq), n)
    if(s1<128):
        return s1
    negative_s = n-s1
    return negative_s 

def encryptWithRabin(d:list):
    s=""
    for i in d:
        s = s + str(i) + "."
    return s[0:len(s)-1]    

def decryptWithRabin(s:str):
    chars = s.split(".")
    d = list()
    for i in chars:
        d.append(int(i))
    return d 

while(True):
    msg = input("->")
    d = list()
    for i in msg:
        d.append(encryption(ord(i), serverKey))
    s = encryptWithRabin(d)    
    csocket.send(s.encode())
    res = csocket.recv(4096).decode()
    res = decryptWithRabin(res)
    s=""
    for i in res:
        s=s+(chr(decrypt(i, p, q)))
    print(s)
    if(s == "bye"):
        break

csocket.close()
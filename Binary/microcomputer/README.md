# microcomputer [Binary / 500pt]

## Problem

Remote debugging of a micro computer.
The server is running on GDB simulator with special patch.

* Connect to the server.

```bash
$ telnet micro.pwn.seccon.jp 10000
$ echo '+$g#67+' | nc micro.pwn.seccon.jp 10000
```
A long connection is disconnected automatically.

* Read "flag.txt" on current directory.

Reference:

* Assembly samples for many architectures

[cross-20130826.zip](http://kozos.jp/books/asm/cross-20130826.zip)

ref: [http://kozos.jp/books/asm/cross-20130826.zip](http://kozos.jp/books/asm/cross-20130826.zip)

See the assembly samples.

```bash
$ unzip cross-20130826.zip
$ cd cross/sample
$ ls *.d
```

See the sample programs running on GDB simulator.

```bash
$ cd cross/exec
$ ls *.d
```

## Answer

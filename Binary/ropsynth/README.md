# ropsynth [Binary / 400pt]

## Problem
`ropsynth.pwn.seccon.jp:10000`

Read "secret" and output the content such as the following code.

```
fd = open("secret", 0, 0);
len = read(fd, buf, 256);
write(1, buf, len);
```

[dist.tgz](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Binary/ropsynth/dist.tgz)

## Answer

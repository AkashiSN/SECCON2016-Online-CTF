# VoIP [Forensics / 100pt]

## Question

```plain
VoIP
Extract a voice.
The flag format is SECCON{[A-Z0-9]}.
```

[voip.pcap](https://github.com/AkashiSN/SECCON2016-Online-CTF/blob/master/Forensics/VoIP/voip.pcap)

## Answer


Ip電話のパケットのようなので、Wiresharkの`電話(y)→VoIP通話(V)→ストリーム再生`で音声を聞ける。

`V`の発音がわからず苦労した

FLAG:`SECCON{9001IVR}`

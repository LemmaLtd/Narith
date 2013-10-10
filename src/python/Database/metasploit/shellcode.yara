rule exec
{
    strings:
        $a = { FC E8 89 00 00 00 60 89 E5 31 D2 64 8B 52 30 8B 52 0C 8B 52 14 8B 72 28 0F B7 4A 26 31 FF 31 C0 AC 3C 61 7C 02 2C 20 C1 CF 0D 01 C7 E2 F0 52 57 8B 52 10 8B 42 3C 01 D0 8B 40 78 85 C0 74 4A 01 D0 50 8B 48 18 8B 58 20 01 D3 E3 3C 49 8B 34 8B 01 D6 31 FF 31 C0 AC C1 CF 0D 01 C7 38 E0 75 F4 03 7D F8 3B 7D 24 75 E2 58 8B 58 24 01 D3 66 8B 0C 4B 8B 58 1C 01 D3 8B 04 8B 01 D0 89 44 24 24 5B 5B 61 59 5A 51 FF E0 58 5F 5A 8B 12 EB 86 5D 6A 01 8D 85 B9 00 00 00 50 68 31 8B 6F 87 FF D5 BB E0 1D 2A 0A 68 A6 95 BD 9D FF D5 3C 06 7C 0A 80 FB E0 75 05 BB 47 13 72 6F 6A 00 53 FF D5}
    condition:
        $a
}

rule shell_reverse_tcp
{
    strings:
        $a = { FC E8 89 00 00 00 60 89 E5 31 D2 64 8B 52 30 8B 52 0C 8B 52 14 8B 72 28 0F B7 4A 26 31 FF 31 C0 AC 3C 61 7C 02 2C 20 C1 CF 0D 01 C7 E2 F0 52 57 8B 52 10 8B 42 3C 01 D0 8B 40 78 85 C0 74 4A 01 D0 50 8B 48 18 8B 58 20 01 D3 E3 3C 49 8B 34 8B 01 D6 31 FF 31 C0 AC C1 CF 0D 01 C7 38 E0 75 F4 03 7D F8 3B 7D 24 75 E2 58 8B 58 24 01 D3 66 8B 0C 4B 8B 58 1C 01 D3 8B 04 8B 01 D0 89 44 24 24 5B 5B 61 59 5A 51 FF E0 58 5F 5A 8B}
    condition:
        $a

}

rule shell_bind_tcp
{
    strings:
        $a = { FC E8 89 00 00 00 60 89 E5 31 D2 64 8B 52 30 8B 52 0C 8B 52 14 8B 72 28 0F B7 4A 26 31 FF 31 C0 AC 3C 61 7C 02 2C 20 C1 CF 0D 01 C7 E2 F0 52 57 8B 52 10 8B 42 3C 01 D0 8B 40 78 85 C0 74 4A 01 D0 50 8B 48 18 8B 58 20 01 D3 E3 3C 49 8B 34 8B 01 D6 31 FF 31 C0 AC C1 CF 0D 01 C7 38 E0 75 F4 03 7D F8 3B 7D 24 75 E2 58 8B 58 24 01 D3 66 8B 0C 4B 8B 58 1C 01 D3 8B 04 8B 01 D0 89 44 24 24 5B 5B 61 59 5A 51 FF E0 58 5F 5A 8B}
    condition:
        $a
}

rule shell_bind_tcp_xpfw
{
    strings:
        $a = { e8 56 00 00 00 53 55 56 57 8b 6c 24 18 8b 45 3c 8b 54 05 78 01 ea 8b 4a 18 8b 5a 20 01 eb e3 32 49 8b 34 8b 01 ee 31 ff fc 31 c0 ac 38 e0 74 07 c1 cf 0d 01 c7 eb f2 3b 7c 24 14 75 e1 8b 5a 24 01 eb 66 8b 0c 4b 8b 5a 1c 01 eb 8b 04 8b 01 e8 eb 02 31 c0 5f 5e 5d 5b c2 08 00 5e 6a 30 59 64 8b 19 8b 5b 0c 8b 5b 1c 8b 1b 8b 5b 08 53 68 8e 4e 0e ec ff d6 89 c7 81 ec 00 01 00 00 57 56 53 89 e5 e8 27 00 00 00 90 01 00 00 b6 19 18 e7 a4 19 70 e9 e5 49 86 49 a4 1a 70 c7 a4 ad 2e e9 d9 09 f5 ad cb ed fc 3b 57 53 32 5f 33 32 00 5b 8d 4b 20 51 ff d7 89 df 89 c3 8d 75 14 6a 07 59 51 53 ff 34 8f ff 55 04 59 89 04 8e e2 f2 2b 27 54 ff 37 ff 55 30 31 c0 50 50 50 50 40 50 40 50 ff 55 2c 89 c7 89 7d 0c e8 06 00 00 00 4f 4c 45 33 32 00 ff 55 08 89 c6 56 68 1b 06 c8}
    condition:
        $a
}

rule speak_pwned
{
    strings:
        $a = { 66 81 e4 fc ff 31 f6 64 8b 76 30 8b 76 0c 8b 76 1c 56 66 be aa 1a 5f 8b 6f 08 ff 37 8b 5d 3c 8b 5c 1d 78 01 eb 8b 4b 18 67 e3 eb 8b 7b 20 01 ef 8b 7c 8f fc 01 ef 31 c0 99 32 17 66 c1 ca 01 ae 75 f7 49 66 39 f2 74 08 67 e3 cb e9 db ff ff ff 8b 73 24 01 ee 0f b7 34 4e 8b 43 1c 01 e8 8b 3c b0 01 ef 31 f6 66 81 fa da f0 74 1b 66 81 fa 69 27 74 20 6a 32 68 6f 6c 65 33 54 ff d7 95 66 be da f0 e9 95 ff ff ff 56 ff d7 66 be 69 27 e9 89 ff ff ff 68 6e 04 22 d4 68 a1 ec ef 99 68 b9 72 92 49 68 74 df 44 6c 89 e0 68 4f 79 73 96 68 9e e3 01 c0 ff 4c 24 02 68 91 33 d2 11 68 77 93 74 96 89 e3 56 54 50 6a 17 56 53 ff d7 5b 68 6f 67 20 55 68 6f 70 20 74 68 21 64 6e 68 96 89 e6 50 ac 66 50 3c 55 75 f9 89 e1 31 c0 50 50 51 53 8b 13 8b 4a 50 ff d1 cc}
    condition:
        $a
}

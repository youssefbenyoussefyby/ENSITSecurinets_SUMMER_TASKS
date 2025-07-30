def inv_digit_shuffle(s: str, seed: int) -> str:
    digits = list(s)
    for i in range(len(digits)):
        j = (i * seed) % len(digits)
        digits[i], digits[j] = digits[j], digits[i]
    return ''.join(digits)

def inv_rotate_xor(data, rot, key):
    out = bytearray()
    for b in data:
        r = b ^ key
        orig = ((r >> rot) | ((r << (8 - rot)) & 0xFF)) & 0xFF
        out.append(orig)
    return bytes(out)

def inv_interleave_scramble(s, rounds):
    for _ in range(rounds):
        a_rev = s[0::2]
        b_rev = s[1::2]
        s = a_rev[::-1] + b_rev[::-1]
    return s

target = "85682cce0a4d29cdeec9ee0c0e4ce80545a82fcf2eeec9456b8b88afac49"
hexstr = inv_digit_shuffle(target, seed=7)
enc = bytes.fromhex(hexstr)
scrambled = inv_rotate_xor(enc, rot=5, key=0xA3).decode()
core = inv_interleave_scramble(scrambled, rounds=3)
flag = f"Securinets{{{core}}}"
print(flag)

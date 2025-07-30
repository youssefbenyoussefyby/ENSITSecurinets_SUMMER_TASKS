import sys

def interleave_scramble(s: str, rounds: int) -> str:
    for _ in range(rounds):
        mid = len(s) // 2
        a, b = s[:mid][::-1], s[mid:][::-1]
        s = ''.join(x + y for x, y in zip(a, b))
    return s

def rotate_xor(data: bytes, rot: int, key: int) -> bytes:
    out = bytearray()
    for b in data:
        r = ((b << rot) & 0xFF) | (b >> (8 - rot))
        out.append(r ^ key)
    return bytes(out)

def digit_shuffle(s: str, seed: int) -> str:
    digits = list(s)
    for i in range(len(digits)):
        j = (i * seed) % len(digits)
        digits[i], digits[j] = digits[j], digits[i]
    return ''.join(digits)

def check_flag(candidate: str) -> bool:
    if not (candidate.startswith("Securinets{") and candidate.endswith("}")):
        return False

    core = candidate[len("Securinets{"):-1]
    s1 = interleave_scramble(core, rounds=3)
    s2 = rotate_xor(s1.encode(), rot=5, key=0xA3)
    final = digit_shuffle(s2.hex(), seed=7)
    target = "85682cce0a4d29cdeec9ee0c0e4ce80545a82fcf2eeec9456b8b88afac49"
    return final == target

if __name__ == "__main__":
    flag = input("Enter flag: ").strip()
    print(f"🎉 Congratulations! 🎉\nYou’ve cracked the code and unveiled the hidden treasure:{flag}!" if check_flag(flag) else "Wrong!")

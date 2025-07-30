# CTF Challenge Write-up

**Flag:** `Securinets{PyTh0n_C4n_b3_Cr4zzy_SOmeTimes}`

---

## 📋 Overview

This challenge provides a compiled Python bytecode file (`chal.pyc`). Your goal is to reverse-engineer the logic, invert its transformations, and recover the hidden flag.

The core transformations applied to the flag’s inner content (`core`) are:

1. **Interleave Scramble** (3 rounds)
2. **Rotate-XOR** (rotate by 5 bits, XOR with key 163)
3. **Digit Shuffle** (hex string, seed 7)

To solve, you need to decompile, understand each step, and implement inverses in the correct order.

---

## 🕵️ Player’s Perspective

### 1. Decompile the Bytecode

```bash
pylingual chal.pyc --output chal.py
````
#### Setup

Install from source, using Poetry:
```
git clone https://github.com/syssec-utd/pylingual
cd pylingual
python -m venv venv
source venv/bin/activate
pip install poetry>=2.0
poetry install
```
#### Usage
```
Usage: pylingual [OPTIONS] [FILES]...

  End to end pipeline to decompile Python bytecode into source code.

Options:
  -o, --out-dir PATH      The directory to export results to.
  -c, --config-file PATH  Config file for model information.
  -v, --version VERSION   Python version of the .pyc, default is auto
                          detection.
  -k, --top-k INT         Maximum number of additional segmentations to
                          consider.
  -q, --quiet             Suppress console output.
  --trust-lnotab          Use the lnotab for segmentation instead of the
                          segmentation model.
  --init-pyenv            Install pyenv before decompiling.
  -h, --help              Show this message and exit.
```

This reveals the Python source with functions:

* `interleave_scramble(s, rounds)`
* `rotate_xor(data, rot, key)`
* `digit_shuffle(s, seed)`
* `check_flag(candidate)`

### 2. Examine `check_flag`

Read the decompiled logic:

```python
if not candidate.startswith('Securinets{') or not candidate.endswith('}'):
    return False
core = candidate[len('Securinets{'):-1]
s1 = interleave_scramble(core, rounds=3)
s2 = rotate_xor(s1.encode(), rot=5, key=163)
final = digit_shuffle(s2.hex(), seed=7)
return final == target
```

#### Key insights:

* The flag format is `Securinets{<core>}`.
* The **core** is scrambled thrice, then byte-transformed, then digits permuted.
* The final result is compared to a constant hex string:

  `85682cce0a4d29cdeec9ee0c0e4ce80545a82fcf2eeec9456b8b88afac49`

### 3. Invert the Transformations

The correct order to invert is the reverse of the forward pipeline:

1. **Inverse Digit Shuffle**
2. **Inverse Rotate-XOR**
3. **Inverse Interleave Scramble**

#### a. Inverse Digit Shuffle

Original `digit_shuffle(s, seed)` does:

```python
for i in range(len(digits)):
    j = i * seed % len(digits)
    digits[i], digits[j] = digits[j], digits[i]
```

Swapping twice using the same operations restores the original order because each swap is its own inverse. Thus, calling `digit_shuffle` again with the same seed reverses it.

```python
hexstr = inv_digit_shuffle(target, seed=7)
# where inv_digit_shuffle = digit_shuffle
```

#### b. Inverse Rotate-XOR

Forward:

```python
r = rol(b, rot)
out_byte = r ^ key
```

To invert:

1. XOR with `key`: `r = byte ^ key`
2. Rotate right by `rot` bits.

```python
def inv_rotate_xor(data, rot, key):
    return bytes(((b ^ key) >> rot | ((b ^ key) << (8-rot)) & 0xFF) & 0xFF for b in data)
```

#### c. Inverse Interleave Scramble

Forward (per round):

1. Split into halves: `a = s[:mid]`, `b = s[mid:]`
2. Reverse each half
3. Interleave: `x0+y0, x1+y1, ...`

To undo:

1. Take even indices for reversed `a`, odd for reversed `b`
2. Reverse each
3. Concatenate

```python
def inv_interleave_scramble(s, rounds):
    for _ in range(rounds):
        a_rev = s[0::2]
        b_rev = s[1::2]
        s = a_rev[::-1] + b_rev[::-1]
    return s
```

### 4. Recover the Flag

Putting it all together:

```python
from chal_inv import (
    inv_digit_shuffle,
    inv_rotate_xor,
    inv_interleave_scramble
)

target = "85682cce0a4d29cdeec9ee0c0e4ce80545a82fcf2eeec9456b8b88afac49"
hexstr = inv_digit_shuffle(target, seed=7)
enc = bytes.fromhex(hexstr)
scrambled = inv_rotate_xor(enc, rot=5, key=0xA3).decode()
core = inv_interleave_scramble(scrambled, rounds=3)
flag = f"Securinets{{{core}}}"
print(flag)  # Securinets{PyTh0n_C4n_b3_Cr4zzy_SOmeTimes}
```

---

## 🛠️ Author’s Perspective

### Design Rationale

1. **Interleave Scramble**:

   * Combines string reversal and interleaving to obscure positional information.
   * Multiple rounds amplify confusion: characters move far from original index.

2. **Rotate-XOR**:

   * Byte-level operation introduces non-linear mixing.
   * Bit rotations prevent simple XOR-key frequency analysis.

3. **Digit Shuffle**:

   * Operates on hex representation, permuting even more.
   * Leverages modular arithmetic for a deterministic but non-trivial permutation.

By stacking these, we ensure that solving requires understanding bytecode decompilation, string manipulations, bitwise operations, and permutation inversion.

### Implementation Notes

* Decompiling with **PyLingual** preserves high-level constructs, making reverse-engineering feasible.
* Designing inversions:

  * Swaps are involutive: swap twice restores original.
  * XOR and rotations are invertible with complementary bit operations.
  * Interleave is undone by selecting positions and reversing slices.

### Learning Points

* Modern CTF challenges often combine Python bytecode with custom obfuscation.
* Familiarity with bitwise operations and slicing in Python is essential.
* Permutation-based obfuscation can be surprisingly simple yet effective.

---

*End of write-up.*

```
```

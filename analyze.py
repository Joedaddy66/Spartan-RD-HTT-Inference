import pandas as pd
import math
import sympy as sp
import re
from typing import Tuple

BASE4 = {"A": 0, "C": 1, "G": 2, "T": 3}
CODON2INT = {
    a + b + c: BASE4[a] * 16 + BASE4[b] * 4 + BASE4[c]
    for a in "ACGT" for b in "ACGT" for c in "ACGT"
}

def codon_to_int(codon: str) -> int:
    codon = codon.upper()
    if len(codon) != 3 or any(n not in BASE4 for n in codon):
        raise ValueError(f"Invalid codon: {codon!r}")
    return CODON2INT[codon]

def semiprime_factors(n: int) -> Tuple[int, int]:
    factors = sp.factorint(n)
    if len(factors) != 2 or any(exp != 1 for exp in factors.values()):
        raise ValueError("Not a semiprime")
    p, q = factors.keys()
    return int(p), int(q)

def fingerprint(p: int, q: int) -> float:
    a = (p + q) / 2
    m = p * q
    delta = abs(p - q)
    if a <= 1: return 0.0
    return delta**2 / (m * math.log(a))

def analyze_sequence_for_score(seq: str, step: int = 1, pam_pattern: str = 'GG') -> float:
    total_lambda = 0.0
    seq = seq.upper()
    # Find every occurrence of the PAM (e.g., GG)
    for m in re.finditer(f'(?=(.[ACGT]{pam_pattern}))', seq):
        pam_index = m.start()
        if pam_index < 20: continue # Need at least 20bp before the PAM
        
        protospacer = seq[pam_index-20:pam_index]
        # Calculate resonance for this specific 20bp window
        for i in range(0, len(protospacer) - 5, step):
            try:
                c1 = codon_to_int(protospacer[i : i + 3])
                c2 = codon_to_int(protospacer[i + 3 : i + 6])
                N = c1 * 64 + c2
                p, q = semiprime_factors(N)
                total_lambda += fingerprint(p, q)
            except (ValueError, KeyError):
                continue
    return total_lambda

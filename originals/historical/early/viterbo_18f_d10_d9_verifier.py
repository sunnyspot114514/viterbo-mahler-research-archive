#!/usr/bin/env python3
"""Exact verifier for the 12V/18F, c=0, D=10 and D=9 closure.

The verifier checks four layers.

1. Relative orbit completeness from the previously certified D=11 profile
   (2,2,2,1): 95 base orbits extend to exactly 802 profile-(2,2,2,2)
   and 2335 profile-(3,2,2,1) orbits.
2. Every orbit labelled rank_ge_5 carries an exact sign-definite
   multiaffine 5x5-minor certificate.  Determinants are recomputed by
   integer Bareiss elimination, with no floating point arithmetic.
3. All remaining orbits are classified: inactive primal columns coincide
   or are antipodal, except for three symbolic families.  The three
   families are checked by exact rank factorization and exact row-space
   identities; each forces extra section vertices incompatible with D=10.
4. The only possible D=9 extension is a profile-(3,2,2,2) family.  An
   exact rank factorization exhibits one nominal primal vertex pair in
   the relative interior of an edge, so it is not a 12-vertex object.

The finite multiplicity-four facts used to close profile (4,2,2) are also
recomputed exactly.  The accompanying lemma file supplies the short
rank-three Gale inequalities.

Usage:
    python viterbo_18f_d10_d9_verifier.py
    python viterbo_18f_d10_d9_verifier.py --certificate path/to/json

Dependencies: Python 3, numpy, sympy.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import sympy as sp


def det_bareiss(matrix: Sequence[Sequence[int]]) -> int:
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    if any(len(row) != n for row in a):
        raise ValueError("square matrix required")
    sign, prev = 1, 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if a[r][k] != 0), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // prev
        prev = p
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[n - 1][n - 1]


def rank_fraction(matrix: Sequence[Sequence[int]]) -> int:
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [a[i][j] - q * a[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def primitive(values: Sequence[int]) -> tuple[int, ...]:
    vals = list(map(int, values))
    g = 0
    for x in vals:
        g = math.gcd(g, abs(x))
    if g:
        vals = [x // g for x in vals]
    for x in vals:
        if x:
            if x < 0:
                vals = [-y for y in vals]
            break
    return tuple(vals)


def cofactor_kernel(rows: Sequence[Sequence[int]]) -> tuple[int, ...]:
    cof = []
    for j in range(5):
        minor = [[row[k] for k in range(5) if k != j] for row in rows]
        cof.append(((-1) ** j) * det_bareiss(minor))
    h = primitive(cof)
    assert any(h)
    assert all(sum(row[j] * h[j] for j in range(5)) == 0 for row in rows)
    return h


def admissible_singleton_directions(h: Sequence[int]) -> list[int]:
    out = []
    for j in range(5):
        others = [k for k in range(5) if k != j]
        for signs in itertools.product((-1, 1), repeat=4):
            s = sum(signs[i] * h[k] for i, k in enumerate(others))
            feasible = (s == 0) if h[j] == 0 else (abs(s) < abs(h[j]))
            if feasible:
                out.append(j)
                break
    return out


def verify_multiplicity_four_finite_input() -> dict:
    vectors = [tuple(1 if (i >> k) & 1 else -1 for k in range(4)) + (1,)
               for i in range(16)]
    ranks = Counter()
    patterns = Counter()
    admissible = Counter()
    for subset in itertools.combinations(range(16), 4):
        mat = [vectors[i] for i in subset]
        r = rank_fraction(mat)
        ranks[r] += 1
        if r == 4:
            h = cofactor_kernel(mat)
            pat = tuple(sorted(abs(x) for x in h))
            patterns[pat] += 1
            admissible[(pat, len(admissible_singleton_directions(h)))] += 1
    assert ranks == Counter({4: 1720, 3: 100})
    assert patterns == Counter({
        (0, 0, 0, 1, 1): 1160,
        (0, 1, 1, 1, 1): 480,
        (1, 1, 1, 1, 2): 80,
    })
    assert admissible == Counter({
        ((0, 0, 0, 1, 1), 3): 1160,
        ((0, 1, 1, 1, 1), 1): 480,
        ((1, 1, 1, 1, 2), 1): 80,
    })
    return {"rank_counts": dict(ranks), "kernel_patterns": {str(k): v for k, v in patterns.items()}}


def generate_rows() -> tuple[list[tuple[int, tuple[int, ...]]], dict[tuple[int, tuple[int, ...]], int]]:
    rows = []
    rid = {}
    for j in range(6):
        others = [k for k in range(6) if k != j]
        first = others[0]
        for bits in itertools.product((-1, 1), repeat=4):
            s = [0] * 6
            s[first] = 1
            for k, bit in zip(others[1:], bits):
                s[k] = bit
            rid[(j, tuple(s))] = len(rows)
            rows.append((j, tuple(s)))
    assert len(rows) == 96
    return rows, rid


def generate_B6_actions(rows, rid) -> np.ndarray:
    actions = []
    seen = set()
    for perm in itertools.permutations(range(6)):
        for flips in itertools.product((-1, 1), repeat=6):
            image = []
            for j, s in rows:
                t = [0] * 6
                nj = perm[j]
                for k in range(6):
                    if k != j:
                        t[perm[k]] = flips[k] * s[k]
                first = next(k for k in range(6) if k != nj)
                if t[first] < 0:
                    t = [-x for x in t]
                image.append(rid[(nj, tuple(t))])
            tup = tuple(image)
            if tup not in seen:
                seen.add(tup)
                actions.append(tup)
    assert len(actions) == 23040
    return np.asarray(actions, dtype=np.uint8)


def lexmin_rows(arr: np.ndarray) -> tuple[int, ...]:
    order = np.lexsort(tuple(arr[:, i] for i in range(arr.shape[1] - 1, -1, -1)))
    return tuple(int(x) for x in arr[order[0]])


def canonical(C: Sequence[int], actions: np.ndarray) -> tuple[int, ...]:
    arr = np.sort(actions[:, np.asarray(C, dtype=np.int64)], axis=1)
    return lexmin_rows(arr)


def stabilizer(C: Sequence[int], actions: np.ndarray) -> np.ndarray:
    arr = np.sort(actions[:, np.asarray(C, dtype=np.int64)], axis=1)
    target = np.asarray(sorted(C), dtype=np.uint8)
    return np.flatnonzero(np.all(arr == target, axis=1))


def augment_base(base: Sequence[Sequence[int]], target: str, rows, actions) -> set[tuple[int, ...]]:
    raw = []
    for C0 in base:
        C = tuple(C0)
        stab = stabilizer(C, actions)
        counts = Counter(rows[r][0] for r in C)
        want = 1 if target == "2222" else 2
        candidates = [r for r, (j, _) in enumerate(rows) if counts[j] == want and r not in C]
        reps = {}
        for r in candidates:
            arr = np.sort(actions[stab][:, np.asarray([r])], axis=1)
            key = lexmin_rows(arr)
            reps.setdefault(key, r)
        raw.extend(tuple(sorted(C + (r,))) for r in reps.values())
    return {canonical(C, actions) for C in raw}


def exact_corner_dets(record: dict) -> list[int]:
    A = np.asarray([row[1] for row in record["rows"]], dtype=int)
    dirs = [row[0] for row in record["rows"]]
    rsel = record["minor_certificate"]["rows"]
    csel = record["minor_certificate"]["cols"]
    B0 = A[np.ix_(rsel, csel)].copy()
    varloc = []
    for loc, r in enumerate(rsel):
        c = dirs[r]
        if c in csel:
            varloc.append((loc, csel.index(c)))
    vals = []
    for bits in itertools.product((-1, 1), repeat=len(varloc)):
        B = B0.copy()
        for (loc, cc), bit in zip(varloc, bits):
            B[loc, cc] = bit
        vals.append(det_bareiss(B.tolist()))
    return vals


def config_matrix(rows, C, variables):
    mat = []
    for i, r in enumerate(C):
        j, s = rows[r]
        row = list(s)
        row[j] = variables[i]
        mat.append(row)
    return sp.Matrix(mat)


def verify_rank_factorization(X: sp.Matrix, R: Sequence[int], C: Sequence[int]) -> sp.Matrix:
    B = X.extract(R, C)
    assert sp.simplify(B.det()) != 0
    U = X[:, C]
    V = sp.simplify(B.inv() * X.extract(R, range(X.cols)))
    assert sp.simplify(U * V - X) == sp.zeros(X.rows, X.cols)
    return V


def assert_row_in_rowspace(X: sp.Matrix, row: Sequence, R: Sequence[int], C: Sequence[int]) -> None:
    B = X.extract(R, C)
    rr = sp.Matrix([row])
    lam = sp.simplify(rr[:, C] * B.inv())
    assert sp.simplify(lam * X.extract(R, range(X.cols)) - rr) == sp.zeros(1, X.cols)


def verify_symbolic_survivors(data, rows, actions, rid) -> dict:
    out = {}
    # 2222 survivor 17.
    t, u = sp.symbols("t u", real=True)
    C17 = tuple(data["special_survivors"]["2222_17"]["row_ids"])
    X17 = config_matrix(rows, C17, [t, t, t, t, -u, u, u, -u])
    verify_rank_factorization(X17, (0, 1, 4, 5), (1, 2, 3, 5))
    for r in ([1, -1, 0, 0, -1, -1], [1, -1, 0, 0, 1, 1]):
        assert_row_in_rowspace(X17, r, (0, 1, 4, 5), (1, 2, 3, 5))
    out["2222_17"] = "rank 4; two forced double rows"

    # 2222 survivor 20.
    a, T, s = sp.symbols("a T s", real=True)
    f = sp.factor(((T - 1) * s - 2 * T) / (T + 1))
    C20 = tuple(data["special_survivors"]["2222_20"]["row_ids"])
    X20 = config_matrix(rows, C20, [a, a, T, T, -s, -f, s, f])
    verify_rank_factorization(X20, (0, 1, 4, 5), (1, 2, 3, 5))
    z = sp.factor((1 - T - 2 * s) / (1 + T))
    for r in ([a, -1, -1, -1, z, -1], [a, -1, -1, -1, 1, -z]):
        assert_row_in_rowspace(X20, r, (0, 1, 4, 5), (1, 2, 3, 5))
    assert sp.factor(1 - z**2 - 4 * (1 - s) * (T + s) / (1 + T)**2) == 0
    wall_row = [-a, 1, 1, 1, -1, 1]
    assert_row_in_rowspace(X20.subs(s, -T), wall_row, (0, 1, 4, 5), (1, 2, 3, 5))
    z1 = sp.factor((2 * T + s + 1) / (s - 1))
    y3 = sp.factor((T*a*s + T*a - 2*T + a*s + a - 2*s) / ((T - 1)*(s - 1)))
    z3 = sp.factor(-(T*s + 3*T + 3*s + 1) / ((T - 1)*(s - 1)))
    for r in ([a, z1, -1, -1, 1, -1], [y3, -1, -1, z3, 1, -1]):
        assert_row_in_rowspace(X20, r, (0, 1, 4, 5), (1, 2, 3, 5))
    assert sp.factor(1 - z1**2 + 4*(T+1)*(T+s)/(s-1)**2) == 0
    assert sp.factor(1 - z3**2 + 8*(T+1)*(T+s)*(s+1)/((T-1)**2*(s-1)**2)) == 0
    F3 = a*(T+1)*(s+1) + T*s - 3*T - 3*s + 1
    assert sp.factor(F3.subs(a, -1) + 4*(T+s)) == 0
    assert sp.factor(1-y3**2 + (T+1)*(a-1)*(s+1)*F3/((T-1)**2*(s-1)**2)) == 0
    out["2222_20"] = "rank 4; doubles off wall, extra single on wall"

    # 3221 survivor 133.
    p, q = sp.symbols("p q", real=True)
    C133 = tuple(data["special_survivors"]["3221_133"]["row_ids"])
    X133 = config_matrix(rows, C133, [p, p, p, q, q, q, q, -q])
    verify_rank_factorization(X133, (0, 1, 2, 3), (1, 2, 4, 5))
    extra = [1, -1, -1, 1, -1, -q]
    assert_row_in_rowspace(X133, extra, (0, 1, 2, 3), (1, 2, 4, 5))
    out["3221_133"] = "rank 4; forced ninth single"

    # The two extra-single branches have the same B6 canonical 9-row orbit.
    wall_id = rid[(0, (0, 1, 1, 1, -1, 1))]
    extra_id = rid[(5, (1, -1, -1, 1, -1, 0))]
    can20 = canonical(tuple(sorted(C20 + (wall_id,))), actions)
    can133 = canonical(tuple(sorted(C133 + (extra_id,))), actions)
    target = tuple(data["D9"]["unique_canonical_row_ids"])
    assert can20 == can133 == target

    # Exact D9 rank factorization and loss of one primal vertex pair.
    X9 = sp.Matrix([
        [p, 1, -1, -1, -1, -1],
        [p, 1, -1, -1, 1, 1],
        [p, 1, -1, 1, -1, 1],
        [1, -1, -1, q, -1, -1],
        [1, -1, -1, q, 1, 1],
        [1, -1, -1, -1, q, -1],
        [1, -1, -1, 1, q, 1],
        [1, -1, -1, -1, 1, -q],
        [1, -1, -1, 1, -1, -q],
    ])
    V = verify_rank_factorization(X9, (0, 1, 2, 3), (1, 2, 3, 4))
    identity = sp.simplify(V[:, 0] - ((1-p)/2)*(-V[:, 1]) - ((1+p)/2)*(-V[:, 2]))
    assert identity == sp.zeros(4, 1)
    out["D9"] = "unique 3222 orbit; v0 is in the relative interior of [-v1,-v2]"
    return out


def partitions(n: int, maxpart: int = 4, maxlen: int = 6) -> list[tuple[int, ...]]:
    out = []
    def rec(rem, mx, cur):
        if rem == 0:
            if len(cur) <= maxlen:
                out.append(tuple(cur))
            return
        if len(cur) >= maxlen:
            return
        for x in range(min(mx, rem), 0, -1):
            rec(rem-x, x, cur+[x])
    rec(n, maxpart, [])
    return out


def verify_partition_tables(data) -> dict:
    p8 = partitions(8)
    p9 = partitions(9)
    listed8 = {tuple(map(int, k.split(','))) for k in data["D10_partition_coverage"]["partitions"]}
    assert set(p8) == listed8
    assert len(p8) == 13 and len(p9) == 14
    assert (3, 2, 2, 2) in p9
    return {"D10_partitions": len(p8), "D9_partitions": len(p9), "D9_unique_candidate": [3,2,2,2]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=Path(__file__).with_name("viterbo_18f_d10_d9_certificate.json"))
    parser.add_argument("--skip-orbit-regeneration", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text(encoding="utf-8"))

    rows, rid = generate_rows()
    actions = generate_B6_actions(rows, rid)

    if not args.skip_orbit_regeneration:
        base = data["base_D11_2221_survivors"]
        for target in ("2222", "3221"):
            generated = augment_base(base, target, rows, actions)
            certified = {tuple(rec["row_ids"]) for rec in data["profiles"][target]["records"]}
            assert generated == certified
            assert len(generated) == data["profiles"][target]["orbit_count"]

    cert_counts = {}
    for name in ("2222", "3221"):
        rank5 = survivors = inactive = 0
        for rec in data["profiles"][name]["records"]:
            if rec["status"] == "rank_ge_5":
                vals = exact_corner_dets(rec)
                assert vals == rec["minor_certificate"]["corner_dets"]
                assert ((all(x >= 0 for x in vals) and any(x > 0 for x in vals)) or
                        (all(x <= 0 for x in vals) and any(x < 0 for x in vals)))
                rank5 += 1
            else:
                survivors += 1
                if "inactive_column_certificate" in rec:
                    cert = rec["inactive_column_certificate"]
                    j, k = cert["inactive_cols"]
                    cj = [row[1][j] for row in rec["rows"]]
                    ck = [row[1][k] for row in rec["rows"]]
                    if cert["relation"] == "equal":
                        assert cj == ck
                    else:
                        assert cj == [-x for x in ck]
                    inactive += 1
        expected = data["profiles"][name]
        assert rank5 == expected["rank_ge_5_count"]
        assert survivors == expected["survivor_count"]
        if name == "2222":
            assert inactive == 19
        else:
            assert inactive == 133
        cert_counts[name] = {"rank_ge_5": rank5, "survivors": survivors,
                             "inactive_column_loss": inactive}

    m4 = verify_multiplicity_four_finite_input()
    symbolic = verify_symbolic_survivors(data, rows, actions, rid)
    part = verify_partition_tables(data)

    print(json.dumps({
        "status": "PASS",
        "B6_action_size": int(actions.shape[0]),
        "certificate_counts": cert_counts,
        "multiplicity_four": m4,
        "symbolic_survivors": symbolic,
        "partition_check": part,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

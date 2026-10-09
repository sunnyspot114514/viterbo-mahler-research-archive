# Closing the final two defect layers in the 12-vertex, 18-facet branch

**Date:** 17 August 2026  
**Scope:** four-dimensional centrally symmetric Mahler / symmetric Viterbo, bounded-12 reduction  
**Status:** computer-assisted analytic proof candidate

## 1. Setup

Let a centrally symmetric four-polytope have six antipodal vertex pairs and nine antipodal facet pairs. Its pairing matrix is

\[
X\in[-1,1]^{9\times6},\qquad \operatorname{rank}X\le4.
\]

An entry is a **defect** when its absolute value is strictly below one. In the \(c=0\) branch, every row has at least one defect. A four-dimensional facet has at least four vertices, so every row has at most two defects.

For \(18\) facets, the SWZ flag bound gives

\[
9\le D\le13.
\]

The layers \(D=13,12,11\) were closed previously. This note closes \(D=10\) and \(D=9\).

---

## 2. Exact relative orbit enumeration for \(D=10\)

Here there are

\[
8\text{ single-defect rows}+1\text{ double-defect row}.
\]

The only eight-single profiles not already killed by seven-row structural obstructions reduce to

\[
(2,2,2,2),\qquad (3,2,2,1),\qquad (4,2,2).
\]

The first two are one-row extensions of the previously certified \((2,2,2,1)\) layer.

Starting from its 95 canonical \(B_6\)-orbits, exact hyperoctahedral augmentation gives

\[
\boxed{802\text{ profile-}(2,2,2,2)\text{ orbits}}
\]

and

\[
\boxed{2335\text{ profile-}(3,2,2,1)\text{ orbits}}.
\]

For each orbit, a \(5\times5\) minor is multiaffine in its selected defect entries. Its values at all defect-cube corners are therefore its Bernstein coefficients. If those corner determinants have one weak sign and at least one is nonzero, the minor cannot vanish in the open cube.

All stored determinant values are recomputed by integer Bareiss elimination. The result is

\[
\begin{array}{c|r|r|r}
\text{profile}&\text{orbits}&\operatorname{rank}\ge5&\text{survivors}\\
\hline
(2,2,2,2)&802&781&21\\
(3,2,2,1)&2335&2201&134
\end{array}
\]

Among the survivors:

* \(19/21\) profile-\((2,2,2,2)\) orbits have the two inactive primal columns equal or opposite;
* \(133/134\) profile-\((3,2,2,1)\) orbits have the two inactive primal columns equal or opposite.

Such an orbit has at most five distinct antipodal vertex pairs and is outside the genuine 12-vertex branch.

Only three symbolic families remain.

---

## 3. First \((2,2,2,2)\) family: two extra double facets

Rank four forces

\[
x_0=x_1=x_2=x_3=t,
\qquad
(x_4,x_5,x_6,x_7)=(-u,u,u,-u),
\]

with \(|t|,|u|<1\).

The row space always contains

\[
(1,-1,0,0,-1,-1)
\]

and

\[
(1,-1,0,0,1,1).
\]

Both are strict double-defect rows. Thus the cube section has at least

\[
8\text{ singles}+2\text{ doubles},
\]

not the \(8+1\) required by \(D=10\).

---

## 4. Second \((2,2,2,2)\) family: chamber-by-chamber closure

Rank four gives

\[
x_0=x_1=a,
\qquad
x_2=x_3=T,
\]

\[
x_4=-s,
\quad x_6=s,
\quad x_5=-f,
\quad x_7=f,
\]

where

\[
f=\frac{(T-1)s-2T}{T+1}.
\]

All displayed defect coordinates lie in \((-1,1)\).

### Chamber \(s>-T\)

The row space contains two double rows with second free coordinate

\[
z=\frac{1-T-2s}{1+T}.
\]

Their strictness follows from

\[
1-z^2=\frac{4(1-s)(T+s)}{(1+T)^2}>0.
\]

### Wall \(s=-T\)

The two double rows coalesce into the strict additional single

\[
(-a,1,1,1,-1,1).
\]

The section therefore has nine singles rather than eight singles and one double.

### Chamber \(s<-T\)

Two further double rows have free coordinates

\[
z_1=\frac{2T+s+1}{s-1},
\]

and

\[
y_3=\frac{Tas+Ta-2T+as+a-2s}{(T-1)(s-1)},
\]

\[
z_3=-\frac{Ts+3T+3s+1}{(T-1)(s-1)}.
\]

The exact identities

\[
1-z_1^2=-\frac{4(T+1)(T+s)}{(s-1)^2}>0,
\]

\[
1-z_3^2=-\frac{8(T+1)(T+s)(s+1)}{(T-1)^2(s-1)^2}>0
\]

show that \(z_1,z_3\) are strict. Also

\[
1-y_3^2=
-\frac{(T+1)(a-1)(s+1)F_3}{(T-1)^2(s-1)^2},
\]

where

\[
F_3=a(T+1)(s+1)+Ts-3T-3s+1.
\]

Since \(F_3\) is increasing in \(a\) and

\[
F_3\big|_{a=-1}=-4(T+s)>0,
\]

we have \(|y_3|<1\). Hence this chamber again has at least two strict double rows.

The family is therefore never a \(D=10\) section.

---

## 5. The \((3,2,2,1)\) family: a forced ninth single

Rank four forces

\[
x_0=x_1=x_2=p,
\]

\[
x_3=x_4=x_5=x_6=q,
\qquad
x_7=-q,
\]

with \(|p|,|q|<1\).

The row space identically contains

\[
(1,-1,-1,1,-1,-q),
\]

which is a new strict single-defect row. The section therefore has at least nine singles, not eight singles plus one double.

---

## 6. The remaining profile \((4,2,2)\)

Fix the multiplicity-four direction. Its four projective sign rows form a four-subset of

\[
\{\pm1\}^5/\{\pm1\}.
\]

The exact local enumeration gives

\[
1820=1720\text{ rank-four}+100\text{ rank-three}.
\]

### Rank four

The primitive kernel has one of the three absolute patterns

\[
(0,0,0,1,1),
\quad
(0,1,1,1,1),
\quad
(1,1,1,1,2).
\]

The latter two admit a strict singleton equation in only one further direction and cannot support two multiplicity-two directions. The support-two pattern admits three directions, but its two nonzero coefficients have equal absolute value, giving a primal relation

\[
v_i=\pm v_j.
\]

The nominal 12-vertex object then has at most ten distinct vertices.

### Rank-three orbit A

After switching,

\[
h=(0,0,p,q,-p-q).
\]

The zero-determinant directions are excluded by the same strict triangle-inequality argument used in the multiplicity-four lemma. The three remaining directions admit a strict singleton precisely under

\[
q(p+q)<0,
\qquad
p(p+q)<0,
\qquad
pq>0,
\]

respectively. These conditions are pairwise incompatible, so at most one further direction can occur.

### Rank-three orbit B

After switching,

\[
h=(0,-p,p,-q,q).
\]

If \(|q/p|<1\), strict singleton rows can occur only in the opposite pair of directions associated with \(\pm p\); if \(|q/p|>1\), only in the pair associated with \(\pm q\).

For a fixed such direction, two distinct strict rows force

\[
(\tau-\tau')+(\eta-\eta')\alpha_1=0.
\]

Multiplicity-four strictness gives \(|\alpha_1|<1\). Two distinct rows therefore require \(\alpha_1=0\). Since the corresponding second Gale coordinate is also zero, a Gale vector vanishes. This is a coloop/direct-sum stratum, reducible to the lower-dimensional symmetric Mahler theorem, not a new irreducible four-dimensional family.

Thus

\[
\boxed{(4,2,2)\text{ yields no genuine irreducible 12-vertex }D=10\text{ section}.}
\]

---

## 7. Exhaustion of all eight-single profiles

The 13 partitions of eight into at most six parts, each at most four, are

\[
\begin{gathered}
(4,4),(4,3,1),(4,2,2),(4,2,1,1),(4,1,1,1,1),\\
(3,3,2),(3,3,1,1),(3,2,2,1),(3,2,1,1,1),(3,1,1,1,1,1),\\
(2,2,2,2),(2,2,2,1,1),(2,2,1,1,1,1).
\end{gathered}
\]

They are exhausted as follows:

* two directions of multiplicity at least three exclude \((4,4),(4,3,1),(3,3,2),(3,3,1,1)\);
* the seven-row obstruction \((4,1,1,1)\) excludes \((4,2,1,1),(4,1,1,1,1)\);
* the obstruction \((3,1,1,1,1)\) excludes \((3,2,1,1,1),(3,1,1,1,1,1)\);
* the obstruction \((2,2,1,1,1)\) excludes \((2,2,2,1,1),(2,2,1,1,1,1)\);
* \((4,2,2)\) is excluded above;
* \((3,2,2,1)\) and \((2,2,2,2)\) are the exact extension classifications above.

Therefore

\[
\boxed{12V/18F,\ c=0,\ D=10\quad\checkmark.}
\]

---

## 8. The final layer \(D=9\)

Here all nine facet-pair rows are singles. Every nine-row partition except

\[
(3,2,2,2)
\]

contains one of the structural obstructions above or an eight-row configuration that forces a double facet.

The extra-single wall of the second \((2,2,2,2)\) family and the forced extra single of the \((3,2,2,1)\) family produce the same \(B_6\)-orbit. It has the exact pairing matrix

\[
X_9(p,q)=
\begin{pmatrix}
p&1&-1&-1&-1&-1\\
p&1&-1&-1&1&1\\
p&1&-1&1&-1&1\\
1&-1&-1&q&-1&-1\\
1&-1&-1&q&1&1\\
1&-1&-1&-1&q&-1\\
1&-1&-1&1&q&1\\
1&-1&-1&-1&1&-q\\
1&-1&-1&1&-1&-q
\end{pmatrix},
\qquad |p|,|q|<1.
\]

A rank factorization \(X_9=UV\) can be chosen with

\[
V=
\begin{pmatrix}
(p-1)/2&1&0&0&0&(q+1)/2\\
-(p+1)/2&0&1&0&0&(q-1)/2\\
0&0&0&1&0&1\\
0&0&0&0&1&1
\end{pmatrix}.
\]

Hence

\[
v_0=
\frac{1-p}{2}(-v_1)+
\frac{1+p}{2}(-v_2).
\]

For \(|p|<1\), both coefficients are strictly positive and sum to one. Thus \(v_0\) lies in the relative interior of the edge \([-v_1,-v_2]\), and \(-v_0\) does likewise. The object has at most ten extreme vertices.

Therefore

\[
\boxed{12V/18F,\ c=0,\ D=9\quad\checkmark.}
\]

Combining the five layers gives

\[
\boxed{12V/18F,\ c=0\quad\checkmark.}
\]

---

## 9. Reproduction and proof status

Run

```bash
python viterbo_18f_d10_d9_verifier.py
```

The verifier regenerates the relative \(B_6\)-orbits, checks every stored integer minor certificate, recomputes the multiplicity-four finite classification, verifies the three symbolic rank families, identifies the unique nine-single orbit, and checks the primal vertex-loss identity.

All checkmarks in this note mean **computer-assisted analytic proof candidate**. The result has not undergone external peer review and is not being claimed here as a published proof of the four-dimensional conjecture.

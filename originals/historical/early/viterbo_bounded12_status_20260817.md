# Bounded-12 status after closing the 18-facet layer

**Date:** 17 August 2026  
**Problem:** four-dimensional centrally symmetric Mahler / symmetric Viterbo  
**Interpretation of ✓:** computer-assisted analytic proof candidate, not a published theorem

## 1. Current closed tree

\[
\boxed{
\begin{array}{c|c}
\text{branch}&\text{status}\\
\hline
c=1&\checkmark\\
c=0,\ 12V/12F&\checkmark\\
c=0,\ 12V/14F&\checkmark\\
c=0,\ 12V/16F&\checkmark\\
c=0,\ 12V/18F,\ D=13&\checkmark\\
c=0,\ 12V/18F,\ D=12&\checkmark\\
c=0,\ 12V/18F,\ D=11&\checkmark\\
c=0,\ 12V/18F,\ D=10&\checkmark\\
c=0,\ 12V/18F,\ D=9&\checkmark
\end{array}}
\]

Thus the entire 12-vertex, 18-facet \(c=0\) layer is now closed as a proof candidate.

The final two layers were closed by:

* exact relative \(B_6\)-orbit enumeration;
* integer sign-definite \(5\times5\) minor certificates;
* three exact rank-four survivor parameterizations;
* forced extra cube-section vertices;
* a local multiplicity-four Gale lemma for profile \((4,2,2)\);
* a unique nine-single orbit whose nominal vertex pair lies in the interior of an edge.

## 2. Transition to 20 facets

For \(12V/20F\), there are ten antipodal facet pairs. In the \(c=0\) branch every row has one or two defects, and the SWZ bound gives

\[
10\le D\le16.
\]

After triangulating the five-vertex facets without adding vertices,

\[
\boxed{g_2=34-2D}.
\]

Hence

\[
\begin{array}{c|c}
D&g_2\\
\hline
10&14\\
11&12\\
12&10\\
13&8\\
14&6\\
15&4\\
16&2
\end{array}
\]

The highest-defect layer \(D=16\) again lies in the rigid \(g_2=2\) equality class.

## 3. Exact preclassification of \(20F,D=16\)

A 12-vertex centrally symmetric simplicial 3-sphere with \(g_2=2\) is reduced to the boundary of the four-crosspolytope with two symmetric stackings. There are three relative positions for the second stacking:

1. an old facet at Hamming distance one;
2. an old facet at Hamming distance two;
3. a facet created by the first stacking.

To recover a \(20\)-facet polytope from the resulting 28 tetrahedra, four antipodal ridge pairs are merged. Only merges whose five-vertex union contains no antipodal vertex pair are admissible.

The exact matching enumeration is:

\[
\begin{array}{c|r|r|r|r}
\text{stacking type}&|\operatorname{Aut}|&\text{raw matchings}&\text{matching orbits}&\text{canonical sign templates}\\
\hline
\text{Hamming 1}&24&371&44&39\\
\text{Hamming 2}&32&457&46&37\\
\text{new facet}&12&71&19&16
\end{array}
\]

After global \(B_6\) canonicalization, the union contains

\[
\boxed{92\text{ distinct pairing sign templates}.}
\]

Exact sign-definite-minor filtering and immediate row-duplication checks give

\[
\boxed{
92
=
72\text{ rank-}\ge5
+
6\text{ duplicate facet-row templates}
+
14\text{ algebraic survivors}.
}
\]

The 14 survivor indices in the released certificate are

\[
2,17,42,76,80,81,82,85,86,87,88,89,90,91.
\]

Each has a constant nonzero \(4\times4\) pivot. The rank-four equations are therefore a 12-equation Schur-complement system in 16 defect variables. At generic numerical solutions the Jacobian rank is 12 in every case, indicating four-dimensional continuous families.

This numerical dimension statement is exploratory, not a proof certificate. Exact Gröbner bases have been computed for all 14 templates, but their strict semialgebraic branch decomposition, cube-section closure and Mahler positivity remain open.

## 4. Immediate next tasks

For each of the 14 four-parameter survivors:

1. factor the Schur-complement ideal into strict branches;
2. map each strict parameter domain to a box or simplex;
3. enumerate all 240 active cube-face charts and certify whether exactly 20 section vertices remain;
4. certify that all 12 primal candidates are extreme;
5. derive fixed primal and polar triangulations chamber by chamber;
6. express
   \[
   |P||P^\circ|-\frac{32}{3}
   \]
   as a rational polynomial and prove positivity, preferably by tensor Bernstein coefficients.

Early numerical samples for strict, correct-closure points lie above \(32/3\), but this is only evidence guiding the exact work.

## 5. Scope warning

Closing the bounded-12, 20-facet layers would still not prove the full four-dimensional conjecture. One must also close higher facet counts and complete the global reduction showing that no other 12-vertex or higher-vertex candidate remains.

The dimension-general part of the work is the shadow-rigidity bridge. The pairing-matrix, two-dimensional Gale and cube-section classifications used here are specific to dimension four.

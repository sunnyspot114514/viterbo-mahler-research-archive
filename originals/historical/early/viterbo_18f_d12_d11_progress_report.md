# 四维中心对称 Mahler / symmetric Viterbo：bounded-12 进展报告

日期：2026-08-16

## 结论摘要

本轮补齐了此前最重要的两项欠账：

1. \(12V/18F,\ c=0,\ D=12\) 的全局离散完备性已经重建并逐层复核；
2. \(12V/18F,\ c=0,\ D=11\) 的最后一个 single-profile \((2,2,2,1)\) 已关闭。

因此，当前可以把

\[
\boxed{
12V/18F,\ c=0,\ D=13,\ 12,\ 11
}
\]

全部列为 **computer-assisted analytic proof candidates**。

这里的 “proof candidate” 表示：组合枚举、精确低秩约束、section closure、primal extremality、体积公式和 Bernstein 正性已经形成闭合论证；正式投稿前仍需统一整理、固定依赖、生成可供第三方一键重放的证书包。

---

## 一、\(D=12\)：355 个 orbit 的全局完备性已恢复

\(D=12\) 有六条 single-defect rows 和三条 double-defect rows。剩余 single-direction profiles 为

\[
(4,1,1),\quad
(3,2,1),\quad
(2,2,2),\quad
(4,2).
\]

从原始 sign space 精确重建后，canonical orbit 数为

\[
59+183+78+35=355.
\]

精确分类结果：

\[
\boxed{
355
=
332\text{ 个强迫列重合/反重合}
+
20\text{ 个强迫额外 single}
+
3\text{ 个 genuine families}.
}
\]

三个 genuine families 分布为：

- \((4,1,1)\)：1 个；
- \((3,2,1)\)：2 个；
- \((2,2,2)\)、\((4,2)\)：0 个。

### 三个 genuine families 的验证

每个 family 均完成：

\[
\text{exact rank completion}
+\text{exact cube-section closure}
+\text{12 primal vertices extremality}
+\text{exact }|P|,|P^\circ|
+\text{Bernstein positivity}.
\]

\((4,1,1)\) family 的 Mahler 余量正分子在 tensor Bernstein basis 中：

\[
43>0,\qquad 37=0,\qquad 0<0,
\]

最小正系数为

\[
\frac{128}{3}.
\]

两个 \((3,2,1)\) families 分别得到：

\[
39>0,\quad11=0,\quad \min_+=\frac83,
\]

和

\[
22>0,\quad6=0,\quad \min_+=\frac{16}{3}.
\]

因此三个 family 全部满足

\[
\boxed{|P||P^\circ|>\frac{32}{3}}.
\]

所以：

\[
\boxed{12V/18F,\ c=0,\ D=12\quad\checkmark}.
\]

---

## 二、\(D=11\)：三个 single-profile 全部关闭

\(D=11\) 有七条 single-defect rows 和两条 double-defect rows。

### 1. \((4,1,1,1)\)

局部 multiplicity-four verifier 精确枚举

\[
\binom{16}{4}=1820
\]

个 projective sign 四元组：

\[
1720\text{ 个 rank }4,\qquad100\text{ 个 rank }3.
\]

rank-3 只有两个 signed-permutation orbits，均由严格三角不等式矛盾排除；rank-4 唯一能容纳三个额外 singleton directions 的 kernel 型为

\[
(0,0,0,1,1),
\]

它强迫两个 primal vertex-pairs 重合，故至多 10 个顶点。

所以：

\[
\boxed{(4,1,1,1)\quad\checkmark}.
\]

### 2. \((3,2,1,1)\)

精确 colored-orbit 分类得到：

- 16 个 colored orbits；
- 4 个 parallel cases，由 parity obstruction 排除；
- 非平行部分只留下 176 个 admissible sign combinations；
- 160 个线性不相容；
- 其余 16 个中，8 个 strict domain 为空，8 个自动多出两条 single rows。

因此不可能恰好只有七条 singles：

\[
\boxed{(3,2,1,1)\quad\checkmark}.
\]

### 3. \((2,2,2,1)\)

全局 exact orbit 数为

\[
95.
\]

精确 Gröbner / Schur 分类：

\[
\boxed{
95
=
89\text{ 个强迫列重合/反重合}
+
3\text{ 个强迫额外 single}
+
2\text{ 个丢失 primal vertex-pair}
+
1\text{ 个 genuine family}.
}
\]

两个 vertex-loss orbits 都满足固定凸组合关系

\[
v_3
=
\frac{1+x_6}{2}(-v_4)
+
\frac{1-x_6}{2}(-v_5),
\qquad |x_6|<1,
\]

所以 \(v_3\) 位于一条边的相对内部，实际至多 10 个顶点。

唯一 genuine family 可写成

\[
X=
\begin{pmatrix}
a&1&1&-1&1&1\\
b&-1&-1&1&1&1\\
1&a&1&-1&1&1\\
-1&b&-1&1&1&1\\
1&-1&c&-1&-1&1\\
-1&1&c&-1&-1&1\\
-1&-1&-1&c&-1&1
\end{pmatrix},
\qquad
c=\frac{2-a+b}{2+a-b},
\]

参数域为

\[
-1<b<a<1.
\]

它恰有七对 edge intersections 和两对 square-face intersections；六对 primal vertices 全部保持 extreme。

精确体积为

\[
|P|=
\frac{
4(a^2-2ab+10a+b^2-10b+12)
}{
3(a-b+2)
},
\]

\[
|P^\circ|=
-\frac{
a^2-ab-4a+b^2+4b-17
}{
6(a-b+2)
}.
\]

令

\[
b=2u-1,\qquad
a=2u-1+2(1-u)v,
\qquad0<u,v<1.
\]

Mahler 余量正分子的 \((4,4)\) tensor Bernstein coefficients 为

\[
\begin{pmatrix}
0&14&32&44&24\\
12&49/2&109/3&44&44\\
16&67/3&244/9&91/3&32\\
12&25/2&13&27/2&14\\
0&0&0&0&0
\end{pmatrix}.
\]

因此：

\[
19>0,\qquad6=0,\qquad0<0,
\]

最小正系数为 \(12\)，从而整个 interior 中

\[
\boxed{|P||P^\circ|>\frac{32}{3}}.
\]

于是：

\[
\boxed{(2,2,2,1)\quad\checkmark}
\]

并最终得到

\[
\boxed{12V/18F,\ c=0,\ D=11\quad\checkmark}.
\]

---

## 三、当前 bounded-12 证明树

\[
\boxed{
\begin{array}{c|c}
\text{分支}&\text{状态}\\
\hline
c=1&\checkmark\\
c=0,\ 12V/12F&\checkmark\\
c=0,\ 12V/14F&\checkmark\\
c=0,\ 12V/16F&\checkmark\\
c=0,\ 12V/18F,\ D=13&\checkmark\\
c=0,\ 12V/18F,\ D=12&\checkmark\\
c=0,\ 12V/18F,\ D=11&\checkmark\\
c=0,\ 12V/18F,\ D=10&\text{当前前沿}\\
c=0,\ 12V/18F,\ D=9&\text{待处理}
\end{array}}
\]

所有勾号均表示 **computer-assisted analytic proof candidate**，尚不是已经外部审阅、正式发表的定理。

---

## 四、\(D=10\) 的当前压缩

\(D=10\) 对应：

\[
8\text{ 条 single rows}+1\text{ 条 double row}.
\]

绝大多数八行 multiplicity partitions 已由前面七行的纯 single obstruction 继承排除：

- 六方向和五方向的宽分布由既有 rank/Gale 引理排除；
- 含 \((4,1,1,1)\) 子型的分支排除；
- 含 \((3,2,1,1)\) 子型的分支会自动产生至少九条 singles；
- \((2,2,2,2)\) 可回收到刚完成的 \((2,2,2,1)\) 分类；
- 高度集中的 \((3,3,2)\)、\((4,4)\) 已有双高 multiplicity Gale 不相容引理。

当前真正需要补成独立证书的，是少数 profile-\((4,2)\) extension strata，主要对应

\[
(4,3,1),\qquad(4,2,2).
\]

这一步尚未完成，所以目前不能把 \(D=10\) 标成勾号。

---

## 五、严格范围

这条工作线推进的是：

\[
\boxed{n=4\text{ 的中心对称 Mahler / symmetric Viterbo 情形}}
\]

中的 bounded-12 分类。

任意维 shadow-rigidity 桥可用于 \(n\ge4\)，但 pairing-matrix、二维 Gale、\(4\)-plane 切 \(6\)-cube 和 \(g_2\) 分类是四维专用部分。

即使 \(D=10,9\) 都关闭，也首先得到 \(12V/18F\) 层的完成；完整四维猜想还需要确认更高 facet 层和 bounded-12 reduction 的全局封口。

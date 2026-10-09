# Research Scope and Verification Status

Packaging date: 2026-10-07. Author attribution: GitHub [sunnyspot114514](https://github.com/sunnyspot114514), with AI assistance. The latest original-research snapshot is v61, dated 2026-09-27. Statements below describe what the archived reports claim, with their stated restrictions. They are not new mathematical validation.

## v61 two exterior point pairs in four dimensions

The proof candidate concerns exactly the family

P = conv([-1,1]^4, ±(a,u,p3,p4), ±(v,b,q3,q4)),

where a,b > 1 and u,v,p3,p4,q3,q4 lie in [-1,1]. Each pair extends beyond the cube in its own specified coordinate only. Cap overlaps are allowed. The claimed lower bound is |P||P°| >= 32/3 for this four-dimensional class. Boundary heights a=1 or b=1 are treated by continuity in the report.

The snapshot includes general-dimensional exact bridge/cap-volume formulas, a written shadow-system reduction, and twelve full-parameter polynomial certificates. Its stored finite geometry outputs cover 31 primal/polar pairs, 27 overlap regions, 27 bridge hulls, and one six-piece descent example. Those counts describe archived evidence, not computations performed during assembly. General-dimensional volume formulas do not establish the full lower-bound argument in every dimension.

The written argument uses the external Meyer–Reisner shadow-system theorem, with its source identified in the original report. It is not a Lean/Coq formalization. It does not prove the bound for arbitrary four-dimensional centrally symmetric bodies, three or more exterior pairs, points crossing two coordinate facets, arbitrary terminal-body reductions, or a complete equality classification. v61 does not embed v60 and did not rerun all earlier mathematics; the original v60 archive is retained separately.

## v60 non-bridging cube extensions in every dimension

For n >= 2, let Q_n = [-1,1]^n and let each active q_i have coordinate (q_i)_i = 1+x_i, x_i > 0, with transverse coordinates y_ij in [-1,1]. The candidate applies to P = conv(Q_n, {±q_i}) only when, for every active i<j, both conditions hold:

(1-y_ij)(1-y_ji) >= x_i x_j,

(1+y_ij)(1+y_ji) >= x_i x_j.

These pairwise conditions cannot be removed. The report claims |P||P°| >= 4^n/n! for this restricted class, a paired-coordinate saturation argument, and a four-dimensional completion of descent. The all-dimensional conclusion is a written analytic argument. Polynomial checks for n=2,...,8 are finite calibrations, not exhaustive verification in every dimension. The supplied executor has restrictions on exact square roots and does not implement arbitrary real-algebraic arithmetic.

The v60 ZIP preserves the exact recursively embedded v59 through v54 baselines. Its prior rebuild and PASS records retain their historical meaning; they were not rerun for this package.

## v33 bounded-class frontier accounting

The v33 report claims closure of the D=17, 12V/22F, c=0 frontier as a computer-assisted analytic proof candidate. Its recorded accounting is 2,395 templates, 25 exact Mahler-positive families, 31 shadow-flow nonminimal families, and zero remaining templates.

The 31 shadow classifications are local-minimizer exclusions within the bounded class. They are not pointwise lower-bound proofs for every member of those families. v33 embeds v32 only, so earlier positive-family proofs and lower-layer archives remain separate. The filename word “complete” is an original historical label and does not imply that this packaging pass independently certified a complete bounded-12 proof.

## Other retained restricted-class work

v43 concerns four-dimensional functional lifts, a lambda=1 homothetic transverse-fiber class, rectangular-prismatic families, an exact H12 test, and inherited stress/curvature work. It uses explicitly identified external theorem interfaces. General non-homothetic lambda=1 gluings, lambda=2, and an arbitrary-body bridge remained open in that snapshot.

v47 concerns restricted reflection/equipartition and chord-centering/contact constructions. v48–v53 address named radial-affine, concave-profile, parabolic, elliptic, and power-profile classes under their stated legal-midpoint assumptions. They do not establish unrestricted four-dimensional Mahler or a general centering/equipartition result. Read each original report for its precise hypotheses and external theorem inputs.

## Missing early material and replay limits

- The August 16 recovery notes identify a finite generator for 355 canonical representatives and source/representative data for 332 duplicate-column certificates. Those files were not located in the retrieved early-source set. A recovered manifest cannot replace regeneration.
- Full underlying source and certificates for earlier c=1 / 12V12F / 12V14F / 12V16F closures were not resolved. Summaries of closure status do not establish complete standalone replay packages.
- Historical scripts and rebuild instructions can depend on absolute paths or their original runtime. No refactor or portable end-to-end replay test was performed.
- The retained original archives contain four unique compiled Python cache files. They are historical bytes, were not executed, and should not be treated as preferred source artifacts.

Consequently this archive should be cited as research artifacts and restricted-class proof candidates, not an independently certified complete bounded-12 proof or a complete general Viterbo/Mahler proof.

## October 7 external review

The separate archive in external-review/ concerns OpenAI's openai/math Family 087 at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. The archived review leans toward validity of the symmetric polar-product main proof chain. It did not perform a full Lean/Comparator replay, a complete transitive dependency-axiom scan, the non-symmetric Mahler proof, or a complete Hanner equality classification. Its local finite diagnostics are not a universal proof. This review does not retrospectively certify sunnyspot114514's earlier work or establish priority.

## What was checked for this package

All 60 selected original files were checked against the recorded sizes and SHA-256 hashes and copied unchanged. The 15 browsable v61 files were safely extracted without executing code, compared to their original ZIP bytes, and checked against the 12 hashed entries of the original v61 manifest. The final outer ZIP and its public file inventory were checked for byte integrity.

Earlier read-only inventory checks recorded matching manifest payloads for v61, v60, v33, v43, v47, and the October 7 audit. Those are file-integrity results, not mathematical correctness checks. The earlier heuristic text screen found no obvious credentials or unrelated personal data; it is not a security guarantee. No mathematical verifier, independent proof review, new formalization, or literature-priority assessment was performed during assembly.

Dates and older open/complete/PASS statements inside originals are preserved historical claims about those snapshots. The qualifications in this document govern how this newly assembled archive should be presented.

## 中文状态摘要

最新原始研究为 v61（2026-09-27），不是 2026-10-07 的外部审读包。v61 的命题仅覆盖四维立方体加两对外点：q=(a,u,p3,p4)、r=(v,b,q3,q4)，a,b>1，其余六个坐标均在 [-1,1]。允许帽交叠，候选下界为 32/3。一般维数的体积公式不等于一般维数下界证明。十二项全参数多项式证书、31 组原体/极体、27 个交叠区域、27 个桥区及六段下降实例均是原档案记录，本次没有重算。

v60 的全维候选下界 4^n/n! 以每个活跃配对的两条条件同时成立为前提：(1-y_ij)(1-y_ji)>=x_i x_j 及 (1+y_ij)(1+y_ji)>=x_i x_j。不能删去非桥接条件。n=2 至 8 的有限校准不构成全维穷尽验证。

v33 的 D=17、12V/22F、c=0 记录为 2395 模板、25 个精确正族、31 个 shadow-flow 非极小族、剩余 0。31 项 shadow 结论是受限类别内的局部极小排除，不是对每个族成员的逐点下界。历史文件名中的 complete 和内容中的 PASS 保留原日期含义，不代表本次独立认证。

早期 355 个代表的有限生成器、332 个重复列证书的源数据，以及更早 c=1 / 12V12F / 12V14F / 12V16F 闭合所需的完整底层证书未补齐。部分旧重放流程依赖原运行环境。本包未重构源码，也未验证一键全程重放。

2026-10-07 审读包单独放在 external-review/，针对 OpenAI 的特定提交；其判断和有限诊断不是完整 Lean/Comparator 认证，也不追认早期局部工作为一般猜想证明或优先权证据。本次确认的是原文件字节、大小、哈希和归档结构，没有重新运行数学验证器或完成独立同行评审。

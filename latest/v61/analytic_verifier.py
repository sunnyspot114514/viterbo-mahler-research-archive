#!/usr/bin/env python3
"""Recompute the complete finite algebra for the two-pair 4D theorem.

Uses exact SymPy arithmetic. The shadow theorem and the geometric volume
partition are written analytic inputs, not formalized by this program.
"""
from __future__ import annotations
import argparse, json
from itertools import product
from math import comb
from pathlib import Path
import sympy as S


def overlap_normalized(a,b,u,v,k,active=True):
    """2*directed overlap / (2^4/4!), after transverse corner saturation."""
    if not active:
        return S.S(0)
    delta=(a-1)*(b-1)-(1-u)*(1-v)
    det=a*b-u*v
    A,B=a-u,b-v
    X=delta*(2*det-delta)
    Y=(delta+2*A)*(delta+2*B)
    return S.cancel(delta**4*det/(2*A*B*X**k*Y**(2-k)))


def terminal_ratio(x,y,u,v,k,flags):
    a,b=x+1,y+1
    dp=x*y-(1-u)*(1-v);dm=x*y-(1+u)*(1+v)
    V=16+4*(x+y)+S.Rational(2,3)*((dp if flags[0] else 0)+(dm if flags[1] else 0))
    Sq=x*x*a*a/((a*a-u*u)*(x+2)**2)
    Sr=y*y*b*b/((b*b-v*v)*(y+2)**2)
    W=1-Sq-Sr+overlap_normalized(a,b,u,v,k,flags[0])+overlap_normalized(a,b,-u,-v,2-k,flags[1])
    return S.factor(V*W/16-1)


def ordinary_positive(poly, variables):
    P=S.Poly(poly,*variables)
    coefficients=P.coeffs()
    assert coefficients and all(bool(c>0) for c in coefficients)
    return dict(basis='ordinary monomials',variables=list(map(str,variables)),
                degrees=list(P.degree_list()),positive=len(coefficients),zero=0,
                minimum_positive=str(min(coefficients)),
                terms=[dict(powers=list(m),coefficient=str(c)) for m,c in P.terms()])


def mixed_certificate(poly, bounded, unbounded):
    """Tensor Bernstein on [0,1] for bounded; monomials for nonnegative rest.

    Includes every slot in the tensor rectangle; independently reconstructs
    each coefficient polynomial in the unbounded variables.
    """
    variables=bounded+unbounded
    P=S.Poly(poly,*variables)
    degrees=tuple(P.degree(v) for v in variables)
    bdeg=degrees[:len(bounded)];udeg=degrees[len(bounded):]
    terms=P.terms();records=[];positive=zero=0;minimum=None
    for up in product(*(range(d+1) for d in udeg)):
        selected=[(powers[:len(bounded)],c) for powers,c in terms if powers[len(bounded):]==up]
        reconstructed=0
        original=sum(c*S.prod(v**e for v,e in zip(bounded,powers)) for powers,c in selected)
        for bp in product(*(range(d+1) for d in bdeg)):
            c=S.S(0)
            for powers,a in selected:
                if all(e<=i for e,i in zip(powers,bp)):
                    c+=a*S.prod(S.Rational(comb(i,e),comb(d,e)) for i,e,d in zip(bp,powers,bdeg))
            assert bool(c>=0), ('negative certificate coefficient',bp,up,c)
            if c:
                positive+=1;minimum=c if minimum is None else min(minimum,c)
            else:zero+=1
            basis=S.prod(comb(d,i)*v**i*(1-v)**(d-i) for v,i,d in zip(bounded,bp,bdeg))
            reconstructed+=c*basis
            records.append(dict(bernstein_indices=list(bp),monomial_powers=list(up),coefficient=str(c)))
        assert S.expand(reconstructed-original)==0
    return dict(basis='Bernstein x nonnegative monomials',
                bounded=list(map(str,bounded)),unbounded=list(map(str,unbounded)),
                degrees=list(degrees),positive=positive,zero=zero,
                minimum_positive=str(minimum),coefficients=records,
                reverse_reconstruction=True)


def denominator_positive(den, variables):
    P=S.Poly(den,*variables)
    assert all(bool(c>0) for c in P.coeffs())
    return str(S.factor(den))


def compute():
    x,y=S.symbols('x y',positive=True)
    t,d=S.symbols('t d',nonnegative=True)
    cases=[]
    # First terminal type: a corner of (u,v) in [-1,1]^2.
    # Simultaneous sign flips and swapping the coordinate pairs leave just
    # (1,-1) and (1,1). All three transverse sign counts are retained.
    for k in range(3):
        f=terminal_ratio(x,y,S.S(1),S.S(-1),k,(True,True))
        N,D=S.fraction(f)
        cases.append(dict(name=f'opposed_corner_k{k}',
            ratio_minus_one=str(f),positive_denominator=denominator_positive(D,(x,y)),
            certificate=ordinary_positive(N,(x,y))))
        f=terminal_ratio(x,y,S.S(1),S.S(1),k,(True,False))
        N,D=S.fraction(f)
        den_info=denominator_positive(D,(x,y))
        mapped=S.factor(f.subs(y,4*t/x));Nm,Dm=S.fraction(mapped)
        cases.append(dict(name=f'same_corner_one_overlap_k{k}',
            substitution='y=4*t/x, x>0, 0<t<=1',ratio_minus_one=str(f),
            positive_denominator=den_info,mapped_denominator=str(S.factor(Dm)),
            certificate=mixed_certificate(Nm,(t,),(x,))))
        f=terminal_ratio(x,y,S.S(1),S.S(1),k,(True,True))
        N,D=S.fraction(f)
        den_info=denominator_positive(D,(x,y))
        mapped=S.factor(f.subs(y,(4+d)/x));Nm,Dm=S.fraction(mapped)
        cases.append(dict(name=f'same_corner_two_overlaps_k{k}',
            substitution='y=(4+d)/x, x>0, d>=0',ratio_minus_one=str(f),
            positive_denominator=den_info,mapped_denominator=str(S.factor(Dm)),
            certificate=ordinary_positive(Nm,(x,d))))
    # The two corner chambers agree exactly at their common boundary.
    for k in range(3):
        one=terminal_ratio(x,y,S.S(1),S.S(1),k,(True,False))
        both=terminal_ratio(x,y,S.S(1),S.S(1),k,(True,True))
        assert S.factor((one-both).subs(y,4/x))==0
    # Second terminal type: one cap pair exactly touches and the other overlaps.
    # (1+u)(1+v)=xy. p=1+u, q=1+v, p+q>=2, 0<p,q<=2.
    p,q,z=S.symbols('p q z',positive=True)
    r,s=S.symbols('r s',nonnegative=True)
    for k in range(3):
        f=terminal_ratio(p*z,q/z,p-1,q-1,k,(True,False))
        N,D=S.fraction(f)
        den_info=denominator_positive(D,(p,q,z))
        mapped=S.expand(N.subs({p:2*r,q:2*(1-r+r*s)}))
        cases.append(dict(name=f'touch_wall_k{k}',
            substitution='p=2*r, q=2*(1-r+r*s), x=p*z, y=q/z; 0<r<=1,0<=s<=1,z>0,q>0',
            ratio_minus_one=str(f),positive_denominator=den_info,
            certificate=mixed_certificate(mapped,(r,s),(z,))))
    # Direct non-overlap subcase. This is rederived, not inherited as PASS.
    G=4+3*(x+y)+2*x*y
    Dx=(x+y+2)*(x+2)**2;Dy=(x+y+2)*(y+2)**2
    bound=(4+x+y)/4*(1-x*(x+1)**2/Dx-y*(y+1)**2/Dy)
    margin=G*(x/Dx+y/Dy)/4
    assert S.factor(bound-1-margin)==0
    # Oriented bridge determinant.
    a,b,u,v,xi,eta,w,h1,h2,T,c1,c2=S.symbols('a b u v xi eta w h1 h2 T c1 c2')
    delta=(a-1)*(b-1)-(1-u)*(1-v)
    determinant=S.det(S.Matrix([[a-1,v-1],[u-1,b-1]]))
    assert S.expand(determinant-delta)==0
    # One-transverse-variable version of the general cap change of variables.
    # The same identity adds each remaining transverse coordinate linearly.
    D=a*b-u*v;A=a-u;B=b-v
    slack1=a*xi+u*eta+c1*T-1
    slack2=v*xi+b*eta+c2*T-1
    leftover=1-xi-eta-T
    assert S.expand(D*leftover+B*slack1+A*slack2+(D-B*c1-A*c2)*T-delta)==0
    assert S.det(S.Matrix([[S.diff(slack1,xi),S.diff(slack1,eta)],
                                [S.diff(slack2,xi),S.diff(slack2,eta)]]))==D
    # A slab where the old formula is definitely invalid.
    from overlap_formula import volumes
    axial=volumes((3,0,0,0),(0,3,0,0))
    assert axial['primal']==36 and axial['polar']==S.Rational(100,243)
    assert axial['primal_bridge']==4 and axial['polar_overlap_correction']==S.Rational(2,243)
    def convert(o):
        from fractions import Fraction
        if isinstance(o,Fraction):return str(o)
        if isinstance(o,dict):return {k:convert(v) for k,v in o.items()}
        if isinstance(o,list):return list(map(convert,o))
        return o
    return dict(status='PASS',version='v61',
        theorem_scope='4D cube plus two antipodal pairs protruding in distinct coordinate directions',
        complete_terminal_cases=len(cases),
        positive_coefficients=sum(c['certificate']['positive'] for c in cases),
        zero_coefficients=sum(c['certificate']['zero'] for c in cases),
        negative_coefficients=0,cases=cases,
        nonoverlap_margin_identity=str(margin),
        bridge_determinant_verified=True,cap_change_of_variables_verified=True,
        axial_overlap_calibration=convert(axial),
        general_four_dimensional_Mahler_proved=False,
        three_or_more_external_pairs_proved=False,
        external_shadow_theorem_formalized=False,
        geometric_partition_formalized=False)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='analytic_certificate.json')
    args=parser.parse_args();result=compute()
    Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','complete_terminal_cases','positive_coefficients','zero_coefficients','negative_coefficients']},sort_keys=True))

if __name__=='__main__':main()

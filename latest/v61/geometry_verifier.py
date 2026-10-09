#!/usr/bin/env python3
"""Independent rational geometry for the v61 overlap formula and reductions."""
from __future__ import annotations
import argparse,json
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import sympy as S
import exact_geometry as eg
from overlap_formula import volumes
from descent import build_path


def centered_volume(poly):
    vs=poly['vertices'];n=poly['dimension']
    center=tuple(sum(p[j] for p in vs)/len(vs) for j in range(n))
    shifted=dict(poly)
    shifted['vertices']=[tuple(x-y for x,y in zip(p,center)) for p in vs]
    return eg.volume_moment(shifted)[0]


def arbitrary_hull_volume(points):
    pts=sorted(set(tuple(map(F,p)) for p in points));n=len(pts[0])
    if eg.affine_rank(pts)!=n:raise AssertionError('Bridge is not full-dimensional')
    center=tuple(sum(p[j] for p in pts)/len(pts) for j in range(n))
    shifted=[tuple(x-y for x,y in zip(p,center)) for p in pts]
    dual=eg.hpoly([(p,F(1)) for p in shifted],n)
    true=[p for p in shifted if eg.rank([v for v in dual['vertices'] if eg.dot(p,v)==1])==n]
    faces=[frozenset(i for i,p in enumerate(true) if eg.dot(p,v)==1) for v in dual['vertices']]
    body=dict(vertices=true,facets=sorted(set(faces),key=lambda f:tuple(sorted(f))),dimension=n)
    return eg.volume_moment(body)[0]


def geometry(q,r,name,check_local=True,double_dual=False):
    q,r=tuple(map(F,q)),tuple(map(F,r));n=len(q)
    corners=[tuple(map(F,e)) for e in product((-1,1),repeat=n)]
    cloud=corners+[q,tuple(-v for v in q),r,tuple(-v for v in r)]
    P,K=eg.central_pair(cloud)
    V,_,VP=eg.volume_moment(P);W,_,WK=eg.volume_moment(K)
    formula=volumes(q,r)
    assert V==formula['primal'] and W==formula['polar'],(name,V,W,formula)
    if n==4:assert V*W>=F(32,3)
    out=dict(name=name,q=q,r=r,dimension=n,vertices=len(P['vertices']),facets=len(P['facets']),
             primal_volume=V,polar_volume=W,product=V*W,
             primal_triangulation=VP,polar_triangulation=WK,
             polar_bases_enumerated=K['bases_enumerated'],formula=formula)
    if double_dual:
        reconstructed=eg.hpoly([(p,F(1)) for p in K['vertices']],n)
        assert reconstructed['vertices']==P['vertices']
        out['double_dual_bases']=reconstructed['bases_enumerated']
    local=[]
    if check_local:
        for sign,key,delta_name in ((1,'overlap_plus','delta_plus'),(-1,'overlap_minus','delta_minus')):
            delta=formula[delta_name]
            if delta<=0:continue
            hs=[(p,F(1)) for p in corners]+[(tuple(-v for v in q),F(-1)),(tuple(-sign*v for v in r),F(-1))]
            inter=eg.hpoly(hs,n);iv=centered_volume(inter)
            assert iv==formula[key]
            ridge=[(F(1),F(sign))+tuple(map(F,t)) for t in product((-1,1),repeat=n-2)]
            bridge=arbitrary_hull_volume(ridge+[q,tuple(sign*v for v in r)])
            expected_bridge=F(2**(n-2),n*(n-1))*delta
            assert bridge==expected_bridge
            local.append(dict(sign=sign,overlap_volume=iv,
                overlap_vertices=len(inter['vertices']),overlap_bases=inter['bases_enumerated'],
                bridge_volume=bridge))
        assert 2*sum(a['bridge_volume'] for a in local)==formula['primal_bridge']
        assert 2*sum(a['overlap_volume'] for a in local)==formula['polar_overlap_correction']
    out['local_corrections']=local
    return out,P


def symmetry_certificate(P):
    verts=P['vertices'];reps=[]
    for p in verts:
        if next(x for x in p if x)>0:reps.append(p)
    M=S.zeros(4)
    for p in verts:
        v=S.Matrix([S.Rational(x.numerator,x.denominator) for x in p]);M+=v*v.T
    inv=M.inv();gram=[]
    vectors=[S.Matrix([S.Rational(x.numerator,x.denominator) for x in p]) for p in reps]
    for v in vectors:gram.append([(v.T*inv*w)[0] for w in vectors])
    diag=[gram[i][i] for i in range(len(reps))]
    assert len(set(diag))==len(diag)
    assert all(gram[i][j]!=0 for i in range(len(reps)) for j in range(i))
    return dict(group='I and -I',representatives=reps,
                diagonal_invariants=list(map(str,diag)),gram=[[str(x) for x in row] for row in gram],
                proof='Distinct diagonal invariants fix each vertex line; nonzero cross terms force a common sign.')


def compute():
    records=[];cache={}
    def add(q,r,name,local=True,double=False):
        key=(tuple(map(F,q)),tuple(map(F,r)))
        if key in cache:return cache[key]
        record,P=geometry(q,r,name,local,double)
        cache[key]=(record,P);records.append(record)
        return record,P
    q0=(F(5,2),F(1,2),F(1,3),F(-2,5))
    r0=(F(2,3),F(7,3),F(-1,4),F(3,5))
    initial,P0=add(q0,r0,'generic asymmetric one-overlap input',True,True)
    sym=symmetry_certificate(P0)
    path=build_path(q0,r0)
    for i,step in enumerate(path['steps'],1):
        end,_=add(step['q_after'],step['r_after'],f'path end {i}',False,i==len(path['steps']))
        mid,_=add(step['q_mid'],step['r_mid'],f'path midpoint {i}',False,False)
        assert end['product']==step['product_after'] and mid['product']==step['product_mid']
    # Three transverse sign configurations at each algebraic boundary type.
    for k,trans in enumerate(((-1,-1),(1,-1),(1,1))):
        for label,a,b,u,v in [
          ('opposed corner',F(2),F(3),F(1),F(-1)),
          ('same corner one overlap',F(2),F(3),F(1),F(1)),
          ('same corner two overlaps',F(3),F(4),F(1),F(1)),
          ('touch wall',F(3),F(19,10),F(1,2),F(1,5))]:
            add((a,u,1,1),(v,b,*trans),f'{label}, k={k}',True,False)
    add((3,0,0,0),(0,3,0,0),'axial calibration from v60',True,False)
    add((4,F(-3,4),-1,F(1,2)),(F(4,5),2,F(1,4),-1),'generic two-overlap input',True,False)
    add((F(3,2),0,F(1,2),F(1,3)),(0,F(3,2),F(-1,4),F(2,5)),'nonoverlap input',True,False)
    add((2,0,F(1,3),F(-1,4)),(0,2,F(2,5),F(1,7)),'simultaneous zero overlap boundary',True,False)
    # General-dimensional formulas cross-checked in dimensions two and three.
    add((F(5,2),F(1,2)),(F(1,4),F(7,3)),'dimension two overlap',True,False)
    add((F(5,2),F(1,2),F(-1,3)),(F(1,4),F(7,3),F(2,5)),'dimension three overlap',True,False)
    return dict(status='PASS',version='v61',
        independently_reconstructed_pairs=len(records),
        dimension_counts={str(n):sum(r['dimension']==n for r in records) for n in (2,3,4)},
        independent_cap_intersections=sum(len(r['local_corrections']) for r in records),
        independent_bridge_hulls=sum(len(r['local_corrections']) for r in records),
        double_dual_reconstructions=sum('double_dual_bases' in r for r in records),
        monotone_path_segments=len(path['steps']),
        whole_segment_bernstein_certificates=2*len(path['steps']),
        initial_automorphism_certificate=sym,path=path,records=records,
        general_four_dimensional_Mahler_proved=False,
        all_dimensions_two_pair_Mahler_proved=False,
        finite_geometry_used_as_universal_sampling_proof=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='geometry_certificate.json');a=p.parse_args()
    result=compute()
    Path(a.output).write_text(json.dumps(eg.jsonable(result),sort_keys=True,indent=2)+'\n')
    keys=['status','independently_reconstructed_pairs','dimension_counts','independent_cap_intersections',
          'independent_bridge_hulls','double_dual_reconstructions','monotone_path_segments','whole_segment_bernstein_certificates']
    print(json.dumps({k:result[k] for k in keys},sort_keys=True))

if __name__=='__main__':main()

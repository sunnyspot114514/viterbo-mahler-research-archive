"""Small exhaustive rational polytope routines (dimensions 2--4).

No floating point hull, random search, or external geometry package is used.
H-to-V enumerates every independent d-subset of the supplied halfspaces.
Volumes use a face-lattice pulling triangulation and cones from the origin.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
from math import factorial, gcd, lcm
from functools import reduce, lru_cache


def dot(a, b):
    return sum(x*y for x, y in zip(a,b))


def determinant(a):
    n = len(a)
    if n == 0: return 1
    if n == 1: return a[0][0]
    if n == 2: return a[0][0]*a[1][1]-a[0][1]*a[1][0]
    if n == 3:
        (a,b,c),(d,e,f),(g,h,i) = a
        return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
    # Integer fraction-free elimination; also works over Fraction.
    b = [list(r) for r in a]; sign=1; old=1
    for k in range(n-1):
        if b[k][k] == 0:
            p = next((i for i in range(k+1,n) if b[i][k]),None)
            if p is None:return 0
            b[k],b[p]=b[p],b[k];sign=-sign
        pivot=b[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=b[i][j]*pivot-b[i][k]*b[k][j]
                b[i][j]=v//old if isinstance(v,int) and isinstance(old,int) else v/old
            b[i][k]=0
        old=pivot
    return sign*b[-1][-1]


def rank(rows):
    if not rows:return 0
    a=[list(map(F,r)) for r in rows]; n=len(a[0]);r=0
    for j in range(n):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];p=a[r][j]
        a[r]=[v/p for v in a[r]]
        for k in range(r+1,len(a)):
            p=a[k][j]
            if p:a[k]=[x-p*y for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r


def affine_rank(points):
    if not points:return -1
    p=points[0]
    return rank([tuple(x-y for x,y in zip(q,p)) for q in points[1:]])


def integer_row(row):
    row=tuple(map(F,row));den=lcm(*(v.denominator for v in row))
    z=tuple(int(v*den) for v in row)
    g=reduce(gcd,(abs(v) for v in z),0)
    return tuple(v//g for v in z) if g else z


def hpoly(halfspaces, dimension=None):
    """Return all vertices/facets of a bounded full-dimensional H-polytope.

    Each row is (normal, bound), expressing normal.x <= bound.
    Origin may be on the boundary. Nonempty full dimension is checked.
    """
    rows=sorted(set(integer_row(tuple(a)+(b,)) for a,b in halfspaces))
    d=dimension or len(rows[0])-1
    if not 1<=d<=4:raise ValueError('Supported dimensions are 1--4')
    verts=set(); checked=0; feasible_bases=0
    for inds in combinations(range(len(rows)),d):
        rr=[rows[i] for i in inds]; A=[r[:d] for r in rr]; b=[r[d] for r in rr]
        den=determinant(A);checked+=1
        if not den:continue
        num=[]
        for j in range(d):
            mat=[list(r) for r in A]
            for i in range(d):mat[i][j]=b[i]
            num.append(determinant(mat))
        if den<0:den=-den;num=[-v for v in num]
        if any(dot(r[:d],num)>r[d]*den for r in rows):continue
        feasible_bases+=1
        verts.add(tuple(F(v,den) for v in num))
    verts=sorted(verts)
    if affine_rank(verts)!=d:raise ValueError('Not a full-dimensional bounded vertex hull')
    # The uses in this package all have an independently bounded H-system.
    facets=set()
    for r in rows:
        face=frozenset(i for i,p in enumerate(verts) if dot(r[:d],p)==r[d])
        if len(face)>=d and affine_rank([verts[i] for i in sorted(face)])==d-1:
            facets.add(face)
    return {'vertices':verts,'facets':sorted(facets,key=lambda f:tuple(sorted(f))),
            'dimension':d,'halfspaces':rows,'bases_enumerated':checked,
            'feasible_bases':feasible_bases}


def central_pair(points):
    """Exhaustively construct P and its polar from a centrally symmetric cloud."""
    pts=sorted(set(tuple(map(F,p)) for p in points));d=len(pts[0])
    cloud=set(pts)
    if any(tuple(-x for x in p) not in cloud for p in pts):
        raise ValueError('Point cloud must be origin symmetric')
    if rank(pts)!=d:raise ValueError('Point cloud does not span ambient space')
    polar=hpoly([(p,F(1)) for p in pts],d)
    # A cloud point is a vertex iff its active polar normals span dimension d.
    true=[]
    for p in pts:
        active=[n for n in polar['vertices'] if dot(p,n)==1]
        if rank(active)==d:true.append(p)
    faces=[]
    for n in polar['vertices']:
        f=frozenset(i for i,p in enumerate(true) if dot(p,n)==1)
        if affine_rank([true[i] for i in sorted(f)])!=d-1:raise AssertionError('Dual facet mismatch')
        faces.append(f)
    primal={'vertices':true,'facets':sorted(set(faces),key=lambda f:tuple(sorted(f))),
            'dimension':d,'cloud_size':len(pts)}
    return primal,polar


def boundary_simplices(poly):
    verts=poly['vertices'];facets=tuple(poly['facets']);d=poly['dimension']
    @lru_cache(None)
    def pull(face):
        if len(face)==1:return [(next(iter(face)),)]
        intersections=set(face & f for f in facets)
        intersections.discard(face);intersections.discard(frozenset())
        sub=[s for s in intersections if not any(s<t for t in intersections)]
        anchor=min(face);simp=[]
        for s in sorted(sub,key=lambda f:tuple(sorted(f))):
            if anchor not in s:
                simp.extend((anchor,)+v for v in pull(s))
        return simp
    result=[]
    for face in facets:
        simplices=pull(face)
        if not simplices or any(len(t)!=d for t in simplices):
            raise AssertionError('Invalid pulling triangulation dimension')
        result.extend(simplices)
    # Facewise pulling with the same global vertex order is coherent.
    incidence={}
    for simplex in result:
        for ridge in combinations(simplex,d-1):
            ridge=tuple(sorted(ridge));incidence[ridge]=incidence.get(ridge,0)+1
    if any(v!=2 for v in incidence.values()):raise AssertionError('Boundary is not a closed simplicial pseudomanifold')
    return result


def volume_moment(poly, moment_coordinate=None):
    verts=poly['vertices'];d=poly['dimension'];simp=boundary_simplices(poly)
    # In this package 0 belongs to every body, possibly its boundary after clipping.
    volume=F(0);moment=F(0);nonzero=0
    for ids in simp:
        ps=[verts[i] for i in ids]
        v=abs(determinant(ps))/factorial(d)
        volume+=v
        if v:nonzero+=1
        if moment_coordinate is not None:
            moment+=v*sum(p[moment_coordinate] for p in ps)/(d+1)
    return volume,moment,{'boundary_simplices':len(simp),'nonzero_origin_cones':nonzero}


def hull2(points):
    ps=sorted(set(tuple(map(F,p)) for p in points))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lower=[]
    for p in ps:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(ps):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    out=lower[:-1]+upper[:-1]
    if len(out)<3:raise ValueError('Degenerate polygon')
    return out


def area2(poly):
    return abs(sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1])))/2


def jsonable(obj):
    if isinstance(obj,F):return str(obj)
    if isinstance(obj,(list,tuple)):return [jsonable(x) for x in obj]
    if isinstance(obj,(set,frozenset)):return [jsonable(x) for x in sorted(obj)]
    if isinstance(obj,dict):return {str(k):jsonable(v) for k,v in obj.items()}
    return obj

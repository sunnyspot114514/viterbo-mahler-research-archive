"""Deterministic derivative-directed one-coordinate reductions for two pairs.

It ends at a certified algebraic boundary, not necessarily a Mahler equality
body. At most four transverse and two mutual-coordinate moves in dimension 4.
"""
from fractions import Fraction as F
import sympy as S
from math import factorial
from overlap_formula import volumes


def _sym(x):
    return S.Rational(x.numerator,x.denominator) if isinstance(x,F) else S.sympify(x)


def symbolic_product(q,r,flags):
    q=list(map(_sym,q));r=list(map(_sym,r));n=len(q)
    a,u,v,b=q[0],q[1],r[0],r[1];x,y=a-1,b-1
    dp=x*y-(1-u)*(1-v);dm=x*y-(1+u)*(1+v)
    V=S.Rational(2**n,n)*(n+x+y)+S.Rational(2**(n-1),n*(n-1))*((dp if flags[0] else 0)+(dm if flags[1] else 0))
    W0=S.Rational(2**n,factorial(n))
    singles=[]
    for i,p in enumerate((q,r)):
        ai=p[i];xi=ai-1
        singles.append(W0*xi**n*ai**(n-2)/S.prod(ai*ai-p[j]*p[j] for j in range(n) if j!=i))
    def ov(q,r,active):
        if not active:return S.S(0)
        a,u,v,b=q[0],q[1],r[0],r[1]
        D=a*b-u*v;A=a-u;B=b-v;delta=(a-1)*(b-1)-(1-u)*(1-v)
        return S.Rational(2**(n-2),factorial(n))*delta**n*D**(n-3)/(A*B*S.prod(D*D-(B*q[j]+A*r[j])**2 for j in range(2,n)))
    qm=[-v if j==1 else v for j,v in enumerate(q)]
    rm=[v if j==1 else -v for j,v in enumerate(r)]
    W=W0-sum(singles)+2*(ov(q,r,flags[0])+ov(qm,rm,flags[1]))
    return S.cancel(V*W)


def build_path(q,r):
    q=list(map(F,q));r=list(map(F,r));n=len(q)
    if n!=4:raise ValueError('This packaged path executor is four-dimensional')
    steps=[]
    def move(which,j,mutual=False):
        nonlocal q,r
        current=(q if which==0 else r)[j]
        if abs(current)==1:return
        rec=volumes(q,r)
        flags=(rec['delta_plus']>0,rec['delta_minus']>0)
        if mutual:
            if rec['delta_plus']==0 or rec['delta_minus']==0:return
            other=r[0] if which==0 else q[1]
            c=(q[0]-1)*(r[1]-1)
            cuts=[F(-1),F(1)]
            if other!=1:cuts.append(1-c/(1-other))
            if other!=-1:cuts.append(c/(1+other)-1)
            cuts=sorted(set(x for x in cuts if -1<=x<=1))
            lo=max(x for x in cuts if x<current);hi=min(x for x in cuts if x>current)
        else:lo,hi=F(-1),F(1)
        t=S.Symbol('t',real=True)
        qs=list(q);rs=list(r);(qs if which==0 else rs)[j]=t
        expression=symbolic_product(qs,rs,flags)
        derivative=S.cancel(S.diff(expression,t).subs(t,_sym(current)))
        derivative=F(int(derivative.p),int(derivative.q))
        endpoint=lo if derivative>0 else hi
        newq=list(q);newr=list(r);(newq if which==0 else newr)[j]=endpoint
        ending=volumes(newq,newr)
        assert ending['product']<=rec['product']
        lam=S.Symbol('s',real=True)
        path_expr=S.cancel(expression.subs(t,_sym(current)+(endpoint-current)*lam))
        N,D=S.fraction(path_expr)
        if D.subs(lam,S.Rational(1,2))<0:N,D=-N,-D
        assert D.subs(lam,0)>0 and D.subs(lam,1)>0
        neg_derivative=S.expand(N*S.diff(D,lam)-S.diff(N,lam)*D)
        from analytic_verifier import mixed_certificate
        # This optional example-specific certificate is stronger than midpoint sampling.
        den_cert=mixed_certificate(S.expand(D),(lam,),())
        der_cert=mixed_certificate(neg_derivative,(lam,),())
        middleq=[(a+b)/2 for a,b in zip(q,newq)]
        middler=[(a+b)/2 for a,b in zip(r,newr)]
        mid=volumes(middleq,middler)
        assert rec['primal']+ending['primal']==2*mid['primal']
        assert rec['product']>=mid['product']>=ending['product']
        steps.append(dict(which_vector=which,coordinate=j,start=q[:] if which==0 else r[:],
                          q_before=q[:],r_before=r[:],q_after=newq[:],r_after=newr[:],
                          interval=[lo,hi],selected_endpoint=endpoint,
                          initial_product_derivative=derivative,
                          product_before=rec['product'],product_after=ending['product'],
                          q_mid=middleq,r_mid=middler,product_mid=mid['product'],
                          constant_primal_volume=not mutual,primal_volume_affine=True,
                          exact_product_along_segment=str(path_expr),
                          denominator_certificate=den_cert,
                          nonpositive_derivative_certificate=der_cert))
        q,r=newq,newr
    for which in (0,1):
        for j in (2,3):move(which,j)
    for which,j in ((0,1),(1,0)):
        rec=volumes(q,r)
        if rec['delta_plus']==0 or rec['delta_minus']==0:break
        move(which,j,True)
    rec=volumes(q,r)
    if rec['delta_plus']<=0 and rec['delta_minus']<=0:kind='nonoverlap boundary'
    elif rec['delta_plus']==0 or rec['delta_minus']==0:kind='one touching cap pair, other overlapping'
    elif abs(q[1])==1 and abs(r[0])==1:kind='mutual-coordinate corner'
    else:raise AssertionError('Not a certified terminal type')
    assert len(steps)<=6
    return dict(steps=steps,q_terminal=q,r_terminal=r,terminal_kind=kind,
                terminal_product=rec['product'],terminates_at_equality_not_claimed=True)

if __name__=='__main__':
    p=build_path((F(5,2),F(1,2),F(1,3),F(-2,5)),
                 (F(2,3),F(7,3),F(-1,4),F(3,5)))
    for i,step in enumerate(p['steps']):
        print(i+1,step['which_vector'],step['coordinate'],step['selected_endpoint'],
              'M',step['product_after'],float(step['product_after']),flush=True)
    print('TERMINAL',p['terminal_kind'],p['q_terminal'],p['r_terminal'])

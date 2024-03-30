#============================================#
# UE Calculabilite L3                        #
# TME GHC propres                            #
# Mathieu.Jaume@lip6.fr                      #
#============================================#

from ensembles import *
from ghc import *

# Symboles annulables
# -------------------

def canc0(r):
    # r : liste de productions
    def is_empty_list(l):
        return len(l)==0
    return [s for s,ls in r if exists_such_that(ls,is_empty_list)]

def next_canc(r,eqnt,prev):
    # r : liste de productions
    # eqnt : egalite sur les non terminaux
    # prev : liste de non terminaux de depart
    res = prev
    for (x,rp) in r :
        for u in rp :
            if u ==[] :
                res = ajout(eq_atom, x, res)
                continue
            vrai = 1
            for elem in u :
                if elem not in prev :
                    vrai = 0
            if vrai == 1:
                res = ajout(eq_atom, x, res)

    return res

def canc(r,eqnt):
    # r : liste de productions
    # eqnt : egalite sur les non terminaux
    def _next_canc(e):
        return next_canc(r,eqnt,e)
    return fixpoint_from(make_eq_set(eqnt),_next_canc,canc0(r))

# Elimination des epsilon-productions
# -----------------------------------

def remove_eps_prod(g):
    # g : ghc
    nt,t,r,si,eqnt = g
    canc_g = canc(r,eqnt)
    def make_new_prod(l):
        if len(l)==0:
            return [[]]
        else:
            res_rec = make_new_prod(l[1:])
            add_first = [[l[0]]+lrec for lrec in res_rec]
            if is_in(eqnt,l[0],canc_g):
                acc = add_first + res_rec
            else:
                acc = add_first
            return acc
    def make_new_prods(ls):
        res = []
        for l in ls:
            new_l = [x for x in make_new_prod(l) if len(x)>0]
            res = union(make_eq_prod(nt,eqnt),new_l,res)
        return res
    new_r = [(s,make_new_prods(ls)) for s,ls in r]
    return (nt,t,new_r,si,eqnt) 

# Egalite sur les paires de symboles non-terminaux

def make_eq_pair_nt(eqnt):
    # eqnt :  egalite sur les non terminaux
    def _eq_pair_nt(p1,p2):
        x1,y1 = p1
        x2,y2 = p2
        return eqnt(x1,x2) and eqnt(y1,y2)
    return _eq_pair_nt


# Paires unitaires
# ----------------

def unit_pair0(nt,r,eqnt):
    # nt : symboles non terminaux
    # r : liste de productions
    # eqnt : egalite sur les non terminaux
    res = []
    for (x,rp) in r :
        for y in rp :
            if len(y) == 1 and y[0] in nt:
                res = ajout(eq_atom, (x,y[0]), res)
    return res

def next_unit_pair(nt,r,eqnt,prev):
    # nt : symboles non terminaux
    # r : liste de productions
    # eqnt : egalite sur les non terminaux
    # prev : liste de non terminaux de depart
    
    prev0 = unit_pair0(nt,r,eqnt)
    res = prev
    for (x,y) in prev :
        for (w,z) in prev0 :
            if y == w :
                res = ajout(eq_atom, (x,z), res)
    return res

def unit_pair(nt,r,eqnt):
    # nt : symboles non terminaux
    # r : liste de productions
    # eqnt : egalite sur les non terminaux
    def _next_unit_pair(e):
        return next_unit_pair(nt,r,eqnt,e)
    return fixpoint_from(make_eq_set(make_eq_pair_nt(eqnt)),\
                         _next_unit_pair,unit_pair0(nt,r,eqnt))


# Elimination des paires unitaires
# --------------------------------

def remove_unit_pairs(g):
    # g : ghc
    nt,t,r,si,eqnt = g
    pairs_unit = unit_pair(nt,r,eqnt)
    r_nv = []

    for x in nt :
        rp = prods_s(r,eqnt,x)
        for y in rp :

            if not (len(y) ==1 and (x,y[0]) in pairs_unit ) :
                r_nv = add_prod(x,y,nt, r_nv, eqnt)
        
    for (x,y) in pairs_unit :
        rp = prods_s(r,eqnt,y)
        for u in rp :

            if not (len(u) == 1 and u[0] in nt ):
                r_nv = add_prod(x,u,nt, r_nv, eqnt)



    return nt,t,r_nv,si,eqnt

# Construction d'une grammaire propre
# -----------------------------------

def make_gp(g):
    # g : ghc
    return remove_unit_pairs(remove_eps_prod(reduce_grammar(g)))

#=====================================================================#
# UE Calculabilite L3                                                 #
# TME Machines de Turing : Machines de Turing deterministes           #
# Mathieu.Jaume@lip6.fr                                               #
#=====================================================================#


#=====================================================================#
# Machines de Turing deterministes a 1 bande                          #
#=====================================================================#


# Fonction associee a une liste representant une fonction sur un domaine fini
#----------------------------------------------------------------------------
from ensembles import *

def assoc_f(lf,x):
    """ list[alpha*beta] * alpha -> beta """
    for (xf,yf) in lf:
        if xf == x:
            return yf
    return None

# Machine de Turing deterministe a 1 bande
#-----------------------------------------
#
# M = (d,q0,qok,qko)
# d = ((q,a),(q',a',m))
#

# exemple

l_M_ex1 = [((0,"A"),(1,"A","R")), ((0,"a"),(3,"a","R")), ((0,"b"),(3,"b","R")),
           ((0,"B"),(3,"B","R")), ((1,"A"),(3,"A","R")), ((1,"B"),(2,"B","R")),
           ((1,"a"),(1,"b","R")), ((1,"b"),(1,"a","R"))]

M_ex1 =(l_M_ex1,0,2,3)


# Affichage d'une configuration pour une machine de Turing a 1 bande
#-------------------------------------------------------------------

def print_config_1(L,t,q,qok,qko):
    for s in L[:t]:
        print(s,end='')
    print("|",end='')
    if q == qok:
        print("ok",end='')
    elif q == qko:
        print("ko",end='')
    else:
        print(q,end='')
    print("|",end='')
    for s in L[t:]:
        print(s,end='')
    print(" ")


# Execution d'une machine de Turing deterministe a 1 bande
#---------------------------------------------------------

def exec_MT_1(M,L,i0):
    # M : machine de Turing deterministe a 1 bande
    # L : liste representant la bande initiale
    # i0 : position initiale de la tete de lecture
    i = i0
    (d,q0,qok,qko) = M
    qcurr = q0
    Lcop =L
    di = "R"
    while qcurr != qko and qcurr != qok :
        print_config_1(Lcop,i,qcurr,qok,qko)
        if assoc_f(d,(qcurr,Lcop[i])) == None :
            qcurr = qko
            break
        (qcurr, Lcop[i], di) = assoc_f(d,(qcurr,Lcop[i]))
        if di == "R" :
            i+=1
            if i>= len(Lcop) :
                Lcop.append("Z")
        if di == "L" :
            i-=1
            if i<0 :
                i=0
                Lcop = ['Z'] + Lcop

    print_config_1(Lcop,i,qcurr,qok,qko)
    b= (qcurr == qok)

    return (b,i,Lcop)

# EXERCICE 2

l_ex2 = [((0,"Z"),(1,"Z","R")),((0,"X"),(0,"X","R")),((0,"Y"),(0,"Y","R")), ((0,"a"),(2,"X","R")), ((0,"b"),(3,"Y","R")),
           ((2,"a"),(2,"a","R")), ((3,"b"),(3,"b","R")),((3,"X"),(3,"X","R")), ((3,"Y"),(3,"Y","R")), ((2,"Y"),(2,"Y","R")),
            ((2,"X"),(2,"X","R")), ((2,"b"),(4,"Y","L")),
           ((4,"a"),(4,"a","L")),((4,"Y"),(4,"Y","L")), ((4,"X"),(0,"X","R")), ((3,"a"),(5,"X","L")),
           ((5,"b"),(5,"b","L")), ((5,"X"),(5,"X","L")),((5,"Y"),(0,"Y","R"))]
M_ex2 = (l_ex2,0,1,6)


# EXERCICE 3

d_isneg1 = [((0,"Z"),(5,"Z","R")),((0,"1"),(11,"Z","R")),((0,"0"),(10,"Z","R")), ((11,"1"),(11,"1","R")), ((11,"0"),(10,"1","R")),
           ((10,"0"),(10,"0","R")), ((10,"1"),(11,"0","R")),((11,"Z"),(2,"1","R")), ((10,"Z"),(2,"0","R")), ((2,"Z"),(3,"Z","L")),
            ((3,"1"),(41,"1","L")), ((41,"1"),(41,"1","L")),((41,"0"),(41,"0","L")),((41,"Z"),(6,"Z","R")),
            ((3,"0"),(40,"0","L")), ((40,"1"),(40,"1","L")),((40,"0"),(40,"0","L")),((40,"Z"),(5,"Z","R")) ]
M_isneg1 = (d_isneg1,0,6,5)


d_isneg = [((0,"0"),(1,"0","R")),((0,"1"),(2,"1","R")),((1,"0"),(1,"0","R")),((1,"1"),(2,"1","R")),
((1,"Z"),(3,"Z","L")),((2,"0"),(1,"0","R")),((2,"1"),(2,"1","R")),((2,"Z"),(4,"Z","L")),
((3,"0"),(3,"0","L")),((3,"1"),(3,"1","L")),((3,"Z"),(5,"Z","R")),((4,"0"),(4,"0","L")),
((4,"1"),(4,"1","L")),((4,"Z"),(6,"Z","R"))]

M_isneg =(d_isneg,0,6,5)



#============================================================#
# Composition de machines de Turing                          #
#============================================================#

# Machines de Turing utiles pour le TME
#---------------------------------------

# complement binaire et repositionnement de la tete de lecture au debut
# bande = mot binaire  se terminant par Z

d_compl_bin = [((0,"0"),(0,"1","R")), ((0,"1"),(0,"0","R")),\
               ((0,"Z"),(1,"Z","L")), ((1,"0"),(1,"0","L")),\
               ((1,"1"),(1,"1","L")), ((1,"Z"),(2,"Z","R"))]

M_compl_bin = (d_compl_bin,0,2,3)

# successeur d'un entier en representation binaire (bit de poids faibles a gauche)
# et repositionnement de la tete de lecture sur le bit de poids faible
# bande = mot binaire avec bits de poids faibles a gauche et se terminant par Z

d_succ_bin = [((0,"0"),(1,"1","L")), ((0,"1"),(0,"0","R")),\
              ((0,"Z"),(2,"1","R")), ((1,"0"),(1,"0","L")),\
              ((1,"1"),(1,"1","L")), ((1,"Z"),(3,"Z","R")),\
              ((2,"Z"),(1,"Z","L"))]

M_succ_bin = (d_succ_bin,0,3,4)

# fonction identite

M_id =([],0,0,1)

# Fonction qui construit une machine de Turing permettant de determiner
# si le symbole sous la tete de lecture est le caractere x et ne modifie
# pas la position de la tete de lecture
# C'est la MT qui accepte le langage { x }

def make_test_eq(c,alphabet):
    d = []
    for x in alphabet:
        if c==x:
            d = d + [((0,c),(1,c,"R"))]
        else:
            d = d + [((0,x),(2,x,"R"))]
        d = d + [((1,x),(3,x,"L")), ((2,x),(4,x,"L"))]
    M = (d,0,3,4)
    return M

# exemple

M_eq_0 = make_test_eq("0",["0","1","Z"])

def make_test_neq(c,alphabet):
    (d,q0,qok,qko) = make_test_eq(c,alphabet)
    return (d,q0,qko,qok)

M_neq_1 = make_test_neq("1",["0","1","Z"])

# deplacement de la tete de lecture a droite :

def make_MTright(alphabet):
    d = []
    for a in alphabet:
        d = d + [((0,a),(1,a,"R"))]
    M = (d,0,1,2)
    return M

M_Right_bin = make_MTright(["0","1","Z"])

# (propagation du bit de signe) : duplication du dernier bit d'un mot binaire


d_prop1 = [((0,"0"),(1,"0","R")), ((0,"1"),(2,"1","R")), \
           ((1,"0"),(1,"0","R")), ((1,"1"),(2,"1","R")), ((1,"Z"),(3,"0","L")),\
           ((2,"0"),(1,"0","R")), ((2,"1"),(2,"1","R")), ((2,"Z"),(3,"1","L")),\
           ((3,"0"),(3,"0","L")), ((3,"1"),(3,"1","L")), ((3,"Z"),(4,"Z","R"))]


M_prop1 =(d_prop1,0,4,5)

# Composition de machines de Turing : sequence
#---------------------------------------------

def exec_seq_MT_1(M1,M2,L,i1):
    (b,i2,L2)=exec_MT_1(M1,L,i1)
    if b:
        return exec_MT_1(M2,L2,i2)
    else:
        return (b,i2,L2)

def make_seq_MT(M1,M2):
    # M1,M2 : machines de Turing deterministes a 1 bande
    (d1,q10,q1ok,q1ko) = M1
    (d2,q20,q2ok,q2ko) = M2
    d = []
    for ((qi,et),(qe, ete, di)) in d2:
        d = ajout(eq_atom, (((2,qi),et),((2,qe), ete, di)) , d)
        if qi == q20 and q10 == q1ok:
            d = ajout(eq_atom, (((1, q10), et), ((2,qe), ete, di)), d )
        if q10 == q1ko:
            d = ajout(eq_atom, (((1, q10), et), ((2,q2ko), ete, di)), d )
    for a,b in d1 :
        qi, et = a
        qe, ete, di = b
        if (qe != q1ok and qe!= q1ko ):
            e = (((1,qi),et) , ((1,qe),ete,di) )
            d = ajout(eq_atom, e, d)
        elif  qe == q1ok :
            e = (((1,qi),et) , ((2,q20),ete,di) )
            d = ajout(eq_atom, e, d)
        elif qe == q1ko:
            e = (((1,qi),et) , ((2,q2ko),ete,di) )
            d = ajout(eq_atom, e, d)
        
    return (d,(1,q10),(2,q2ok), (2,q2ko))


# construction Mopp
M_opp_int_bin = make_seq_MT(M_compl_bin, M_succ_bin)

# Composition de machines de Turing : conditionnelle
#---------------------------------------------------

def exec_cond_MT_1(MC,M1,M2,L,i0):
    (bc,ic,Lc)=exec_MT_1(MC,L,i0)
    if bc:
        return exec_MT_1(M1,Lc,ic)
    else:
        return exec_MT_1(M2,Lc,ic)


def make_cond_MT(MC,M1,M2):
    # MC, M1, M2 : machines de Turing deterministes a 1 bande
    
    (d1,q10,q1ok,q1ko) = M1
    (d2,q20,q2ok,q2ko) = M2
    (dC, qC0, qCok, qCko) = MC
    d = []

    for ((qi,et),(qe, ete, di)) in d2:
        d = ajout(eq_atom, (((2,qi),et),((2,qe), ete, di)) , d)
        if qC0 == qCko and qi == q20 :
            d = ajout(eq_atom, (((0,qCko),et),((2,qe), ete, di)) , d)




    for a,b in dC:
        qi, et = a
        qe, ete, di = b
        if qe != qCok and qe != qCko:
            d = ajout(eq_atom, ((((0,qi),et),((0,qe),ete,di))), d)
        elif qe == qCok:
            d = ajout(eq_atom, (((0,qi),et),((1,q10),ete,di)), d)
        elif qe == qCko:
            d = ajout(eq_atom, (((0,qi),et),((2,q20),ete,di)), d)
        

    for a,b in d1 :
        qi, et = a
        qe, ete, di = b
        if qC0 == qCok and qi == q10 :
            d = ajout(eq_atom, (((0,qCok),et),((1,qe), ete, di)) , d)
        if (qe != q1ok and qe!= q1ko ):
            e = (((1,qi),et) , ((1,qe),ete,di) )
            d = ajout(eq_atom, e, d)
        elif  qe == q1ok :
            e = (((1,qi),et) , ((2,q2ok),ete,di) )
            d = ajout(eq_atom, e, d)
        elif qe == q1ko:
            e = (((1,qi),et) , ((2,q2ko),ete,di) )
            d = ajout(eq_atom, e, d)
    
    
    if d1 == []:
        if q10 == q1ko:
            for ((qi,et),_) in dC :
                if qi == q10:
                    d = ajout(eq_atom, (((1,q10),et),((2,q2ko), et,"R" )) , d)
        if q10 == q1ok:
            for ((qi,et),_) in dC :
                if qi == q10:
                    d = ajout(eq_atom, (((1,q10),et),((2,q2ok), et,"R" )) , d)
                    


        
    return (d,(0,qC0),(2,q2ok), (2,q2ko))

M_abs = make_cond_MT(M_isneg, M_opp_int_bin, M_id )
# Composition de machines de Turing : boucle
#-------------------------------------------

def exec_loop_MT_1(MC,M,L,i0):
    (bc,ic,Lc)=exec_MT_1(MC,L,i0)
    if bc:
        (bM,iM,LM) = exec_MT_1(M,Lc,ic)
        if bM:
            return exec_loop_MT_1(MC,M,LM,iM)
        else:
            return (False,iM,LM)
    else:
        return (True,ic,Lc)

def make_loop_MT(MC,M):
    # MC,M : machines de Turing deterministes a 1 bande
    (dM, qM0, qMok, qMko) = M
    (dC, qC0, qCok, qCko) = MC
    d = []

    for a,b in dC:
        qi, et = a
        qe, ete, di = b
        if qe != qCok:
            d = ajout(eq_atom, (((0,qi),et),((0,qe),ete,di)), d)
        elif qe == qCok:
            d = ajout(eq_atom, (((0,qi),et),((1,qM0),ete,di)), d)
        if qM0 == qMok and qi==qC0:
            d = ajout(eq_atom, (((1,qM0),et),((0,qe),ete,di)), d)

    for a,b in dM:
        qi, et = a
        qe, ete, di = b
        if qe != qMok:
            d = ajout(eq_atom, (((1,qi),et),((1,qe),ete,di)), d)
        elif qe == qMok:
            d = ajout(eq_atom, (((1,qi),et),((0,qC0),ete,di)), d)
        if qC0 == qCok and qi == qM0:
            d = ajout(eq_atom, (((0,qC0),et),((1,qe),ete,di)), d)   
    return (d, (0, qC0), (0, qCko), (1, qMko))

# exemple 6 
M_foo1 = make_loop_MT(M_eq_0, M_Right_bin)

#exemple 7
M_foo0 = make_cond_MT(M_isneg, M_prop1, M_id)
M_foo2 = make_seq_MT(M_foo0, M_foo1)
M_foo3 = make_seq_MT(M_Right_bin, M_compl_bin)
M_eq_Z = make_test_eq("Z",["0","1","Z"])
M_foo4 = make_cond_MT(M_eq_Z, M_id, M_foo3)
M_foo = make_seq_MT(M_foo2, M_foo4)
#======================================================================#
# Machines de Turing deterministes a k bandes                          #
#======================================================================#

# Machine de Turing deterministe a k bandes
#
# M = (d,q0,qok,qko)
#
# d = [((q,(a1,...,an)),(q',(a'1,...,a'n),(m1,...,mn))),...]
#
# bandes : L = [L1,...,Ln]
#

# Affichage d'une configuration pour une machine de Turing a k bandes
#--------------------------------------------------------------------

def print_config_k(L,T,q,qok,qko,k):
    for i in range(k):
        print_config_1(L[i],T[i],q,qok,qko)


def exec_MT_k(M,k,L,T):
    # M : machine de Turing deterministe a k bandes
    # k : nombre de bandes
    # L : liste des representations des bandes initiales
    # T : positions initiales des k tetes de lecture
    T0 = T.copy()
    (d,q0,qok,qko) = M
    qcurr = q0
    Lcop = L
    di = "R"
    while qcurr != qko and qcurr != qok :
        print_config_k(Lcop,T0,qcurr,qok,qko,k)
        Lcop_T0 = tuple(Lcop[i][T0[i]] for i in range(k))

        if assoc_f(d,(qcurr,Lcop_T0)) == None :
            qcurr = qko
            break

        (qcurr, Lcop_T0, di) = assoc_f(d,(qcurr,Lcop_T0))
        for i in range(k) :
            Lcop[i][T0[i]]=Lcop_T0[i]
            if di[i] == "R" :
                T0[i]+=1
                if T0[i]>= len(Lcop[i]) :
                    Lcop[i].append("Z")
            if di[i] == "L" :
                T0[i]-=1
                if T0[i]<0 :
                    T0[i]=0
                    Lcop[i] = ['Z'] + Lcop[i]

    print_config_k(Lcop,T0,qcurr,qok,qko,k)
    b= (qcurr == qok)

    return (b,T0,Lcop)

# mots sur {a,b} contenant autant de a que de b
#

d2_ex1 = [((0,("a","Z")),(1,("a","X"),("R","R"))),\
          ((0,("b","Z")),(2,("b","X"),("R","R"))),\
          ((0,("Z","Z")),(3,("Z","Z"),("S","S"))),\
          ((1,("a","X")),(1,("a","X"),("R","R"))),\
          ((1,("a","Z")),(1,("a","Z"),("R","R"))),\
          ((1,("b","Z")),(1,("b","Z"),("R","L"))),\
          ((1,("b","X")),(2,("b","X"),("R","R"))),\
          ((1,("Z","X")),(3,("Z","X"),("S","S"))),\
          ((2,("a","X")),(1,("a","X"),("R","R"))),\
          ((2,("a","Z")),(2,("a","Z"),("R","L"))),\
          ((2,("b","Z")),(2,("b","Z"),("R","R"))),\
          ((2,("b","X")),(2,("b","X"),("R","R"))),\
          ((2,("Z","X")),(3,("Z","X"),("S","S")))]


M2_ex1 = (d2_ex1,0,3,4)

# L = { a^nb^nc^n | n entier naturel }
# etat acceptant : 1

d2_anbncn = [((0,("Z","Z")),(1,("Z","Z"),("R","R"))), \
             ((0,("a","Z")),(2,("a","A"),("R","R"))), \
             ((2,("a","Z")),(2,("a","A"),("R","R"))), \
             ((2,("b","Z")),(3,("b","Z"),("S","L"))), \
             ((3,("b","A")),(3,("b","B"),("R","L"))), \
             ((3,("c","Z")),(4,("c","Z"),("S","R"))), \
             ((4,("c","B")),(4,("c","C"),("R","R"))), \
             ((4,("Z","Z")),(1,("Z","Z"),("R","R")))]



M2_anbncn = (d2_anbncn,0,1,5)


d2_palin_bin = [((0, ("1", "Z")), (0, ("1", "1"), ("R", "R"))), \
                ((0, ("0", "Z")), (0, ("0", "0"), ("R", "R"))), \
                ((0, ("Z", "Z")), (1, ("Z", "Z"), ("L", "S"))), \
                ((1, ("0", "Z")), (1, ("0", "Z"), ("L", "S"))), \
                ((1, ("1", "Z")), (1, ("1", "Z"), ("L", "S"))), \
                ((1, ("Z", "Z")), (2, ("Z", "Z"), ("R", "L"))), \
                ((2, ("0", "0")), (2, ("X", "X"), ("R", "L"))), \
                ((2, ("1", "1")), (2, ("X", "X"), ("R", "L"))), \
                ((2, ("Z", "Z")), (3, ("Z", "Z"), ("S", "S"))), \
                ((4, ("1", "Z")), (0, ("1", "Z"), ("S", "S"))), \
                ((4, ("0", "Z")), (0, ("0", "Z"), ("S", "S"))), \
                ((4, ("Z", "Z")), (5, ("Z", "Z"), ("R", "R"))), \
                ((5, ("Z", "Z")), (3, ("Z", "Z"), ("L", "L"))), 
                ]

M2_palin_bin = (d2_palin_bin, 4, 3, 6)

d2_un_to_bin = [((0,("$","Z")),(1,("$","$"),("R","R"))), \
                ((1,("Z","Z")),(8,("Z","0"),("S","S"))), \
                ((1,("I","Z")),(2,("I","1"),("R","R"))), \
                ((2,("Z","Z")),(9,("Z","Z"),("S","L"))), \
                ((9,("Z","0")),(9,("Z","0"),("S","L"))), \
                ((9,("Z","1")),(9,("Z","1"),("S","L"))), \
                ((9,("Z","$")),(8,("Z","$"),("S","R"))), \
                ((2,("I","Z")),(3,("I","Z"),("S","L"))), \
                ((3,("I","1")),(3,("I","1"),("S","L"))), \
                ((3,("I","0")),(4,("I","1"),("S","R"))), \
                ((4,("I","1")),(4,("I","0"),("S","R"))), \
                ((4,("I","Z")),(2,("I","Z"),("R","S"))), \
                ((3,("I","$")),(5,("I","$"),("S","R"))), \
                ((5,("I","1")),(6,("I","1"),("S","R"))), \
                ((6,("I","1")),(6,("I","0"),("S","R"))), \
                ((6,("I","Z")),(7,("I","0"),("S","R"))), \
                ((7,("I","Z")),(2,("I","Z"),("R","S")))]

M2_un_to_bin = (d2_un_to_bin, 0, 8,10)


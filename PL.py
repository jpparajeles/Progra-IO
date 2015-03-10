__author__ = 'luisdiegopizarro'
from sympy.solvers import solve
from sympy import Symbol



#print(lambda:1)





class Ecuacion():
    def __init__(self):
        self.pto1=[]
        self.pto2=[]

    def setPoints(self,ecua):
        y = Symbol('y')
        x=0
        self.pto1.append(x)
        self.pto1.append(solve(ecua(x,y), y)[0])

        x = Symbol('x')
        y=0
        self.pto2.append(solve(ecua(x,y), x)[0])
        self.pto2.append(y)


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return [x,y]
    else:
        return False

restricciones=["6*x+4*y<=24",'x+2*y<=6','-x+y<=1','y<=2']
ecuaciones=["6*x+4*y-(24)",'x+2*y-6','-x+y-1']
rectas=[]
puntos=[]
puntosSolucion=[]

for i in ecuaciones:
    form1=Ecuacion()
    form1.setPoints(lambda:eval(i))
    rectas.append(form1)
    puntos.append(form1.pto1)
    puntos.append(form1.pto2)


#intersecciones con los ejes
for e in rectas:
    print(e.pto1)
    print(e.pto2)


for x in range(0,len(rectas)):
    for y in range(x, len(rectas)):
        L1 = line(rectas[x].pto1,rectas[x].pto2)
        L2 = line(rectas[y].pto1, rectas[y].pto2)
        R = intersection(L1, L2)
        if R:
            puntos.append(R)

puntos.append([0,0])
for p in puntos:
    x=p[0]
    y=p[1]
    contador=0#cuenta cuantas restricciones cumple
    for ec in restricciones:
        if eval(ec):
            contador+=1
        else:
            break
    if contador==len(restricciones):
        puntosSolucion.append(p)


for a in puntosSolucion:
    print(a)







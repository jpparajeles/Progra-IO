__author__ = 'José Pablo'

from Enums import Mtype
from Tools import special_div
from Simplex.printing import list_str_w, matrix_str_w, head_m

class SimplexCore:
    def __init__(self, qDescicion, qHolgura, qArtificial, qSuperhabit, qDir):
        #Matrix
        # Base
        self.Zcuantity = 1
        self.base = []
        #  sub[col][fila] => celda
        # Var decision X_n
        self.decision = []
        for i in range(0, qDescicion):
            self.decision.append([])
        # Var holgura H_n
        self.holgura = []
        for j in range(0, qHolgura):
            self.holgura.append([])
        # Var Superhabit
        self.superhabit = []
        for k in range(0,qSuperhabit):
            self.superhabit.append([])
        # Var Artificiales
        self.artificial = []
        for l in range(0,qArtificial):
            self.artificial.append([])
        # Valor solucion
        self.val_sol = []
        # Si hay algo extra
        self.Solucion = ""
        self.Output = []
        # Funcion
        self.find = min if qDir == Mtype.Max else max
        self.stop = (lambda x: x < 0 )if qDir == Mtype.Max else (lambda x: x > 0)

        self.heigth = 0
        # Flags
        self.empateFlag = False
        self.empateList = []
        self.inlist = []
        self.multipleFlag = []

    def addRestricion(self, iBase, iDescicion, iHolgura,iSuperhabit, iArtificial, iSol):
        self.base.append(iBase)
        for i,elem in enumerate(iDescicion):
            self.decision[i].append(elem)
        for j, elem in enumerate(iHolgura):
            self.holgura[j].append(elem)
        for k, elem in enumerate(iSuperhabit):
            self.superhabit[k].append(elem)
        for l, elem in enumerate(iArtificial):
            self.artificial[l].append(elem)
        self.val_sol.append(iSol)
        self.heigth += 1


    def getSubZ(self,submatrix):
        return [col[-1] for col in submatrix]

    def getZ(self):
        return self.getSubZ(self.decision)+self.getSubZ(self.holgura)+self.getSubZ(self.superhabit)+self.getSubZ(self.artificial)

    def getIn(self):
        # encuentra el valor de el min/max entre descion y holgura
        last_row = self.getZ()
        value = self.find(last_row)
        # retorna el index
        return last_row.index(value)

    def getOut(self, index_pivote_c):
        # Usar la submatrix adecuada
        local = self.localizar(index_pivote_c)
        if type(local)==int:
            return
        submatrix = local[0]
        index_pivote_c_1 = local[1]
        # Obtener la columna
        pivote_c = submatrix[index_pivote_c_1]
        # si no hay empate en el paso pasado
        if self.empateFlag:
            self.Output.append("Degenerado")
        if not self.empateFlag:
            # dividir ValSol / columna pivote
            list_div = [special_div(self.val_sol[i] , pivote_c[i]) for i in range(0, self.heigth-self.Zcuantity)]
            # obtener el minimo
            minimum = min([positive for positive in list_div if positive > 0])
            # dejar el indece del min en empateList
            self.empateList = [o for o, val in enumerate(list_div) if val == minimum]
        # set Flag de empate si hay mas de 1 elemento en la lista
        self.empateFlag = True if len(self.empateList) > 1 else False
        # retornar el 1ro de la lista, indices de fila
        return self.empateList.pop(0)

    def localizar(self, index_pivote_col):
        len_d = len(self.decision)
        if index_pivote_col< len_d:
            return (self.decision,index_pivote_col)
        temp = index_pivote_col- len_d
        len_h = len(self.holgura)
        if temp < len_h:
            return (self.holgura,temp)
        temp -= len_h
        len_s = len(self.superhabit)
        if temp < len_s:
            return (self.superhabit,temp)
        temp -= len_s
        len_a = len(self.artificial)
        if(temp<len_a):
            return (self.artificial,temp)
        self.Output.append("ERROR")
        return temp-len_a

    def map_pivote(self, matrix, pivote, index):
        # para cada elemento de la lista dividalo entre el pivote
        for col in matrix:
            col[index] /= pivote

    def map_letter(self, sub):
        if sub == self.decision:
            return "x"
        if sub == self.holgura:
            return "h"
        if sub == self.superhabit:
            return "s"
        if sub == self.artificial:
            return "a"

    def update_pivote(self, index_x, index_y):
        # Usar (Descicion o Holgura)
        local = self.localizar(index_y)
        if type(local)==int:
            return
        submatrix = local[0]
        index_y_local = local[1]
        # obtener pivote operacional
        pivote = submatrix[index_y_local][index_x]
        # actualizar la base
        self.base[index_x] = "{}{}".format(self.map_letter(submatrix),index_y_local)
        # actualizar la submatriz de desicion
        self.map_pivote(self.decision, pivote,index_x)
        # actualizar la submatriz de holgura
        self.map_pivote(self.holgura, pivote,index_x)
        # actualizar la submatriz de superhabit
        self.map_pivote(self.superhabit, pivote,index_x)
        # actualizar la submatriz de artifical
        self.map_pivote(self.artificial, pivote,index_x)
        # actualizar el val solucion
        self.val_sol[index_x] /= pivote

    def map_otras(self, matrix, altura, fpivote, pivoteCol):
        for index,col in enumerate(matrix):
            col[altura] = col[altura]- (pivoteCol * fpivote[index])

    def update_resto(self, index_x, index_y):
        # fila pivote
        pivote_d = [col[index_x] for col in self.decision]
        pivote_h = [col[index_x] for col in self.holgura]
        pivote_s = [col[index_x] for col in self.superhabit]
        pivote_a = [col[index_x] for col in self.artificial]
        pivote_vs = self.val_sol[index_x]
        # Usar submatrix correcta
        local = self.localizar(index_y)
        if type(local)==int:
            return
        submatrix = local[0]
        index_y_local = local[1]
        # obtener pivote operacional
        pivote = submatrix[index_y_local][index_x]
        for fila in range(0, self.heigth):
            #No actualizar la pivote
            if(fila == index_x):
                continue
            # valor de la columna pivote en la fila actual
            pivore_columna = submatrix[index_y_local][fila]
            # actualizar resto de la filas
            # decision
            self.map_otras(self.decision,fila, pivote_d, pivore_columna)
            # holgura
            self.map_otras(self.holgura, fila, pivote_h, pivore_columna)
            # superhabit
            self.map_otras(self.superhabit, fila, pivote_s, pivore_columna)
            # artificial
            self.map_otras(self.artificial, fila, pivote_a, pivore_columna)
            # val sol
            self.val_sol[fila] = self.val_sol[fila] - (pivote_vs * pivore_columna)

    def stopf(self):
        return len([elem for elem in self.getZ() if self.stop(elem)]) > 0

    def chechSol(self):
        # Hay 0 (+|-) segun el metodo
        if self.stopf():
            # Hay almenos 1, iterar una vez más
            return False
        # Revisar por el sol multiple

        self.Output.append("~~~~~~~~~-----Solucion-----~~~~~~~~~")
        for i,elem in enumerate(self.base):
            if not "x" in elem:
                continue
            self.Output.append("{} = {}".format(elem,self.val_sol[i]))
        self.Output.append("Solucion = {}".format(self.val_sol[-1]))

        diff = list(set(range(0, len([zero[-1] for zero in self.decision if zero[-1] == 0]))) - set(self.inlist))
        # Hay 0 de diff
        if (len(diff) > 0):
            # Caso Multiple
            self.Output.append("Solución Multiple")
            self.multipleFlag = diff
            return False
        # end
        return True

    def SimplexIterate(self):
        # simplex c f
        # simplex[][i]
        var_in = self.getIn() if len(self.multipleFlag) == 0 else self.multipleFlag.pop(0)
        # Ya se uso
        self.inlist.append(var_in)
        # simples[i][]
        var_out = self.getOut(var_in)
        # pivote
        self.update_pivote(var_out,var_in)
        # resto
        self.update_resto(var_out, var_in)
        self.Output.append(str(self))
        self.Output.append(" ")
        return self if self.chechSol() else self.SimplexIterate()

    def CheckAcotada(self):
        for var_d in self.decision:
            if 0 == len([z for z in var_d if z >= 0]):
                self.Output.append("No acotada")
                return False
        return True

    def Start(self):
        return self if not self.CheckAcotada() else self.SimplexIterate()

    def result(self):
        return [(self.base[i],self.val_sol[i]) for i in range(0,self.heigth)]

    def print_aux(self,letter,lensub):
        return ["{}{}".format(letter,i) for i in range(0, lensub)]

    def __str__(self):
        # Warning! Heavy use of lists comprehension ahead. Proceed with extreme care
        width = max(
            [list_str_w(self.base), matrix_str_w(self.decision), matrix_str_w(self.holgura), list_str_w(self.val_sol),
             len("Val Sol")])
        len_d = len(self.decision)
        len_h = len(self.holgura)
        len_s = len(self.superhabit)
        len_a = len(self.artificial)
        heads = self.print_aux("x",len_d)+self.print_aux("h",len_h)+self.print_aux("s",len_s)+self.print_aux("a",len_a) + ["Val Sol"]
        quantity = 1 + 1 + len_d + len_h+len_s+len_a
        head = head_m(quantity).format("Base", *heads, width=width)
        matrix = [head_m(quantity).format(str(self.base[ii]),
                                          *([str(d_ij[ii]) for d_ij in self.decision]
                                           + [str(d_jj[ii]) for d_jj in self.holgura]
                                           + [str(d_jj[ii]) for d_jj in self.superhabit]
                                           + [str(d_jj[ii]) for d_jj in self.artificial]
                                           + [str(self.val_sol[ii])]),width=width) for ii in range(0,self.heigth)]
        matrix.insert(0,head)
        return "\n".join(matrix)

__author__ = 'José Pablo'

from fractions import Fraction
from Tools import fill_w
from Enums import Mtype
from  Simplex.Core import SimplexCore

class Simplex (SimplexCore):
    def __init__(self, qDescicion, qHolgura, qDir=Mtype.Max):
        super().__init__(qDescicion, qHolgura,0,0,qDir)

    def addRestricion(self, iBase, iDescicion, iHolgura, iSol):
        super().addRestricion(iBase, list(map(Fraction.from_float,iDescicion)),
                                 list(map(Fraction.from_float,iHolgura)), [], [], iSol)

    def addFunObj(self,iDescicion):
        self.addRestricion("z",iDescicion,fill_w(self.holgura),0)

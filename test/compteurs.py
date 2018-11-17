from MachExecUtils import *
from MachExec import *

def getDurReact(n):
	return 10

class CompteurTempsTheorique(CompteurTemps):
	def avance(self):
		self.__class__.incrementeGlobal(1)
	@classmethod
	def init(cls):
		cls.an_globalTime = 0
	@classmethod
	def incrementeGlobal(cls, an_increment):
		cls.an_globalTime += an_increment
	@classmethod
	def getGlobalVal(cls):
		return cls.an_globalTime

class CompteurReaction(CompteurReact):
	def doIt(self):
		lProcesseur = self.aLiveProg_localisation.getProcesseur()
		print(str(lProcesseur.aClassCompteur_temps.getGlobalVal()) + ' : une réaction')
		lProcesseur.aClassCompteur_temps.incrementeGlobal(lProcesseur.aFunc_getDurReact(self.__class__.getGlobalVal()))

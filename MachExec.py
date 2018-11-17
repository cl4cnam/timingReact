#
# MachExec.py
# Auteur : Claude Lion
# Date création : 12/11/2018
# Copyright : © Claude Lion 2018
#
from MachExecUtils import *

PAS_FINI = 0
FINI = 1

################################################################
#
#  Les Compteurs
#  =============
#
################################################################

class Compteur: # abstract
	def __init__(self, pLiveProg_localisation):
		self.aLiveProg_localisation = pLiveProg_localisation
	def getVal(self): pass
	def avance(self): pass

class CompteurTemps(Compteur): # abstract
	def __init__(self, pLiveProg_localisation):
		super().__init__(pLiveProg_localisation)
		self.an_start = self.__class__.getGlobalVal()
	def getVal(self):
		return self.__class__.getGlobalVal() - self.an_start

class CompteurReact(Compteur): # abstract
	def __init__(self, pLiveProg_localisation):
		super().__init__(pLiveProg_localisation)
		self.an_start = self.__class__.getGlobalVal()
	def getVal(self):
		return self.__class__.getGlobalVal() - self.an_start
	def avance(self):
		lProcesseur = self.aLiveProg_localisation.getProcesseur()
		self.__class__.incrementeGlobal()
		self.doIt()
	@classmethod
	def init(cls):
		cls.an_nombreReact = 0
	@classmethod
	def incrementeGlobal(cls):
		# printErr('--------------> ' + str(cls.an_nombreReact))
		cls.an_nombreReact += 1
	@classmethod
	def getGlobalVal(cls):
		return cls.an_nombreReact

class CompteurBlock(Compteur):
	def __init__(self, pLiveProg_localisation):
		super().__init__(pLiveProg_localisation)
		self.an_nbreBloc = 0
	def getVal(self):
		return self.an_nbreBloc
	def avance(self):
		l_parent = self.aLiveProg_localisation.aLiveProg.a_parent
		self.aLiveProg_localisation.aLiveProg = self.aLiveProg_localisation.aLiveProg.aProg.getLive()
		self.aLiveProg_localisation.aLiveProg.a_parent = l_parent
	def incremente(self):
		self.an_nbreBloc += 1


################################################################
#
#  Le Processeur
#  =============
#
################################################################

class Processeur:
	def __init__(self, pClassCompteur_temps, pClassCompteur_react, pFunc_getDurReact):
		self.aClassCompteur_temps = pClassCompteur_temps
		self.aClassCompteur_react = pClassCompteur_react
		self.aClassCompteur_block = CompteurBlock
		self.aFunc_getDurReact = pFunc_getDurReact
	def start(self, pProg):
		self.aClassCompteur_temps.init()
		self.aClassCompteur_react.init()
		self.aProg = pProg
		self.aLiveProg = pProg.getLive()
		self.aLiveProg.aProcesseur = self
		self.aLiveProg.run()

################################################################
#
#  Les instructions
#  ================
#
################################################################

class Program:
	niv_tab = 0
	def __init__(self, *args, **kwargs):
		self.aList_args = list(args)
		self.aDict_kwargs = dict(kwargs)
	def getClassNameLive(self, pClass):
		try:
			return getGlobalByName(__name__, 'Live' + pClass.__name__)
		except AttributeError:
			for lClass_base in pClass.__bases__:
				ls_rep = self.getClassNameLive(lClass_base)
				if ls_rep != None: return ls_rep
	def getLive(self):
		lClass_live = self.getClassNameLive(self.__class__)
		lList_liveArgs = [
			arg.getLive() if isinstance(arg, Program) else arg
			for arg in self.aList_args
		]
		lLiveProg = lClass_live(*lList_liveArgs, **self.aDict_kwargs)
		lLiveProg.aProg = self
		return lLiveProg
	def __str__(self):
		ls_nom = self.__class__.__name__
		if 'Prog' in ls_nom:
			ls_nom = ls_nom[4:]
		ls_debut = ls_nom + '(\n'
		ls_fin = ')'
		ls_milieu = ',\n'.join( [ str(arg) for arg in self.aList_args ] ) + '\n'
		self.__class__.niv_tab += 1
		ls_milieu = getAvecTab(ls_milieu, self.__class__.niv_tab)
		self.__class__.niv_tab -= 1
		return ls_debut + ls_milieu + ls_fin

class LiveProgram:
	def __init__(self, *args):
		self.ai_avancement = PAS_FINI
		self.aList_args = list(args)
		setParent(args, self)
	def getProcesseur(self):
		try:
			return self.aProcesseur
		except AttributeError:
			return self.a_parent.getProcesseur()
			# try:
				# return self.a_parent.getProcesseur()
			# except AttributeError:
				# printErr(self.aProg)
				# printErr(self.aList_args)
				# raise Error('aaaaa')
	def isTermine(self):
		return self.ai_avancement == FINI
	def terminer(self):
		self.ai_avancement = FINI
	def run(self):
		while not self.isTermine():
			self.doEtape()

class ProgNothing(Program): pass
class LiveProgNothing(LiveProgram):
	def __init__(self, *args):
		super().__init__(*args)
	def doEtape(self):
		self.terminer()
Nothing = ProgNothing

class ProgSeq(Program): pass
class LiveProgSeq(LiveProgram):
	def doEtape(self):
		if not self.aList_args[0].isTermine():
			self.aList_args[0].doEtape()
		elif len(self.aList_args) == 1:
			self.terminer()
		else:
			del self.aList_args[0]
Seq = ProgSeq

class ProgIn(Program): pass
class LiveProgIn(LiveProgram):
	def __init__(self, ps_condition, ps_typeAvance, pLiveProg):
		super().__init__(ps_condition, ps_typeAvance, pLiveProg)
		# printErr('---> ' + str(self.aProg))
		self.as_condition = ps_condition
		self.as_typeAvance = ps_typeAvance
		self.aLiveProg = pLiveProg
		self.aCompteur_temps = None
		self.aCompteur_react = None
		self.aCompteur_block = None
	def doEtape(self):
		lProcesseur = self.getProcesseur()
		# printErr('-----------------------' + self.as_typeAvance + '/' + str(getattr(lProcesseur,'aGlobal_time', 0)))
		if self.aCompteur_temps == None:
			self.aCompteur_temps = lProcesseur.aClassCompteur_temps(self)
			self.aCompteur_react = lProcesseur.aClassCompteur_react(self)
			self.aCompteur_block = lProcesseur.aClassCompteur_block(self)
		ls_condition = self.as_condition.replace('TimeCounter', str(self.aCompteur_temps.getVal()))
		ls_condition = ls_condition.replace('ReactCounter', str(self.aCompteur_react.getVal()))
		ls_condition = ls_condition.replace('BlockCounter', str(self.aCompteur_block.getVal()))
		if not eval(ls_condition):
			self.terminer()
		elif self.aLiveProg.isTermine():
			if self.as_typeAvance == 'TimeCounter':
				self.aCompteur_temps.avance()
			elif self.as_typeAvance == 'ReactCounter':
				self.aCompteur_react.avance()
			elif self.as_typeAvance == 'BlockCounter':
				self.aCompteur_block.avance()
		else:
			self.aLiveProg.doEtape()
			if self.aLiveProg.isTermine():
				self.aCompteur_block.incremente()

################################################################
#
#  Les abréviations
#  ================
#
################################################################

def In(ps_condition, ps_typeAvance, *pList_prog):
	return ProgIn(ps_condition, ps_typeAvance, Seq(*pList_prog))
def Delay(n):
	return ProgIn('TimeCounter < ' + str(n), 'TimeCounter', Nothing())
def React(n):
	return ProgIn('ReactCounter < ' + str(n), 'ReactCounter', Nothing())
def While(ps_condition, *pList_prog):
	return In(ps_condition, 'BlockCounter', *pList_prog)
def Repeat(n, *pList_prog):
	return While('BlockCounter < ' + str(n), *pList_prog)
def RepeatForever(*pList_prog):
	return While('True', *pList_prog)
def InMax(n, *pList_prog):
	return In( 'BlockCounter < 1 and TimeCounter < ' + str(n), 'TimeCounter', *pList_prog )
def InMin(n, *pList_prog):
	return In( 'BlockCounter < 1 or TimeCounter < ' + str(n), 'TimeCounter', *pList_prog )
def InMaxReact(n, *pList_prog):
	return In( 'BlockCounter < 1 and ReactCounter < ' + str(n), 'ReactCounter', *pList_prog )
def InMinReact(n, *pList_prog):
	return In( 'BlockCounter < 1 or ReactCounter < ' + str(n), 'ReactCounter', *pList_prog )

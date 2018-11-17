from MachExecUtils import *
from MachExec import *

import datetime
import time

class CompteurTempsReel(CompteurTemps):
	def avance(self):
		# import time
		time.sleep(10 / 1000)
	@classmethod
	def init(cls):
		# cls.adt_startTime = datetime.datetime.utcnow()
		cls.an_startTimeSec = time.clock() * 1000
	@classmethod
	def incrementeGlobal(cls, an_increment):
		pass
	@classmethod
	def getGlobalVal(cls):
		# return (datetime.datetime.utcnow() - cls.adt_startTime) / datetime.timedelta(milliseconds=1)
		return time.clock() * 1000 - cls.an_startTimeSec

class CompteurReactionReel(CompteurReact):
	def doIt(self):
		lProcesseur = self.aLiveProg_localisation.getProcesseur()
		# print(str(int(lProcesseur.aClassCompteur_temps.getGlobalVal())) + ' : une réaction')
		print(str(int(lProcesseur.aClassCompteur_temps.getGlobalVal())) + ', ', end='')

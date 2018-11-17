from MachExec import *

test = Seq(
	Delay(23),
	React(1)
)

expected = '''
23 : une réaction
'''
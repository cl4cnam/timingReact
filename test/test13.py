from MachExec import *

test = Seq(
	React(3),
	Delay(8),
	React(1)
)

expected = '''
0 : une réaction
10 : une réaction
20 : une réaction
38 : une réaction
'''
from MachExec import *

def getDurReact(n):
	return 10*n

test = InMinReact(5,
	InMax(20,
		React(3),
		Delay(17),
		React(2)
	)
)

expected = '''
0 : une réaction
10 : une réaction
30 : une réaction
60 : une réaction
100 : une réaction
'''
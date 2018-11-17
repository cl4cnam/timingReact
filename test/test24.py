from MachExec import *

def getDurReact(n):
	return 2*n

test = InMinReact(6,
	InMax(20,
		React(3),
		Delay(7),
		React(1)
	)
)

expected = '''
0 : une réaction
2 : une réaction
6 : une réaction
19 : une réaction
27 : une réaction
37 : une réaction
'''
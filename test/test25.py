from MachExec import *

def getDurReact(n):
	return 2*n

test = InMaxReact(4,
	RepeatForever(
		React(2),
		Delay(7),
		React(1)
	)
)

expected = '''
0 : une réaction
2 : une réaction
13 : une réaction
19 : une réaction
'''
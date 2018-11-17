from MachExec import *

test = InMax(85,
	In('BlockCounter >= 0', 'BlockCounter',
		InMin(40,
			React(3),
			Delay(8),
			React(1)
		)
	)
)

expected = '''
0 : une réaction
10 : une réaction
20 : une réaction
38 : une réaction
48 : une réaction
58 : une réaction
68 : une réaction
'''
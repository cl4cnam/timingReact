from MachExec import *

test = Repeat(3,
	InMin(40,
		React(3),
		Delay(8),
		React(1)
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
86 : une réaction
96 : une réaction
106 : une réaction
116 : une réaction
134 : une réaction
'''
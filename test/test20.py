from MachExec import *

test = In('ReactCounter < 11', 'BlockCounter',
	Seq(
		InMin(40,
			React(3),
		),
		InMin(37,
			React(2),
		)
	)
)

expected = '''
0 : une réaction
10 : une réaction
20 : une réaction
40 : une réaction
50 : une réaction
77 : une réaction
87 : une réaction
97 : une réaction
117 : une réaction
127 : une réaction
154 : une réaction
'''
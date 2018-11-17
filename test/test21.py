from MachExec import *

def getDurReact(n):
	return n

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
1 : une réaction
3 : une réaction
40 : une réaction
44 : une réaction
77 : une réaction
83 : une réaction
90 : une réaction
117 : une réaction
126 : une réaction
154 : une réaction
'''
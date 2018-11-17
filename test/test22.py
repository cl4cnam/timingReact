from MachExec import *

def getDurReact(n):
	return n

test = In('ReactCounter < 11', 'BlockCounter',
	Seq(
		InMin(20,
			React(3),
		),
		InMin(9,
			React(2),
		)
	)
)

expected = '''
0 : une réaction
1 : une réaction
3 : une réaction
20 : une réaction
24 : une réaction
29 : une réaction
35 : une réaction
42 : une réaction
50 : une réaction
59 : une réaction
69 : une réaction
'''
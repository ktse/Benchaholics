from random import *
def monte(times):
	total = 0
	for i in range(0,times):
		total+= simulation()
	return total / times
def simulation():
	stop = 0
	off = False
	time = 0
	while stop < 6:
		chance = randint(1,100)
		if chance < 81:
			off = False
		else:
			off = True
		if off == True:
			chance2 = randint(1,100)
			if chance2 < 31:
				time += 3
		chance3 = randint(1,100)
		if chance3 < 76:
			time += 5
		else:
			time += 13
		stop += 1
	return time


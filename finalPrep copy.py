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
		chance = random()
		if chance <= 0.8:
			off = False
		else:
			off = True
		if off == True:
			chance2 = random()
			if chance2 <= 0.3:
				time += 3
		chance3 = random()
		if chance3 <= 0.75:
			time += 5
		else:
			time += 13
		stop += 1
	return time

def nth(cap):
	count = 0
	guess = 1
	while count < cap:
		if narcissisticNumber(guess) == True:
			count+=1
		guess+=1
	guess -= 1
	return guess
def narcissisticNumber(guess):
	temp = guess
	length = len(str(guess))
	total = 0
	for i in range (length):
		total += (guess%10)**length
		guess = guess//10
	return total == temp


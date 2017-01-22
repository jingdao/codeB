#!/usr/bin/python

import numpy
import matplotlib.pyplot as plt
import time

earnings = {}
price = {}
f = open('earningdb2.txt','r')
for l in f:
	ll = l.split(',')
	tick = ll[1]
	e = float(ll[2])
	p = float(ll[3])
	if tick in earnings:
		earnings[tick].append(e)
		price[tick].append(p)
	else:
		earnings[tick] = [e]
		price[tick] = [p]
f.close()

for id0 in range(0,200,10):
	id1=id0 + 100
	plt.figure(1)
	plt.clf()
	for t in earnings:
#	y = earnings[t][id0:]
		y = numpy.array(earnings[t][1:]) / numpy.array(earnings[t][:-1])
		y = y[id0:id1]
		x = range(id0,id1)
		plt.plot(x,y,label=t)
	plt.xlabel('Time')
	plt.ylabel('Relative Earnings ($)')
	plt.axis([id0,id1,0.9,1.1])
	plt.legend()
	plt.savefig('/home/jd/Desktop/codeB/pa'+str(id0)+'.png')
	plt.figure(2)
	plt.clf()
	for t in earnings:
		base = price[t][id0]
		y = numpy.array(price[t])[id0:id1] / base
		x = range(id0,id1)
		plt.plot(x,y,label=t)
	plt.xlabel('Time')
	plt.ylabel('Relative Stock Price ($)')
	plt.axis([id0,id1,0.99,1.01])
	plt.legend()
	plt.savefig('/home/jd/Desktop/codeB/pb'+str(id0)+'.png')
	print 'Saved to Desktop'

	time.sleep(1)


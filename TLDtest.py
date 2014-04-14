#!/usr/bin/env python
# PassiveDNSSearcher [PDS]
# version 1.0
# devoleped in python v3.4
# born Thursday 27 March 2014 A.D.				  
# made by Olaf Elzinga & Nick de Bruijn Van Melis En Mariekerke	 
# this file is meant to test modules to split tld to array and check if they exists

from dnspy.dnspy import Dnspy
import tldextract

log = open('test.log','r')

def main():
	tldList={}
	for line in log:
		array = (line.split('||')) #split each line get from passiveDNS logf ile
		domainame = array[4]
		#tld = tldex(domainame)
		tld = DNSPY(domainame)
		

		print (tld)
		#if not tld:
		#	tld = "not existing"
		#fillList(tldList, tld)


def tldex(arg):
	tld = tldextract.extract(arg)
	tld = tld.suffix
	return tld

def DNSPY(arg):
	d = Dnspy()
	return d.subdoms(arg[:-1])



def fillList(x, y):
	if y not in x:
		x[y] = 1
	else:
		x[y] += 1

if __name__ == "__main__":
    main()
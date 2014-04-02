#!/usr/bin/env python
# PassiveDNSSearcher [PDS]
# version 1.0
# devoleped in python v3.4
# born Thursday 27 March 2014 A.D.				  
#      ░░███████ ]▄▄▄▄▄▄▄▄▄ 
#  ▂▄▄▄▅█████████▅▄▄▃▂       
#l██████████████████████].    
#  ◥⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙▲⊙◤..
# made by Olaf Elzinga & Nick de Bruijn Van Melis En Mariekerke	 
# import
import getopt, sys
import tldextract
# global vars
log = None
filex = open('testfile.txt','w')

def main():
    global log
    logCheck = False
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 't:l:hs' # before : is for value with argu / after : no arg[litle bit strange]
															, ['ttl=', 
		                                                       'log=',
		                                                       'help',
		                                                        'statistic',])
    except getopt.GetoptError as err:
        print(err)
        print("type -h for more information!")
        sys.exit()

    if options:
        #print(options)
        for opt, arg in options:
            if opt in ('-l', '--log'):
                log = open(arg,'r')
                logCheck = True
            elif opt in ('-h', '--help'): # help !work in progrese!
                help()
                sys.exit()
        if logCheck == True:
            for opt, arg in options:   	
                if opt in ('-t', '--ttl'): # time to live !work in progrese!
                    TTL(arg)
                elif opt in ('-s', '--statistic'):
                    statistic()
                elif opt in ('-a', '--all'):
                    statistic()
                    TTL(arg)
        else:
            print("Select a log with -l \nFor more info check --help")
            sys.exit()

    else:
    	print("Give an option to run this script \nType -h for more information!")
    	sys.exit()

def help():
	print("-s 	:Show all info about a log file")
	print("-t   :Print all lines with less than Time-to-Live is specified")

def statistic():
	tldList={}
	DNSsList = {}
	QTList={}
	for line in log:
		array = (line.split('||')) #split each line get from passiveDNS logf ile
		#Top Level Domain [TLD] 
		tld = tldextract.extract(array[4])
		tld = tld.suffix
		if not tld:
			tld = "not existing"
		fillList(tldList, tld)
		#DNS servers involved 
		DNSs = (array[2])
		fillList(DNSsList, DNSs)
		#Query Type [Record (e.g. A, CNAME, MX)]
		QT = (array[5])
		fillList(QTList, QT)

	print("\nDNSserver")
	printList(DNSsList)
	print("\nTop Level Domains")
	printList(tldList)
	print("\nQuery types")
	printList(QTList)

def TTL(arg):
	TTL=[]
	for line in log:
		array = (line.split('||'))
		TTLv = array[7]
		if int(TTLv)<int(arg):
			TTL.append(line)
	print (''.join(TTL))

def printList(item):
	for key, value in item.items():
		spaceLength = 30-len(key)
		line = key,''.ljust(spaceLength),":", value

		print(key,''.ljust(spaceLength),":", value)	
		filex.write(str(line)+"\n")

def fillList(x, y):
	if y not in x:
		x[y] = 1
	else:
		x[y] += 1

if __name__ == "__main__":
    main()

#statistic(log) 
#from epicsclass import *;
#from speadsheet import *;

import re;
import math;
import sys, traceback
import copy


#execfile('guiClass.py')
execfile('epicsclass.py')
#execfile('speadsheet.py')
#execfile('screenMaker.py')
#execfile('genCode.py')
#execfile('edmMaker.py')
#execfile('edmClass.py')

"""
execfile('epicsParse.py')


epicsdb = ssToUserPvs('MDRM.csv',None)
xw=[250,100,100] 

scr=dbToScreen1(epicsdb,False,False,24)
scr.writeXML('test.opi')


scr=dbToScreen1(epicsdb,True,True,24)
scr.writeXML('testch.opi')

newdb=makeGlobalEpicsDb(epicsdb,'d_window0_RBV','$(P)$(R)d_window$(CH)_RBV',['VME01:','VME02:','VME03:'],['DIG1:','DIG3:'],['0','1','2','3','4','5'])
 
xw=[200,100,0] 
scr=dbToScreen1(newdb,True,False,24)
scr.writeXML('testg.opi')


a=readEpicsDb('gretBoard.template')
b=find(a,None,'ao',None,None)
for x in b: print x.getPvName()
for x in b: print x.getAsynSpec()['param']
for x in b: print x.getRecType()
for x in b: print x.getField('DTYP')

b=find(a,None,"(ao)|(bo)|(mbbo)|(longout)",None,None)
b=find(a,None,None,'DTYP','asyn')
"""



e_pvnamestr='$(P)$(R)%s'
e_pvnamestrrbv='$(P)$(R)%s_RBV'



# take a screen and make an epics database
def screenToEpicsDb(scrfile):
	
	scr=cssScreen()
	scr.readXML(scrfile);
	wlist = scr.getWidgets()
	
	epicsdb=[]
	
	for w in wlist:
		if w.getType()!='label':
			pv=epicspv()
			pv.setPvName(w.getField('pv_name'))
			
			#add some junk metadata, so gui maker can deal with it.
			r={ 'Field Mode': 'RW',  'Human field name': 'dont know',  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'i'}
		
			r['Human field name']=pv.getPvName()
		
			pv.setExtra('row',r)

			pv.setRecType('longin')
			
			epicsdb.append(pv)
			
			
			
	return(epicsdb)

###########################################################################################
# given a list of pvs we find str in pvname and replace with new str.
#
#
###########################################################################################
def pvNameReplace(epicsdb,findstr,replacestr):
	for pv in epicsdb:
		s=pv.getPvName()
		s=s.replace(findstr,replacestr)
		pv.setPvName(s)






###########################################################################################
#give list of dbs, where each db is a list of epicspv(). make all same length. 
#return one db with pvs interleaved. 
#example one database is all the trig_rate pvs. Another is all the trig_enable pvs.
# make new database with order trig_rate0, trigenable0, trigrate1, etc...
#used fr making guis.
#give an interleave number. if the number is 1, then we take 1 pv from db1, 1 pv from db2 etc.
#if the number is 10, we take 10 from db1, 10 from db2 etc.
########################################################################################
def interleaveEpicsDb(dbs,interleave):
	
	#number of databases
	numdb=len(dbs)
	
	#new empty epics database
	newdb=[]
	
	
	
	#process pvs in dbs, use len of shortest db
	#figure out shortest db length
	dblen=2000000000
	for db in dbs:
		if len(db)<dblen:
			dblen=len(db)
			
	
	#fill in new epics database, interleaving the inputted databases.
	for k in range(0,dblen,interleave):
		for db in dbs:
			for i in range(interleave):
				newdb.append(db[k+i])
			
		
	return(newdb)

#################################################################################
#
#give epics db. give pvname to find, with macros. gen new epics db with macros filled in
#for making a global screen with all windws etc.. or all m counters.
#make an epics db, with base pv name with macros: $(P), $(R), $(CH), for vme, board and chan.
# guve lists of what P, R and chan are set to. we get nested for loops. give None if no for loop
#################################################################################

def makeGlobalEpicsDb(epicsdb,findname,basename,vmelist,boardlist,chanlist):




	if vmelist==None:
		vmelist=['']
	
	
	if boardlist==None:
		boardlist=['']
	
	
	
	if chanlist==None:
		chanlist=['']
	
	
	targets=find(epicsdb,findname,None,None,None)

	
	longouts=find(targets,'LONGOUT',None,None,None)
	
	for x in longouts:
		targets.remove(x)
		
		
	longins=find(targets,'LONGIN',None,None,None)
	for x in longins:
		targets.remove(x)
	
	
	print "found pvs"
	for t in targets:
		print t.getPvName()
		
	print '_______________________'
	
	newdb=[]
	
	if (len(targets)>1):
		return(newdb)
		
	for v in vmelist:
		for b in boardlist:
			for c in chanlist:
			
				strx=basename.replace('$(P)',v)
				strx=strx.replace('$(R)',b)
				strx=strx.replace('$(CH)',c)
				
				pv=targets[0].deepcopy()
				
				pv.setPvName(strx)
				
				r=pv.getExtra('row')
				if pv.isOutRec():
					r['Field Mode']='W'				
				else:
					r['Field Mode']='R'
					
				
				r['Human field name']='%s%s-%s'%(v,b,c)
				newdb.append(pv)
				print pv.getPvName()
				
				
	return(newdb)		
				
				
	
		


##############################################################################
#
# give spreadsheet row as dict. give epics pv list to add to.
# makes a fanout pv for globals. 
# fans out a single pv to many boards in many crates
#fans from global on trig crate to boards on dig crates
#these pvs live on master creates
##############################################################################

def makeDigGlobalPv(epicsdb,vmelist,boardlist,r):
	
	
	
	outs=['OUTA','OUTB','OUTC','OUTD','OUTE','OUTF','OUTG','OUTH']
	
	
	
	for k in range(len(vmelist)):
		ko=0
		pvname="GLBL:DIG:F%02d:%s"%(vmelist[k],r['Software field name'])
		pvf=epicspv()
		pvf.setPvName(pvname)
		pvf.setRecType('dfanout')
		pvf.setField('PREC','3')
		
		if (k<(len(vmelist)-1)):
			nxtpv="GLBL:DIG:F%02d:%s PP NMS"%(vmelist[k+1],r['Software field name'])
			pvf.setField(outs[ko],nxtpv)
			ko=ko+1
		
		
		for brd in boardlist:
			# pvn2="VME%02d:DIG%d:%s PP NMS"%(vmelist[k],brd,r['Software field name'])
			pvn2="VME%02d:%s:%s PP NMS"%(vmelist[k],brd,r['Software field name'])
			pvf.setField(outs[ko],pvn2)
			ko=ko+1
			
		#tell where the pv lives...
		pvf.setExtra('live_on','GLBL')
	
		epicsdb.append(pvf)
		
	
	


		


##############################################################################
#
# give spreadsheet row as dict. give epics pv list to add to.
# makes fanouts from global in master crate to dig crates. thse pvs live on master crate
##############################################################################

def makePvFanGlbl2Crates(epicsdb,vmelist,r):
	
	
	
	outs=['OUTA','OUTB','OUTC','OUTD','OUTE','OUTF','OUTG','OUTH']
	
	# we make the pv if it is NOT a channel, or IS Chan 0.
	# if chan 0, then the name has the 0 stripped off.
	(name,ischan) = getNameFromSwFName(r['Software field name'])
	
	if name == None:
		return(epicsdb);


	
	for k in range(len(vmelist)):
		ko=0
		pvname="GLBL:DIG:F%02d:%s"%(vmelist[k],name)
		pvf=epicspv()
		pvf.setPvName(pvname)
		pvf.setRecType('dfanout')
		pvf.setField('PREC','3')
		
		#next fanout for next crate. one fanout per crate.
		if (k<(len(vmelist)-1)):
			nxtpv="GLBL:DIG:F%02d:%s PP NMS"%(vmelist[k+1],name)
			pvf.setField(outs[ko],nxtpv)
			ko=ko+1
		
		
		
		pvn2="VME%02d:GLBL:%s PP NMS"%(vmelist[k],name)
		pvf.setField(outs[ko],pvn2)
		ko=ko+1
		
		#tell where the pv lives...
		pvf.setExtra('live_on','GLBL')
		
		epicsdb.append(pvf)
		
	
	





##############################################################################
#
# give spreadsheet row as dict. give epics pv list to add to.
# makes fanouts from dig global in dig crate to dig boards. thse pvs live on dig crate
##############################################################################

def makePvFanCrate2Boards(epicsdb,vmelist,boardlist,r):
	
	
	
	outs=['OUTA','OUTB','OUTC','OUTD','OUTE','OUTF','OUTG','OUTH']
	
		
	# we make the pv if it is NOT a channel, or IS Chan 0.
	# if chan 0, then the name has the 0 stripped off.
	(name,ischan) = getNameFromSwFName(r['Software field name'])
	if name == None:
		return(epicsdb);


	
	for k in range(len(vmelist)):
		ko=0
		pvname="VME%02d:GLBL:%s"%(vmelist[k],name)
		
		pvf=epicspv()
		pvf.setPvName(pvname)
		pvf.setRecType('dfanout')
		pvf.setField('PREC','3')
		
		
	
		for brd in boardlist:
			#pvn2="VME%02d:DIG%d:%s PP NMS"%(vmelist[k],brd,name)
			pvn2="VME%02d:%s:%s PP NMS"%(vmelist[k],brd,name)
			pvf.setField(outs[ko],pvn2)
			ko=ko+1
			
		
		#tell where the pv lives...
		pvf.setExtra('live_on','VME%02d'%(vmelist[k]))
		
		epicsdb.append(pvf)
		
	
##########################################################################	
#use r['Software field name']	 from ss as swfname. 
#return None of pv is channel 1-9.
#return pv w/out channel number for chan 0
#return pv r['Software field name'] if nto a channel
##########################################################################
def getNameFromSwFName(swfname):
	# we make the pv if it is NOT a channel, or IS Chan 0.
	# if chan 0, then the name has the 0 stripped off.
	ischan=0
	name = None
	if (re.search('[0-9]$',swfname) !=None):
		#it is a channel...
		#is last digit a zero?
		digit=re.search('[0-9]$',swfname).group(0)
		if (digit=='0'):
			name= re.search('.*(?=[0-9]$)',swfname).group(0)
			ischan=1
		else:
			#dont make the pv and return
			name = None
			ischan=1

	else:
		#make the pv, and not a channel
		name= swfname	
		ischan=0
	
	return((name,ischan));


##############################################################################
#
# if the pv in ss row is a channel, and is channel 0, we make a board level
# pv. this pv fans out from board to each channel. the channel pvs are created
# elsewhere, in the normal dig epics database. this is just for connecting globals 
##############################################################################

def makePvFanBrd2Chan(epicsdb,vmelist,boardlist, r):
	#determine if it is a channel pv. does it end with a number?
	
	outs=['OUTA','OUTB','OUTC','OUTD','OUTE','OUTF','OUTG','OUTH']
	

		
	# we make the pv if it is NOT a channel, or IS Chan 0.
	# if chan 0, then the name has the 0 stripped off.
	
	(name,ischan) = getNameFromSwFName(r['Software field name'])
	
	if name == None:
		return(epicsdb);
	
	if ischan==0:
		return(epicsdb);

	
	
	for k in range(len(vmelist)):
			

		for brd in range(len(boardlist)):

			pvf=epicspv()
			pvf.setRecType('dfanout')
	   		#pvf.setPvName("GLBL:DIG:F01:%s"%(name))

	   		pvf.setPvName("VME%02d:%s:%s"%(vmelist[k],boardlist[brd],name))

	   		pvf.setField('PREC','3')
	   		pvf.setField('OUTA',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,0))
	   		pvf.setField('OUTB',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,1))
	   		pvf.setField('OUTC',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,2))
	   		pvf.setField('OUTD',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,3))
	   		pvf.setField('OUTE',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,4))
	   		pvf.setField('OUTF',"VME%02d:%s_F2:%s PP NMS"%(vmelist[k],boardlist[brd],name))
			pvf.setExtra('live_on','VME%02d'%(vmelist[k]))
	   		epicsdb.append(pvf)


	   		pvf2=epicspv()
	   		pvf2.setPvName("VME%02d:%s_F2:%s"%(vmelist[k],boardlist[brd],name))
	   		pvf2.setRecType('dfanout')
	   		pvf2.setField('PREC','3')
	   		pvf2.setField('OUTA',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,5))
	   		pvf2.setField('OUTB',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,6))
	   		pvf2.setField('OUTC',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,7))
	   		pvf2.setField('OUTD',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,8))
	   		pvf2.setField('OUTE',"VME%02d:%s:%s%d PP NMS"%(vmelist[k],boardlist[brd],name,9))
			pvf2.setExtra('live_on','VME%02d'%(vmelist[k]))
	   		epicsdb.append(pvf2)





##############################################################################
# make a single global pv of correct type based on ss.
# if a channel pv, we only make a globl for chan0, and strip off the 0.
# pv lives on crate. it will have a out link to fanout 
#give ss row. and epics db to add to
##############################################################################

#we make globals here- all pvs live on the trigger crate or in a soft ioc. or any ioc I guess.
#the globals fan out to directly talk to the dig board and chan pvs. only one epics db is generated
def makePvGlblData(epicsdb,r):


	try:
		iscreatedpv = 0
	
		# we make the pv if it is NOT a channel, or IS Chan 0.
		# if chan 0, then the name has the 0 stripped off.
		(name,ischan) = getNameFromSwFName(r['Software field name'])
		
		if name == None:
			return(iscreatedpv);

		
		
		pv=epicspv()
		pv.setPvName("GLBL:DIG:%s"%(name))
		pv.setField('DESC',r['Field Description for database'][0:30])
		pv.setField('OUT',"GLBL:DIG:F01:%s PP NMS"%(name))
		pv.setField('DTYP','Soft Channel')
		pv.setExtra('live_on','GLBL')
		#if h or I type, we make long out, longin
		if (r['EPICS type'].lower() =="h" or r['EPICS type'].lower() =="i") :



			
			#we make pvs here.
			if (re.search('W',r['Field Mode'])!=None):
				
				pv.setRecType('longout')
		
				r['Field Mode']='W'
				pv.setExtra('row',r)
				fillEpicsPvFields(pv,r['EPICS PV Fields'])
				pv.setExtra('live_on','GLBL')
				epicsdb.append(pv)
				iscreatedpv=1




		if (r['EPICS type'].lower() =="m") :
			if (re.search('W',r['Field Mode'])!=None):
				
				pv.setRecType('mbbo')
				
				pv.setField('DOL',"0")
				
				fillMultiBitFields(pv,r['Bitfield Sub-Descriptor'],r['Bit'])

				r['Field Mode']='W'

				pv.setExtra('row',r)
				fillEpicsPvFields(pv,r['EPICS PV Fields'])
				pv.setExtra('live_on','GLBL')
				epicsdb.append(pv)
				iscreatedpv=1




		if (r['EPICS type'].lower() =="b" or r['EPICS type'].lower() =="bm") :
			if (re.search('W',r['Field Mode'])!=None):
				
				pv.setRecType('bo')
				pv.setField('DOL',"0")
	
				fillBitFields(pv,r['Bitfield Sub-Descriptor'])
				r['Field Mode']='W'
				pv.setExtra('row',r)
				fillEpicsPvFields(pv,r['EPICS PV Fields'])
				pv.setExtra('live_on','GLBL')

				epicsdb.append(pv)
				iscreatedpv=1





		if (r['EPICS type'].lower() =="a") :
			if (re.search('W',r['Field Mode'])!=None):
				
				pv.setRecType('ao')
				pv.setField('EGU',r['EPICS units'])

				#!! how do we set DOL? It seems to set max val...
				#!! need max/min vals in ss.
				pv.setField('PREC', "2")
				fillEpicsPvFields(pv,r['EPICS PV Fields'])
				r['Field Mode']='W'
				pv.setExtra('row',r)
				pv.setExtra('live_on','GLBL')


				epicsdb.append(pv)
				iscreatedpv=1


	except:
			print "Parsing error"
			print r

			print " "
			traceback.print_exc(file=sys.stdout)
			




	return(iscreatedpv)		

				



##############################################################################
#
#fans out for channel pvs- single pv fans out to chan 0,1,2...9
#
#
##############################################################################

def makeDigChanGlobalPv(epicsdb,pv,r):
	#determine if it is a channel pv. does it end with a number?
	if (re.search('[0-9]$',r['Software field name']) !=None):
		#is last digit a zero?
		digit=re.search('[0-9]$',r['Software field name']).group(0)
		if (digit=='0'):
			#get pv name minus the last digit
			name= re.search('.*(?=[0-9]$)',r['Software field name']).group(0)
			pv2=pv.deepcopy()
			
			pv2.setPvName("GLBL:DIG:%s"%(name))
			
			pv2.setField('OUT',"GLBL:DIG:F01:%s PP NMS"%(name))
			
			
			epicsdb.append(pv2)
			

			pvf=epicspv()
			pvf.setRecType('dfanout')
			pvf.setPvName("GLBL:DIG:F01:%s"%(name))
			pvf.setField('PREC','3')
			pvf.setField('OUTA',"GLBL:DIG:%s%d PP NMS"%(name,0))
			pvf.setField('OUTB',"GLBL:DIG:%s%d PP NMS"%(name,1))
			pvf.setField('OUTC',"GLBL:DIG:%s%d PP NMS"%(name,2))
			pvf.setField('OUTD',"GLBL:DIG:%s%d PP NMS"%(name,3))
			pvf.setField('OUTE',"GLBL:DIG:%s%d PP NMS"%(name,4))
			pvf.setField('OUTF',"GLBL:DIG:F02:%s PP NMS"%(name))
			
			epicsdb.append(pvf)

			
			pvf=epicspv()
			pvf.setPvName("GLBL:DIG:F02:%s"%(name))
			pvf.setRecType('dfanout')
			pvf.setField('PREC','3')
			pvf.setField('OUTA',"GLBL:DIG:%s%d PP NMS"%(name,5))
			pvf.setField('OUTB',"GLBL:DIG:%s%d PP NMS"%(name,6))
			pvf.setField('OUTC',"GLBL:DIG:%s%d PP NMS"%(name,7))
			pvf.setField('OUTD',"GLBL:DIG:%s%d PP NMS"%(name,8))
			pvf.setField('OUTE',"GLBL:DIG:%s%d PP NMS"%(name,9))
			
			epicsdb.append(pvf)



##############################################################################
#
#The structure of global db is this:
#  if not a channel:
#  global pv of ao,long bo, etc that has value. outs to fanout.
#   a fanout record to point to each dig in each crate. If 10 crates, we have 10 fanouts
#   if 4 digs per crate, then each fanout has points to 4 digs.

# if a channel
# we make a global value pv
# we make 2 fanouts from global, for chans 0 to 9
# then like above. 
##############################################################################

#we make globals here- all pvs live on the trigger crate or in a soft ioc. or any ioc I guess.
#the globals fan out to directly talk to the dig board and chan pvs. only one epics db is generated
def ssToDigGlobalPVs(ss_filename, vmelist,boardlist,epicsfile):
	ss=spreadsheet()
	ss.readTabText(ss_filename);
	mycols = range(5,21)
	rows=ss.getColsD(mycols)
	
	epicsdb=[]
	
	
	
	for r in rows:
		
		try:
			#if h or I type, we make long out, longin
			if (r['EPICS type'].lower() =="h" or r['EPICS type'].lower() =="i") :



				pv=None
				pv_rbv=None

				#we make pvs here.
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('longout')
					pv.setPvName("GLBL:DIG:%s"%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT',"GLBL:DIG:F01:%s PP NMS"%(r['Software field name']))
					pv.setField('DTYP','Soft Channel')

					r['Field Mode']='W'
					pv.setExtra('row',r)
					fillEpicsPvFields(pv,r['EPICS PV Fields'])

					epicsdb.append(pv)

					makeDigGlobalPv(epicsdb,vmelist,boardlist,r)
					makeDigChanGlobalPv(epicsdb,pv,r);		



			if (r['EPICS type'].lower() =="m") :
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('mbbo')
					pv.setPvName("GLBL:DIG:%s"%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT',"GLBL:DIG:F01:%s PP NMS"%(r['Software field name']))
					pv.setField('DOL',"0")
					pv.setField('DTYP','Soft Channel')
					fillMultiBitFields(pv,r['Bitfield Sub-Descriptor'],r['Bit'])
						
					r['Field Mode']='W'
														
					pv.setExtra('row',r)
					fillEpicsPvFields(pv,r['EPICS PV Fields'])

					epicsdb.append(pv)
					makeDigGlobalPv(epicsdb,vmelist,boardlist,r)
					makeDigChanGlobalPv(epicsdb,pv,r);		




			if (r['EPICS type'].lower() =="b" or r['EPICS type'].lower() =="bm") :
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('bo')
					pv.setPvName("GLBL:DIG:%s"%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT',"GLBL:DIG:F01:%s PP NMS"%(r['Software field name']))
					pv.setField('DOL',"0")
					pv.setField('DTYP','Soft Channel')
					
					fillBitFields(pv,r['Bitfield Sub-Descriptor'])
					r['Field Mode']='W'
					pv.setExtra('row',r)
					fillEpicsPvFields(pv,r['EPICS PV Fields'])

					epicsdb.append(pv)
					makeDigGlobalPv(epicsdb,vmelist,boardlist,r)
					makeDigChanGlobalPv(epicsdb,pv,r);		


			
			

			if (r['EPICS type'].lower() =="a") :
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('ao')
					pv.setPvName("GLBL:DIG:%s"%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT',"GLBL:DIG:F01:%s PP NMS"%(r['Software field name']))
					pv.setField('DTYP','Soft Channel')
					pv.setField('EGU',r['EPICS units'])
					
					
					
					#!! how do we set DOL? It seems to set max val...
					#!! need max/min vals in ss.
					pv.setField('PREC', "2")
					fillEpicsPvFields(pv,r['EPICS PV Fields'])
					r['Field Mode']='W'
					pv.setExtra('row',r)
					
				
					epicsdb.append(pv)
					makeDigGlobalPv(epicsdb,vmelist,boardlist,r)
					makeDigChanGlobalPv(epicsdb,pv,r);		




		except:
				print "Parsing error"
				print r
				
				print " "
				traceback.print_exc(file=sys.stdout)
				break
				
	
			
	writeEpicsDb(epicsdb,epicsfile);
	
	
	return(epicsdb)		
			
				





#####################################################################################################
#
# 
# this is a distributed global database
# make global pvs and fanout to crates on glbl crate
# make dig crate pvs, and board pvs and chan fanout pvs on dig crate.
# all pvs goto one list of pvs, use find by extra "lives_on" to see which crate they belong to.
#
# for non channels
# glbl pv (ao)-->global fanout----> vme01:global (fanout)---->vmexx:dig1:pv (ao)
#				   			---->vmexx:digz2pv (ao)
#
# for a chan
# for non channels
# glbl pv (ao)-->global fanout----> vme01:global (fanout)---->vmexx:dig1:fanout1--->vme1:dig1:chan0
#										--->vme1:dig1:chan1
#											
#							---->vmexx:dig1:fanout2--->vme1:dig1:chan5
#							---->vmexx:dig1:fanout2--->vme1:dig1:chan6
#							
#							
#   glbl crate		glbl crate	dig crate		dig crate		dig crate			   			
#######################################################################################################


#we make globals here- all pvs live on the trigger crate or in a soft ioc. or any ioc I guess.
#the globals fan out to directly talk to the dig board and chan pvs. only one epics db is generated
def ssToDigGlobalPVsDist(ss_filename, vmelist,boardlist,epicsfile):
	ss=spreadsheet()
	ss.readTabText(ss_filename);
	mycols = range(5,21)
	rows=ss.getColsD(mycols)
	
	#get only rows that have a m b bm h i as epics types
	rows = ss.find(rows,'EPICS type',r'(a)|(m)|(b)|(bm)|(h)|(i)')
	
	epicsdb=[]
	
	
	
	for r in rows:
		
		try:
			#make pv on master crate that is ao, etc. outs to a fanout on master crate
			#if a channel pv, then it makes a single global w/out channel
			iscreatepv = makePvGlblData(epicsdb,r)
			
			
			if (iscreatepv>0):
				#make fanouts to dig crates, that live on master crate
				#makes a fanout per crate. not that efficient, shoudl be 7 crates per fanout
				makePvFanGlbl2Crates(epicsdb,vmelist,r)
				
				#make crate level pvs resigding on dig crates. they are fanouts to boards.
				#if it is a board pv, then this fanout points to it. board pv is made
				#by regular dig epics database. 
				makePvFanCrate2Boards(epicsdb,vmelist,boardlist,r)
				
				#this makes another level of fanouts if it is a channel pv. make a board
				#level pv (fanout) that fans to each channel. the actual chan pv is made
				#by dig epics database and is not global.
				makePvFanBrd2Chan(epicsdb,vmelist,boardlist, r)
			
			
			
			
		except:
				print "Parsing error"
				print r
				
				print " "
				traceback.print_exc(file=sys.stdout)
				break
				
	
			
	writeEpicsDb(epicsdb,epicsfile);
	
	
	return(epicsdb)		
			
				




##############################################################################
#
#
#
#
##############################################################################

def saveEpicsDbByCrates(epicsdb,sysname):
	#get list of all crates
	crates=[]
	for pv in epicsdb:
		crates.append(pv.getExtra('live_on'))
		
	#take out duplicates
	crates=set(crates);
	
	for cr in crates:
		db=findExt(epicsdb,'live_on',cr)
		fname='dgsGlobals_%s_%s.db'%(sysname,cr)
		print "Writing %s"%fname
		writeEpicsDb(db,fname);
		
		


##############################################################################
#
#
#
#
##############################################################################

def saveEpicsDbByCrates2(epicsdb,sysname,path):
	#get list of all crates
	crates=[]
	for pv in epicsdb:
		crates.append(pv.getExtra('live_on'))
		
	#take out duplicates
	crates=set(crates);
	
	for cr in crates:
		db=findExt(epicsdb,'live_on',cr)
		fname='%sdgsGlobals_%s_%s.db'%(path,sysname,cr)
		print "Writing %s"%fname
		writeEpicsDb(db,fname);
		
		


##############################################################################
#
#
#
#
##############################################################################

def ssToUserPvs(ss_filename,epicsfile):

	if isinstance(ss_filename,str):
		ss=spreadsheet()
		ss.readTabText(ss_filename);
	else:
		ss=ss_filename

	
	mycols = range(5,21)
	rows=ss.getColsD(mycols)
	
	#debugging... make a subset
	#leds=ss.find(rows,'Register Name','led')
	#goop=rowsDToUserPvs(leds,None)
	#for g in goop: print g.getPvName()
	
	analog_mult = float(ss.verdataD['Register Time Unit ns'])
	epicsdb = rowsDToUserPvs(rows,epicsfile,analog_mult)
	return(epicsdb)
	


#analog mult is the slope for multipliing ns to get right time value in register.
#rows is list of rows, epicsfile is filename

def rowsDToUserPvs(rows,epicsfile,analog_mult):
	epicsdb=[]	
	for r in rows:
		
		try:
			#if h or I type, we make long out, longin
			if (r['EPICS type'].lower() =="h" or r['EPICS type'].lower() =="i") :



#e_pvnamestr='$(P)$(R)%s'
#e_pvnamestrrbv='$(P)$(R)%s_RBV'

				pv=None
				pv_rbv=None

				#we make pvs here.
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('longout')
					pv.setPvName(e_pvnamestr%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT'," ")
					pv.setField('DTYP','asynUInt32Digital')
					if r['EPICS units']!=None:
						pv.setField('EGU',r['EPICS units'])
					mask = makeMask_aa(r['Bit'])
					pv.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))
					
					fillEpicsPvFields(pv,r['EPICS PV Fields'])

					pv.setExtra('row',r)
					
					epicsdb.append(pv)


				if (re.search('R',r['Field Mode'])!=None):
					pv_rbv=epicspv()
					pv_rbv.setRecType('longin')
					pv_rbv.setPvName(e_pvnamestrrbv%(r['Software field name']))
					pv_rbv.setField('DESC',r['Field Description for database'][0:30])
					pv_rbv.setField('DTYP','asynUInt32Digital')
					pv_rbv.setField('INP'," ")
					if r['EPICS units']!=None:
						pv_rbv.setField('EGU',r['EPICS units'])
					
					pv_rbv.setField('SCAN','1 second')
					mask = makeMask_aa(r['Bit'])
					pv_rbv.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))
					pv_rbv.setExtra('row',r)
					fillEpicsPvFields(pv_rbv,r['EPICS PV Fields'])
					
					epicsdb.append(pv_rbv)



			if (r['EPICS type'].lower() =="m") :
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('mbbo')
					pv.setPvName(e_pvnamestr%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT'," ")
					pv.setField('DOL',"0")
					pv.setField('DTYP','asynUInt32Digital')
					mask = makeMask(r['Bit'])
					pv.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))

					fillMultiBitFields(pv,r['Bitfield Sub-Descriptor'],r['Bit'])
					pv.setExtra('row',r)
					fillEpicsPvFields(pv,r['EPICS PV Fields'])

					epicsdb.append(pv)


				if (re.search('R',r['Field Mode'])!=None):
					pv_rbv=epicspv()
					pv_rbv.setRecType('mbbi')
					pv_rbv.setPvName(e_pvnamestrrbv%(r['Software field name']))
					pv_rbv.setField('DESC',r['Field Description for database'][0:30])
					pv_rbv.setField('DTYP','asynUInt32Digital')
					pv_rbv.setField('INP'," ")
					pv_rbv.setField('SCAN','1 second')
					mask = makeMask(r['Bit'])
					pv_rbv.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))
					fillMultiBitFields(pv_rbv,r['Bitfield Sub-Descriptor'],r['Bit'])

					pv_rbv.setExtra('row',r)
					fillEpicsPvFields(pv_rbv,r['EPICS PV Fields'])
					
					epicsdb.append(pv_rbv)



			if (r['EPICS type'].lower() =="b" or r['EPICS type'].lower() =="bm") :
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('bo')
					pv.setPvName(e_pvnamestr%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT'," ")
					pv.setField('DOL',"0")
					pv.setField('DTYP','asynUInt32Digital')
					mask = makeMask(r['Bit'])
					pv.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))

					fillBitFields(pv,r['Bitfield Sub-Descriptor'])
	
					pv.setExtra('row',r)
					fillEpicsPvFields(pv,r['EPICS PV Fields'])

					epicsdb.append(pv)


				if (re.search('R',r['Field Mode'])!=None):
					pv_rbv=epicspv()
					pv_rbv.setRecType('bi')
					pv_rbv.setPvName(e_pvnamestrrbv%(r['Software field name']))
					pv_rbv.setField('DESC',r['Field Description for database'][0:30])
					pv_rbv.setField('DTYP','asynUInt32Digital')
					pv_rbv.setField('INP'," ")
					pv_rbv.setField('SCAN','1 second')
					mask = makeMask(r['Bit'])
					pv_rbv.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))
					fillBitFields(pv_rbv,r['Bitfield Sub-Descriptor'])

					pv_rbv.setExtra('row',r)
					fillEpicsPvFields(pv_rbv,r['EPICS PV Fields'])
					
					epicsdb.append(pv_rbv)

			
			

			if (r['EPICS type'].lower() =="a") :
				if (re.search('W',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('ao')
					pv.setPvName(e_pvnamestr%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('OUT',"%sLONGOUT PP NMS"%(pv.getPvName()))
					pv.setField('DTYP','Raw Soft Channel')
					
					calcESLO(pv,analog_mult,r['EPICS units'])	
					
					pv.setField('LINR', 'SLOPE')
					#!! how do we set DOL? It seems to set max val...
					#!! need max/min vals in ss.
					pv.setField('PREC', "2")
					

					fillEpicsPvFields(pv,r['EPICS PV Fields'])
					


					pvl=epicspv()
					pvl.setRecType('longout')
					pvl.setPvName("%sLONGOUT"%(pv.getPvName()))
					pvl.setField('DESC',r['Field Description for database'][0:30])
					pvl.setField('OUT'," ")
					pvl.setField('DTYP','asynUInt32Digital')
					mask = makeMask_aa(r['Bit'])
					pvl.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))
					
					
					pv.setExtra('row',r)
					
					
					pvl.setExtra('row',r)
					
					epicsdb.append(pvl)
					epicsdb.append(pv)


				if (re.search('R',r['Field Mode'])!=None):
					pv=epicspv()
					pv.setRecType('ai')
					pv.setPvName(e_pvnamestrrbv%(r['Software field name']))
					pv.setField('DESC',r['Field Description for database'][0:30])
					pv.setField('INP',"%sLONGIN PP NMS"%(pv.getPvName()))
					pv.setField('SCAN','1 second')
					pv.setField('DTYP','Raw Soft Channel')
					
					calcESLO(pv,analog_mult,r['EPICS units'])
						
					
					pv.setField('LINR', 'SLOPE')
					#!! how do we set DOL? It seems to set max val...
					#!! need max/min vals in ss.
					pv.setField('PREC', "2")
					

					
					fillEpicsPvFields(pv,r['EPICS PV Fields'])


					pvl=epicspv()
					pvl.setRecType('longin')
					pvl.setPvName("%sLONGIN"%(pv.getPvName()))
					pvl.setField('DESC',r['Field Description for database'][0:30])
					pvl.setField('DTYP','asynUInt32Digital')
					pvl.setField('INP'," ")
					pvl.setField('SCAN','1 second')
					mask = makeMask_aa(r['Bit'])
					pvl.setAsynSpec(makeAsynSpec('$(PORT)',r['Register Name'],mask))
					

					pv.setExtra('row',r)
					
					pvl.setExtra('row',r)
					
					
					epicsdb.append(pvl)
					epicsdb.append(pv)






		except:
				print "Parsing error"
				print r
				
				print " "
				traceback.print_exc(file=sys.stdout)
				break
				
	
			
	writeEpicsDb(epicsdb,epicsfile);
	
	
	return(epicsdb)		
			

##############################################################################
#
#
# give a pv object, epunits like 'us' from the ss. give analog_mult, from ss as a double
# which is that 10 FPGA ns clock unit at top of ss.
# we fill in ESLO and EGU on pv. this is for analog pvs
##############################################################################
def calcESLO(pv,analog_mult,epunits):
	
	eslo='1.0'
	units=''
	
	if epunits=='us':
		eslo_d=1.0/(1000/analog_mult)
		eslo='%f'%(eslo_d)
		units=epunits
	
	
	elif epunits=='ns':
		eslo_d=1.0/(1.0/analog_mult)
		eslo='%f'%(eslo_d)
		units=epunits
	
	
	elif epunits=='ms':
		eslo_d=1.0/(1000000.0/analog_mult)
		eslo='%f'%(eslo_d)
		units=epunits
	
	
	elif epunits=='s':
		eslo_d=1.0/(1000000000.0/analog_mult)
		eslo='%f'%(eslo_d)
		units=epunits
	
	
	else:
		#search for a ;. If there is a semicolun then we have a raw ESLO and units
		if re.search(';',epunits)!=None:
			eslo=epunits.split(';')[0]
			units=epunits.split(';')[1]
		
	pv.setField('EGU',units)
	pv.setField('ESLO',eslo)
		
		
						

##############################################################################
#
#
#
#
##############################################################################


#fill mbbo/mbbi fileds
def fillMultiBitFields(pv,subdesc,bits):
	#tokenize by ;
	sbd=subdesc.split(';')
	
	#simetimes the ss will end in ; and we get an empty entry in sbd
	#remove the last entry if ==''
	if (sbd[len(sbd)-1]==''):
		del sbd[len(sbd)-1]
	
	
	st=['ZRST','ONST','TWST','THST','FRST','FVST','SXST','SVST','EIST','NIST','TEST','ELST','TVST','TTST','FTST','FFST']
	vl=['ZRVL','ONVL','TWVL','THVL','FRVL','FVVL','SXVL','SVVL','EIVL','NIVL','TEVL','ELVL','TVVL','TTVL','FTVL','FFVL']
	
	
	
	
	
	#bits is 31:14, or just 17. shift is either the lower bit, or the only bit
	b=bits.split("..")
	if (len(b)==1):
		pv.setField('SHFT',b[0])
	
	if (len(b)==2):
		pv.setField('SHFT',b[1])


	for s in sbd:

		spec=s.split(":")
		#spreadsheet may have couples instead of triples.
		#in a triple we have index:text:val, in couple, index=val
		#convert to triple
		if (len(spec)==2):
			spec.append(spec[0])
		
		
		pv.setField(st[int(spec[0])],spec[1])
		pv.setField(vl[int(spec[0])],spec[2])
		

		




##############################################################################
#
#
#
#
##############################################################################


#fill mbbo/mbbi fileds
def fillEpicsPvFields(pv,epicspvf):
	
	#if empty then return
	if epicspvf=='':
		return()
		
	
	#tokenize by ;	
	epf=epicspvf.split(';')
	for s in epf:
		spec=s.split(":")
		pv.setField(spec[0],spec[1])
		

		


##############################################################################
#
#
#
#
##############################################################################


#fill mbbo/mbbi fileds
def fillBitFields(pv,subdesc):
	#tokenize by ;
	sbd=subdesc.split(';')
	
	st=['ZNAM','ONAM']
	
	
	
	
	

	for s in sbd:

		spec=s.split(":")		
		pv.setField(st[int(spec[0])],spec[1])
		

##############################################################################
#
# for bo, bi, mbbo, mbbi and Directs, convert epics fields to 
# ss bitfield subdescriptor
#
##############################################################################

def pvBitFields2ssSubDesc(pv):
	subdesc=None
	rt=pv.getRecType()

	if rt=='bo' or rt=='bi':
	
		
		subdesc='0:%s;1:%s'%(pv.getField('ZNAM'),pv.getField('ONAM'))
	
	

	elif rt=='mbbo' or rt=='mbbi' or rt=='mbboDirect' or rt=='mbbiDirect':


		st=['ZRST','ONST','TWST','THST','FRST','FVST','SXST',
			'SVST','EIST','NIST','TEST','ELST','TVST','TTST','FTST','FFST']
		vl=['ZRVL','ONVL','TWVL','THVL','FRVL','FVVL','SXVL',
			'SVVL','EIVL','NIVL','TEVL','ELVL','TVVL','TTVL','FTVL','FFVL']
	
		subdesc=''

		for k in range(len(st)):
			if pv.getField(st[k])!=None:
				subdesc=subdesc + '%d:%s:%s;'%(k,pv.getField(st[k]),pv.getField(vl[k]))
			

	else:
		#print "ERROR: pv %s not Binary Pv Type"%(pv.getPvName())
		subdesc=''






	return(subdesc)



##############################################################################
#
#
#
#
##############################################################################
		
			
#provide a str of 31 or 31..23
#convert to 0xaaaaAABB where AA is num bits, BB is shift			
			
def makeMask_aa(bits):
	#make sure no ' in the numbers- used in calc and excel to force numbers to act as text
	bits=bits.replace('\'','')
	bits=bits.split('..')
	if len(bits)==1:
		#single bit
		AA=1
		BB=int(bits[0])
		aaaa=0xaaaa0000L
		mask=aaaa + AA*256 + BB
		maskh=re.search('[^L]*',hex(mask)).group(0)		
		return(maskh)
	else:
		#single bit
		AA=1 + int(bits[0]) - int(bits[1])
		BB=int(bits[1])
		aaaa=0xaaaa0000L
		mask=aaaa + AA*256 + BB
		maskh=re.search('[^L]*',hex(mask)).group(0)
		return(maskh)
			
		
		


		

##############################################################################
#
#
# convert 11..2 to 0xf02
#
##############################################################################
			
#provide a str of 31 or 31..23
#convert to 0x???????? pure hex number where AA is num bits, BB is shift			
			
def makeMask(bits):
	#make sure no ' in the numbers- used in calc and excel to force numbers to act as text
	bits=bits.replace('\'','')
	bits=bits.split('..')
	if len(bits)==1:
		#single bit
		
		
		mask=pow(2,int(bits[0]))
		maskh=re.search('[^L]*',hex(mask)).group(0)		
		return(maskh)
	else:
		#single bit
		mask=0L
		for b in range(int(bits[1]),1+int(bits[0])):
			mask = mask + pow(2,b)
			
		maskh=re.search('[^L]*',hex(mask)).group(0)
		return(maskh)
			
		
		

##############################################################################
#
##############################################################################

def pvType2ssType(pvtype):
	
	p2s=dict([
		('ai','A'),
		('ao','A'),
		('bi','B'),
		('bo','B'),
		('mbbi','L'),
		('mbbo','L'),
		('mbbiDirect','L'),
		('mbboDirect','L'),
		('longout','I'),
		('longin','I'),
		('waveform','W')])

	
	return(p2s[pvtype])


##############################################################################
#
# convert str 0xf23 etc to 5..1
#
#
##############################################################################


def getMaskBits(maskh):
	
	
	if isinstance(maskh,str):
		maskh=maskh.replace('L','')
		m=int(maskh,16)
	else:
		m=maskh

	if m&0xffff0000==0xaaaa0000:
		m=m&0xffff
	
	bitlo=-1
	bithi=-1	

	for k in range(32):
		v=pow(2,k)
		if v&m>0 and bitlo==-1:
			bitlo=k

		if v&m>0:
			bithi=k

	if bithi!=bitlo:
		bits='\'%d..%d'%(bithi,bitlo)
	
	else:
		bits='\'%d'%(bitlo)

	return(bits)
			




	
##############################################################################
#
#
#
#
##############################################################################

def makeAsynSpec(port,param,mask):
	
	
	
	asyn=dict()
	asyn['atyp']='asynMask'
	asyn['port']=port
	asyn['address']='0'
	asyn['timeout']='1'
	asyn['mask']=mask
	asyn['param']="reg_%s"%(param)
	return(asyn)



##############################################################################
#
#
#
#
##############################################################################

#reads spreadsheet, gets raw registers and gen epics DB input and/or output pvs
#generates simple epics db with just params and addresses, DESC, RW.
#for simplicity just make long out regs for all entries in spreadsheet, even if they are read ouly
#assume col 0..3 are the raw reg pvs
#db=ssEpicsSoftChan('MDigMap.txt')
def ssEpicsSoftChan(ss_filename):
	
	if isinstance(ss_filename,str):
		ss=spreadsheet()
		ss.readTabText(ss_filename);
	else:
		ss=ss_filename
		


	mycols = [1,2,3,4]
	rows=ss.getColsD(mycols)
	
	
	epicsdb=[]
	for r in rows:
		print r
		if re.search(r'W|R',r['Register Mode'])!=None:
			
			pv=epicspv()
			#set spec of pv fields
			pv.setRecType('longout')
			pv.setPvName("$(P)$(R)reg_%s"%(r['Register Name']))
			pv.setField('DESC',r['Function'])
			pv.setField('DTYP','Soft Channel')
			#save vme addr, as extra info, not written as prt of pv record
			pv.setExtra('vmeaddr',r['Address'])
			#save if R/W 
			pv.setExtra('rw',r['Register Mode'])
			pv.setExtra('param','reg_%s'%(r['Register Name']))

			pv.setExtra('row',r)

			print "adding pv" + pv.getPvName()
			epicsdb.append(pv)
			
		
	
			
	return(epicsdb)
	
	
			




##############################################################################
#
#
#
#
##############################################################################

#reads spreadsheet, gets raw registers and gen epics DB input and/or output pvs
#give tabbed text spreadsheet filename,
#returns list of epicspv() classes with the database.
#give a col number reg expression for which pvs to get- 
#ex ssRawRegEpicsDb(ss_filename,1,'(RW)') to get cols for only RW.
#ex ssRawRegEpicsDb(ss_filename,1,'W') to get cols that have a W ro RW.

#generates asynDig int32 records.
#assume col 0..3 are the raw reg pvs
def ssToRawEpicsDB(ss_filename,epicsfile):

	if isinstance(ss_filename,str):
		ss=spreadsheet()
		ss.readTabText(ss_filename);
	else:
		ss=ss_filename
		


	mycols = [1,2,3,4]
	rows=ss.getColsD(mycols)
	
	epicsdb=[]
	for r in rows:
		#do longout
		if re.search('W',r['Register Mode'])!=None:
			pv=epicspv()
			#set spec of pv fields
			pv.setRecType('longout')
			pv.setPvName("$(P)$(R)reg_%s"%(r['Register Name']))
			pv.setField('DESC',r['Function'][0:30])
			pv.setField('DTYP','asynUInt32Digital')
			pv.setField('OUT',"  ")
			#save vme addr, as extra info, not written as prt of pv record
			pv.setExtra('vmeaddr',r['Address'])
			#setup asyn OUT field
			asyn=dict()
			asyn['atyp']='asynMask'
			asyn['port']='$(PORT)'
			asyn['address']='0'
			asyn['timeout']='1'
			asyn['mask']='0xaaaa2000'
			asyn['param']="reg_%s"%(r['Register Name'])
			pv.setAsynSpec(asyn)
			
			
			#add some junk metadata, so gui maker can deal with it.
			r['Field Mode']= r['Register Mode']
			r['Human field name']=r['Register Name']
			r['EPICS type']='h'
			pv.setExtra('row',r)

			epicsdb.append(pv)
			
		
		#do longin
		if re.search('R',r['Register Mode'])!=None:
			pv=epicspv()
			pv.setRecType('longin')
			pv.setPvName("$(P)$(R)reg_%s_RBV"%(r['Register Name']))
			pv.setField('DESC',r['Function'][0:30])
			pv.setField('DTYP','asynUInt32Digital')
			pv.setField('SCAN','1 second')
			pv.setField('INP',"  ")
			#store the address in vme.. not part of pv rec. but save info
			pv.setExtra('vmeaddr',r['Address'])

			#setup asyn outfield
			asyn=dict()
			asyn['atyp']='asynMask'
			asyn['port']='$(PORT)'
			asyn['address']='0'
			asyn['timeout']='1'
			asyn['mask']='0xaaaa2000'
			asyn['param']="reg_%s"%(r['Register Name'])
			pv.setAsynSpec(asyn)

			#add some junk metadata, so gui maker can deal with it.
			r['Field Mode']= r['Register Mode']
			r['Human field name']=r['Register Name']
			r['EPICS type']='h'
			pv.setExtra('row',r)
			

			epicsdb.append(pv)
	
	
	writeEpicsDb(epicsdb,epicsfile)		
	return(epicsdb)
	
	
			
	
	

##############################################################################
#
#
#
#
##############################################################################


#call as readEpicsDb('gretBoard.template') and list of epicspv objecst is created
#containing all info in the epics database.
def readEpicsDb(filename):
	pvlist=[]
	f=open(filename);
	
	
	stat=0
	k=0
	while(stat==0):
		pvlist.append(epicspv())
		stat=pvlist[k].parseEpicsDb(f)
		
		
		#add some junk metadata, so gui maker can deal with it.
		r={ 'Field Mode': 'RW',  'Human field name': 'dont know',  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'i'}
		
		r['Human field name']=pvlist[k].getPvName()
		
		pvlist[k].setExtra('row',r)
		
		k=k+1
	f.close()	
	return(pvlist);




##############################################################################
#
#
#
#
##############################################################################


def writeEpicsDb(pvlist, filename):
	
	
	if (filename!=None):
		f=open(filename,'w')

		for x in pvlist:
			x.genEpicsDb(f)

		f.close()


#find pvs based on what the asyn spec is, like param, address, mask port etc.
#findAsyn(a,"param","reg_master_logic_status")
#finds all pvs that point to param reg_master_logic_status

def findAsyn(pvlist,afield,aval):
	#get all asyn type pvs
	b=find(pvlist,None,None,"DTYP","asyn")
	
	c=[]
	
	for x in b:
		if re.search(aval,x.getAsynSpec()[afield])!=None:
			c.append(x);

	
	return(c)
		

###########################################################################
#
#find pvs with a given name, OR, rectuype, or a field being some value.
#put None if we dont care.
#b=find(a,None,"(ao)|(bo)|(mbbo)|(longout)",None,None)
#finds those tuype sof records. we insert reg expression for args.
#b=find(a,None,None,'DTYP','asyn'), finds all asyn type records
#b=find(a,"Window",None,None,None) finds all pvs with Window in the name
#use reg exp for pvname, rec type, or field val. fieldname must be exact
#
##########################################################################

def find(pvlist,pvname,rectype,fieldname,fieldval):

	outlist=[]

	if (pvname!=None):
		for p in pvlist:
			if re.search(pvname,p.getPvName())!=None:
				outlist.append(p);
				

	elif (rectype!=None):
		for p in pvlist:
			if re.match(rectype,p.getRecType())!=None:
				outlist.append(p);

				
	else:
		for p in pvlist:
			fv=p.getField(fieldname)
			if (fv!=None):
				if re.search(fieldval,fv)!=None:
					outlist.append(p);
			
	return(outlist);



##############################################################################
#
#
#search c code or any text file. give list of lines, or a filename
#
##############################################################################

def findLines(ff,regx):

	outlist = []
	
	#if a string, we assume iots a filename. else a list.
	
	if isinstance(ff,str):
		f=open(ff,'r')
		#print "opened file %s"%(ff)
	else: 
		f=ff;
	
	for line in f:
		if re.search(regx,line)!=None:
			outlist.append(line);
			
			
	if isinstance(ff,str):
		f.close()
	
	
	return(outlist)



	
##############################################################################
#From asyn cpp drivers find setAddress lines and get regname and address
# as a dictionary. ret tuple of reg2addr and addr2reg to look either way
##############################################################################

def getRegAddressList(ff):
	
	lns=findLines(ff,'setAddress');
	#print "setAddr %d"%(len(a))
	
	reg2addr=dict()
	addr2reg=dict()

	for line in lns:
		try:
			regname = re.search('(?<=\().*(?=,)',line).group(0)
			regname = regname.strip()
			addr= re.search('(?<=0x)[0-9ABCDEFabcdef]*',line).group(0)
			addr = '0x'+addr
			reg2addr[regname]=addr
			addr2reg[addr]=regname
		except:
			print "err " + line

	ans=(reg2addr,addr2reg)

	return(ans)
	
	
	
##############################################################################
#
# give a reg name and cpp file where asyn setAddress is called.
# truens address of the register.
##
# if regname starts with 0x, then we start w/ address and find the regname
##############################################################################

def findRegAddress(ff,regname):
	
	a=findLines(ff,'setAddress');
	#print "setAddr %d"%(len(a))
	
	b=findLines(a,regname);
	#print "regname %d"%( len(b))
	if len(b)>1:
		print "more then one instance for regname"
		return(-1)
	
	if len(b)==0:
		#print "Cound not find regname"
		return(0)
		
	bl=b[0];
	
	#if we gave regname start w/ 0x then we find a regname from address
	if re.search('\A0x',regname)!=None:
		addr = re.search('(?<=\().*(?=,)',bl).group(0)
		#strip whitespace
		addr = addr.strip()
	else:
	
		addr= re.search('(?<=0x)[0-9ABCDEFabcdef]*',bl).group(0)
	
	return(addr)
	
	
##############################################################################
#
#
#
#
##############################################################################


def findExt(pvlist,extname,extval):

	outlist=[]

	
	for p in pvlist:
		fv=p.getExtra(extname)
		if (fv!=None):
			if re.search(extval,fv)!=None:
				outlist.append(p);
			
	return(outlist);

##############################################################################
#
#
#
#
##############################################################################

def findaddr(pvlist,vmeaddr):

	for p in pvlist:
		a=int(p.getExtra('vmeaddr'),16)
		b=int(vmeaddr,16)
		if (a==b):
			return(p)
	return(None)







##############################################################################
#
#
#
#
##############################################################################


#calcout_dig_timestamp="""
#record(calcout, "Dig$(DB)_CV_LiveTS") {
#  field(DESC, "Timesstamp Count= A and B")
#  field(CALC, "A*65536 + B")
#  field(SCAN, "1 second")
#  field(INPA, "$(P)$(R)reg_live_timestamp_lsb_RBV.VAL PP")
#  field(INPB, "$(P)$(R)reg_live_timestamp_msb_RBV.VAL PP")
#}
#
#"""



def makePvLiveTS():
	pv=epicspv()
	pv.setRecType('calcout')
	pv.setPvName('$(P)$(R)CV_LiveTS')
	pv.setField('DESC','Timesstamp Count in seconds')
	#take upper 16 of lsb (32bits) and shift msb by 16 (its a 16 bit reg)
	#we convert 10ns to 1s
	#pv.setField('CALC','65536*0.00000001*(ABS(B)*65536.0 + ABS(A)/65536.0)')
	pv.setField('CALC','(((A&2147483647)>>16) + ABS(A>>31)*32678 +(B<<16))/1525.8')
	pv.setField('SCAN','1 second')
	pv.setField('INPA','$(P)$(R)reg_live_timestamp_lsb_RBV.VAL PP')
	pv.setField('INPB','$(P)$(R)reg_live_timestamp_msb_RBV.VAL PP')
	
	r={ 'Field Mode': 'R',  'Human field name': 'Time Stamp',  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'i'}
	pv.setExtra('row',r)
	
	return(pv)



###################################################################################
#
# converts 16 bits from insigned to signed short...
#
##################################################################################

def makeSignShort(pvn,inpt,opt):
	pv=epicspv()
	pv.setRecType('calcout')
	pv.setPvName(pvn)
	pv.setField('DESC','conv ushort to short')
	#
	#reintrepret as signed short
	pv.setField('CALC',' (A&32767) - (A&32768)')
	pv.setField('SCAN','1 second')
	pv.setField('INPA',inpt)
	pv.setField('OUT',opt)
	
	
	r={ 'Field Mode': 'R',  'Human field name': 'Time Stamp',  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'i'}
	pv.setExtra('row',r)
	
	return(pv)





	
#	record(bi, "DAQB$(DB)_CV_Running") {
#  field(DESC, "Status: DAQ on")
#  field(ZNAM, "Stopped")
#  field(ONAM, "Running")
#}
	
	

def makeCVRunning():
	pv=epicspv()
	pv.setRecType('bi')
	pv.setPvName('$(P)$(R)CV_Running')
	pv.setField('DESC','Tells if DAQ runs')
	#take upper 16 of lsb (32bits) and shift msb by 16 (its a 16 bit reg)

	pv.setField('ZNAM','Stopped')
	pv.setField('ONAM','Running')
	
	r={ 'Field Mode': 'R',  'Human field name': 'DAQ Running',  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'i'}
	pv.setExtra('row',r)
	
	return(pv)



def makeSoftAo(pvname,desc,sval,lives):
	pv=epicspv()
	pv.setRecType('ao')
	pv.setPvName(pvname)
	pv.setField('DESC',desc)
	pv.setField('DTYPE','Soft Channel')
	pv.setField('PINI','YES')
	pv.setField('VAL',sval)
	pv.setField('PREC','3')
	pv.setExtra('live_on',lives)

	#take upper 16 of lsb (32bits) and shift msb by 16 (its a 16 bit reg)

	
	
	r={ 'Field Mode': 'W',  'Human field name': desc,  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'a'}
	pv.setExtra('row',r)
	
	return(pv)



def makeSoftBo(pvname,desc,sval,znam,onam,lives):
	pv=epicspv()
	pv.setRecType('bo')
	pv.setPvName(pvname)
	pv.setField('DESC',desc)
	pv.setField('DTYPE','Soft Channel')
	pv.setField('PINI','YES')
	pv.setField('VAL',sval)
	
	pv.setField('ZNAM',znam)

	pv.setField('ONAM',onam)

	pv.setExtra('live_on',lives)

	#take upper 16 of lsb (32bits) and shift msb by 16 (its a 16 bit reg)

	
	
	r={ 'Field Mode': 'W',  'Human field name': desc,  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'b'}
	pv.setExtra('row',r)
	
	return(pv)





def makeSoftLongin(pvname,desc):
	pv=epicspv()
	pv.setRecType('longin')
	pv.setPvName(pvname)
	pv.setField('DESC',desc)
	pv.setField('DTYPE','Soft Channel')
	pv.setField('SCAN','1 second')
	

	#take upper 16 of lsb (32bits) and shift msb by 16 (its a 16 bit reg)

	
	
	r={ 'Field Mode': 'R',  'Human field name': desc,  'Database Group': 'B',  'Address': '0x0000', 'EPICS type':'i'}
	pv.setExtra('row',r)
	
	return(pv)


	

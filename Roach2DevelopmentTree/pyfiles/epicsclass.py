import re
import copy


'''

pv = epicsclass.epicspv()
pv.listFields()
pv.printEpicsDb()
pv.setPvName('IOC:aaa')
pv.printEpicsDb()

pv.setRecType('ao')
pv.setField('DTYP','Soft Channel')
pv.setField('PINI','YES')
pv.setField('VAL','1.0')
pv.setField('SCAN','1 second')
pv.printEpicsDb()



'''

#calc that incremest every 1sec
def makeCounterPV(pvname):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('calc')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('PINI','NO')
    pv.setField('VAL','0')
    pv.setField('INPA','1')
    pv.setField('CALC','A; A:=A+1')
    pv.setField('SCAN','1 second')
    
    return(pv)

def makeSoftAo(pvname):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('ao')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('PINI','NO')
    pv.setField('VAL','0.0')
   
    return(pv)
    
def makeSoftAi(pvname):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('ai')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('PINI','NO')
    pv.setField('VAL','0.0')
    pv.setField('SCAN','I/O Intr')
    return(pv)
    


def makeSoftLongout(pvname):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('longout')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('PINI','NO')
    pv.setField('VAL','0')
   
    return(pv)
    

def makeSoftLongin(pvname):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('longin')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('PINI','NO')
    pv.setField('VAL','0')
    pv.setField('SCAN','I/O Intr')
    return(pv)


def makeCharWaveform(pvname,nelm = 256):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('waveform')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('NELM','%f'%(nelm))
    pv.setField('FTVL','CHAR')
    return(pv)

def makeFloatWaveform(pvname,length=2048):
    pv = epicspv()   
    pv.setPvName(pvname) 
    pv.setRecType('waveform')  
    pv.setField('DTYP','Soft Channel')   
    pv.setField('NELM','%i'%(length))
    pv.setField('FTVL','FLOAT')
    return(pv)
    
    
#pvname string
#{'string':integer . etc...}

def makeSoftMBBO(pvname,mbdict):
    states=['ZRST','ONST','TWST','THST','FRST','FVST' ,'SXST' ,'SVST' ,
        'EIST' ,'NIST','TEST']
    values = ['ZRVL','ONVL','TWVL','THVL','FRVL','FVVL' ,'SXVL' ,'SVVL' ,
        'EIVL' ,'NIVL','TEVL']
    pv = epicspv()
    pv.setPvName(pvname) 
    pv.setRecType('mbbo')  
    pv.setField('DTYP','Soft Channel')   
   
  
  
    
    for stringitem in mbdict.keys():
        val = mbdict[stringitem]
        stfield = states[val]
        svfield = values[val]
        pv.setField(stfield,stringitem)
        pv.setField(svfield,val)
        
    return(pv)    


def makeSoftMBBI(pvname,mbdict): 
    pv = makeSoftMBBO(pvname,mbdict)  
    pv.setRecType('mbbi')    
    pv.setField('SCAN','I/O Intr')        
    return(pv)    


class epicspv:

	
	def __init__(self):
		#pv fie;ds
		self.fieldlist=dict()
		#extra info about pv not written to pv record. such as comments, address etc.
		self.extralist=dict()
		#rectype and pv name as strings
		self.rectype=''
		self.pvname=''
		
		#bunch of parsing.
		self.s_record=re.compile(r"^\s?record")
		self.s_openbrace=re.compile(r"{")
		
		self.s_closebrace=re.compile(r"}")
		
		self.s_commaleft= re.compile(r".*(?=,)")
		self.s_commaright= re.compile(r"(?<=,).*")
		
		
		self.s_inquotes=re.compile(r"(?<=\").*(?=\")")

		self.s_field=re.compile(r"\s?field")
		
		
		self.s_outrec=re.compile(r'(ao)|(bo)|(mbbo)|(bo)|(longout)|(mbboDirect)|(stringout)')
		self.s_inrec=re.compile(r'(ai)|(bi)|(mbbi)|(bi)|(longin)|(mbbiDirect)|(stringin)')
		self.s_textnum=re.compile(r'\w*')
		
		self.s_inparen=re.compile(r'(?<=\().*(?=\))')
		#strip white from ends? for now use this...
		self.s_pvchars=re.compile('[\w$()@:_]*')
		
		self.s_at=re.compile(r'(?<=@)\w*')
		
		self.s_lastword=re.compile(r'\w+\s?$')
		
		self.s_stripnumber=re.compile(r'.*(?=[0-9]$)')
		
		self.s_striprbv=re.compile(r'.*(?=_RBV)')
		
	
	def deepcopy(self):
		p=epicspv()
		p.fieldlist=copy.deepcopy(self.fieldlist)
		p.extralist=copy.deepcopy(self.extralist)
		p.rectype=copy.deepcopy(self.rectype)
		p.pvname=copy.deepcopy(self.pvname)
		return(p)
	
	def printEpicsDb(self):
		print " "
		
		print "record(%s,\"%s\")"%(self.rectype,self.pvname)
		print "{"
		
		for f in self.fieldlist:
			print "field(%s,\"%s\")"%(f,self.fieldlist[f])

		print "}"
		print " "
				
	

	def genEpicsDb(self,fileobj):
		
		
		fileobj.write(" \n");
		
		fileobj.write("record(%s,\"%s\")\n"%(self.rectype,self.pvname))
		fileobj.write("{\n")
		
		for f in self.fieldlist:
			fileobj.write("  field(%s,\"%s\")\n"%(f,self.fieldlist[f]))

		fileobj.write( "}\n")
		fileobj.write( " \n")
				


	#provide a stream- so we can read line.. pr file pointer. 
	# looks for record, fils out record then retuns
	# at eof ret -1, or if cannot parse. 
	def parseEpicsDb(self,fileobj):
		#look for record
		try:
			line = fileobj.readline();print line
			N=0
			stat=0

			while (self.s_record.search(line)==None):
				line = fileobj.readline(); print line
				N=N+1
				if (N>100):
					print "cannot find record in 100 lines"
					stat=1
					break;


			#found record
			#get what is in ()
			d=self.s_inparen.search(line).group(0)

			cr=self.s_commaright.search(d).group(0)

			#just get txt chars and spec pv chars
			self.pvname=self.s_inquotes.search(cr).group(0)



			#get left of comma
			cl = self.s_commaleft.search(d).group(0)
			#get alpha text
			self.rectype = self.s_textnum.search(cl).group(0)



			#search for {
			N=0
			while (self.s_openbrace.search(line)==None):
				line = fileobj.readline();print line
				N=N+1
				if (N>100):
					print "cannot find { in 100 lines"
					stat=1
					break;

			#now inside pv record

			not_done = True
			N=0
			while(not_done):

				#look for field
				if (self.s_field.search(line)!=None):
					#get what is in paran
					p=self.s_inparen.search(line).group(0)

					#get left of ,
					f = self.s_commaleft.search(p).group(0)
					#get text chars only
					f_type = self.s_textnum.search(f).group(0)
					#get right of ,
					f = self.s_commaright.search(p).group(0)
					#get what is in ""
					f_data = self.s_inquotes.search(f).group(0)
					self.fieldlist[f_type]=f_data



				#look for ?
				if (self.s_closebrace.search(line)!=None):
					print "Found end of pv record"
					not_done=False
					stat=0
				else:
					line = fileobj.readline();print line
					if len(line)==0:
						print "EOF"
						stat=1
						break
					N=N+1
					if (N>100):
						print "record is 100+ lines long!!!"
						stat=1
						break;
						
						
		
		except:
			print "end of file "
			stat=1
					
		return(stat)
		
		
	
	def listFields(self):
		for f in self.fieldlist:
			print "%s : %s\n"%(f,self.fieldlist[f])
		
	
	def setField(self,f,val):
		self.fieldlist[f]=val
	
	def getField(self,f):
		
			a=self.fieldlist.get(f)
			return(a)
		
		
	
	
	def listExtra(self):
		for f in self.extralist:
			print "%s : %s\n"%(f,self.extralist[f])
		
	
	def setExtra(self,f,val):
		self.extralist[f]=val
	
	def getExtra(self,f):
		
			a=self.extralist.get(f)
			return(a)
		
		



	def setRecType(self,r):
		self.rectype=r
		
	def getRecType(self):
		return(self.rectype)
		
	def setPvName(self,n):
		self.pvname=n
		
	def getPvName(self):
		return(self.pvname)
		
	
	
	def isRBV(self):
		n=self.getPvName()
		rbv=self.s_striprbv.search(n)
		if rbv!=None:
			return(True)
			
		return(False)
		
		
		
	def getPvNameStrRBV(self):
		n=self.getPvName()
		rbv=self.s_striprbv.search(n)
		if rbv!=None:
			return(rbv.group(0))
			
		return(None)
		
		
		
	


	def getAsynSpec(self):
	
	        if self.getField('DTYP')==None:
	                return(None)
	       
		if (re.search(r'asyn',self.getField('DTYP')) == None):
			return(None)
			
			
		if (self.fieldlist.get("OUT")!=None):
			asyntxt=self.fieldlist.get("OUT");
		
		
		if (self.fieldlist.get("INP")!=None):		
			asyntxt=self.fieldlist.get("INP");
			
		if (asyntxt==None):
			print "No INP or OUT"
			return(None)
		
		asyn=dict()
		#get what is after @
		asyn['atyp']=self.s_at.search(asyntxt).group(0)
		#get param name. last ord in the line
		asyn['param']=self.s_lastword.search(asyntxt).group(0)
		#get stuff in ()
		p=self.s_inparen.search(asyntxt).group(0)
		#split by ,
		pl=p.split(',')
		if (len(pl)==3):
			asyn['port']=pl[0]
			asyn['address']=pl[1]
			asyn['timeout']=pl[2]
		else:
			asyn['port']=pl[0]
			asyn['address']=pl[1]
			asyn['mask']=pl[2]
			asyn['timeout']=pl[3]
			
		return(asyn)
		
		
		
	def setAsynSpec(self,asyn):
		if (len(asyn)==6):
			asyntxt="@%s(%s,%s,%s,%s)%s"%(asyn['atyp'],asyn['port'],asyn['address'],asyn['mask'],asyn['timeout'],asyn['param'])
				
			
		if (len(asyn)==5):
			asyntxt="@%s(%s,%s,%s)%s"%(asyn['atyp'],asyn['port'],asyn['address'],asyn['timeout'],asyn['param'])
				
		
				
		if (self.fieldlist.get("OUT")!=None):
			self.fieldlist['OUT']=asyntxt
		
		
		if (self.fieldlist.get("INP")!=None):		
			self.fieldlist['INP']=asyntxt

		
	
	def isChanPv(self):
		#asyn=self.getAsynSpec()
		#if (asyn!=None):
		#	baseparam=self.s_stripnumber.search(asyn['param'])
		#	if (baseparam!=None):
		#		return(True)
			
		#return(False)
		nn=self.getPvName()
		
		n=self.s_striprbv.search(nn)
		
		if (n!=None):
			nm=n.group(0)
		else:
			nm=self.getPvName()
			
		
		baseparam=self.s_stripnumber.search(nm)
		if (baseparam!=None):
				return(True)

		return(False)
		
		
		
	def getBaseName(self):
#		asyn=self.getAsynSpec()
#		if (asyn!=None):
#		    baseparam=self.s_stripnumber.search(asyn['param'])
#		    if (baseparam!=None):
#			    return(baseparam.group(0))
#			
#		return(None)
		
		n=self.s_striprbv.search(self.getPvName())
		if (n!=None):
			nm=n.group(0)
		else:
			nm=self.getPvName()
			
		baseparam=self.s_stripnumber.search(nm)
		if (baseparam!=None):
				return(baseparam.group(0))

		return('')
		

	
	def makeChanName(self,macro):
		n=self.getBaseName()
		
		
		n=n+macro
		
		if self.isRBV():
			n=n+'_RBV'
			
		return(n)
		

	def isOutRec(self):

		if (self.s_outrec.search(self.getRecType()) != None):
			return(True)
			
		return(False)
		

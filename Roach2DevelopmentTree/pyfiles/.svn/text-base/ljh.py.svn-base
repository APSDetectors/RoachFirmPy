import numpy;
import struct;

"""

#
#This class reads NIST data files and stores into a hierarchical python dictionary, similar to how h5py works.
# The dictionary is in myobhect.header, and can be addressed with the [].
# waveform data is stored in this hierarchy in the dictionary.
# for ease of use, there are some helper functions to get the waveform data as numpy arrays
#


#here is the most common way to get data, easist method.



execfile('ljh.py')
filename='/home/oxygen26/TMADDEN/ROACH/NistDevData/2011_07_13_G_chan1.ljh'
aa=LJH(filename)


#this reads the header AND the actual data
aa.readData()

#show how many channes are in the file. returns an int from 1 to N
aa.numChannels()
#get num of waveforms for channel 0, chans number from 0.
aa.numRecords(0)


#to know length of a waveform record for channel 0

aa.getRecLen(0)
	
    
    	




#now we get pulses from the file and plot. we get pulses from channel 0, pulse number from 0 to N-1
#get data from chan 0, waveform 0.
myarray=aa.getRecord(0,0)

#get several pulses from chan 0 and plot

clf();
plot(aa.getRecord(0,0))
plot(aa.getRecord(0,1))
plot(aa.getRecord(0,2))
plot(aa.getRecord(0,3))



#
# For noise files, you may want to put all data records into one long array. 
# For channel 0, get all waveform data as one long numpy array:
#we call as joinRecords(chan, skip_samples, get_samples)
# in this way we can skip data at start of the file, and grab seom number of saples.
# We can only skip whole records and return whole records, so if record length is 3072, then we can get samples in mult of 3072.
# we do not read half records.   

#to read 10000 samples starting from the beginnging of the data, for channel 0
noise = aa.joinRecords(0,0,10000)
clf()
plot(noise)



#to read 200000 samples, skipping the 1st 50000 samples,for channel 0
noise = aa.joinRecords(0,50000,200000)
clf()
plot(noise)


#to read to end of file, put in a huge number for num samples, It will rad to end of file and return

noise=aa.joinRecords(0,46220000,1e9)
clf()
plot(noise)


#
# putting ALL data into one long array could take forever. It is not very efficient...for 15k records of 3k long, we get 45M samples
# Do not attempt to make such a long array


#
#To see info in the haeader read on:
#



execfile('ljh.py')
filename='/home/oxygen26/TMADDEN/ROACH/NistDevData/2011_07_13_G_chan1.ljh'
aa=LJH(filename)

#only reads header, not data. aa.readData() reads header AND data. So you can only call aa.readData()
# if the file is long, aa.readData() may take a long time. aa.readHeader() returns quickly as it only reads header.
aa.readHeader()
#show what is in header. prints header and values on screen.
#you can copy/paste what is printed from ls() to get data from header
aa.ls()

# the header is a dict() item in our object. you can print header like this too:
#if there is waveform data it will print and print and print. 
aa.header



#the file is read in a s hierracchical dict item or dict or dict's.
#waveform data is read in as short waveform vectors. it appeadrs a s list in the 
#header as a list of numpy.arrys. the 0th waveform is a numpy array called as
aa.header['Digitizer']['1']['Channel']['0']['Data'][0]
#you can copy.paste from the aa.ls() command to get data from the header.

#for easier method to get waveform data see below... 



"""



    



class LJH:


    def __init__(self,fn):


	
	self.header=dict()
	self.header['Digitizer']=dict()
	
	
	self.data=dict()
	self.filename = fn
	self.fp=0
	

	#count channels found in header
	self.channel_counter=0;
	#keep track of path in the dict for each foujnd channel. binary data indices by found channel
	#then we can find the channel header info and dig info based on fourn chann number
	self.channel_list = []
	
	
    def readHeader(self):
        self.readHeader2()
	self.fp.close()
	
	
    def readHeader2(self):
        description=""
	comments=""
	self.fp=open(self.filename,'rb')
	
	
	rline=self.fp.readline();
	
	while(rline.find("#End of Header")==-1):
	
	    print "top  " + rline
	
		
		
	    
	    #begin muiltu line comment
	    if rline.lower().find("description of this file")!=-1:
	    
	    	
	    	tolkens=rline.split(":")
		description=description + tolkens[1] + "\n"
		rline=self.fp.readline();
		
		while (rline.lower().find("end of description")==-1):
		    print "DESC " + rline
		    description=description + rline + "\n"
		    rline=self.fp.readline();
		    
		    
	    
	    #beginning of dig desc
	    	
	    elif rline.find("Digitizer:")!=-1:
		while rline.find("Digitizer:")!=-1:

		    print "Foudn digitizer!"
	    	    tolkens=rline.split(":")
		    whichdig =  '%d'%(int(self.toFloat(tolkens[1])))
		    self.header['Digitizer'][whichdig]=dict()
		    self.header['Digitizer'][whichdig]['Channel']=dict()
		    
		    rline=self.fp.readline();
		    is_done_desc = ( (rline.find("Digitizer:")!=-1) or \
			    (rline.find("Channel:")!=-1)  or \
			    (rline.lower().find("description of this file")!=-1) or \
			    (rline.find("#End of Header")!=-1) );
		
		    print "is_done_desc = %d"%(is_done_desc)
		    while ( is_done_desc==False):
			print "DIG " + rline
			tolkens=rline.split(":")
			self.header['Digitizer'][whichdig][tolkens[0]]=self.toFloat(tolkens[1])
			rline=self.fp.readline();
		        is_done_desc = ( (rline.find("Digitizer:")!=-1) or \
			    (rline.find("Channel:")!=-1)  or \
			    (rline.lower().find("description of this file")!=-1) or \
			    (rline.find("#End of Header")!=-1) );
		    
		    
	    elif rline.find("Channel:")!=-1:
		while rline.find("Channel:")!=-1:

		    print "Found channel"
	    	    tolkens=rline.split(":")
		    chandig=tolkens[1].split('.')
		    
		    whichdig = '%d'%(int(self.toFloat(chandig[0])))
		    whichchan = '%d'%(int(self.toFloat(chandig[1])))
		    
		    self.header['Digitizer'][whichdig]['Channel'][whichchan]=dict()
		    self.header['Digitizer'][whichdig]['Channel'][whichchan]['FoundNumber']=self.channel_counter
		    self.header['Digitizer'][whichdig]['Channel'][whichchan]['Data']=[]
		    
		    self.channel_counter=self.channel_counter+1;
		    
		    self.channel_list.append(['Digitizer',whichdig,'Channel',whichchan])
		    rline=self.fp.readline();
		    is_done_desc = ( (rline.find("Digitizer:")!=-1) or \
			    (rline.find("Channel:")!=-1)  or \
			    (rline.lower().find("description of this file")!=-1) or \
			    (rline.find("#End of Header")!=-1) );
	
		    while ( is_done_desc==False):
			print "Chan " + rline
			tolkens=rline.split(":")
			self.header['Digitizer'][whichdig]['Channel'][whichchan][tolkens[0]]=self.toFloat(tolkens[1])
			rline=self.fp.readline();
			is_done_desc = ( (rline.find("Digitizer:")!=-1) or \
			    (rline.find("Channel:")!=-1)  or \
			    (rline.lower().find("description of this file")!=-1) or \
			    (rline.find("#End of Header")!=-1) );

		    	    
	    elif rline[0] =='#':
	    	print rline
	    	comments=  comments + rline + "\n"
		rline=self.fp.readline();
	    	
	    elif rline.find(":")>-1:
	        tolkens=rline.split(":")
		self.header[tolkens[0]]=self.toFloat(tolkens[1])
		
	        rline=self.fp.readline();
	    
	    else: 
		pass;    	
   
 	
	
	self.header['description']=description  
 	self.header['comments']=comments  
	
		

	
	
	
    
    def toFloat(self,str):
    	try:a=float(str)
	except:a=str
	
	return(a)
    
    
    
    def readWave(self):
    
    	#
	# read bin header data
	#
	self.bindata = self.fp.read(6)
	
	if len(self.bindata)<6:
	    return(False);
	
	
	
	self.binheader  = struct.unpack('BBHH',self.bindata)
	self.zero=self.binheader[0]
	self.binchan=self.binheader[1]
	self.bints=self.binheader[2] + 65536*self.binheader[2] 
	
	#print 'zero %d chan %d ts %d'%(self.zero, self.binchan, self.bints)
	
	
	#
	# figure out how long waveform is
	#
	
	headerlocation = self.channel_list[self.binchan]
	
	self.numsamples = int(self.header[headerlocation[0]][headerlocation[1]]['Total Samples'])
	self.bytes_per_sample = int(self.header['Digitized Word Size in bytes'])


	#
	# Read waveform
	#
	
	self.bindata=self.fp.read(self.bytes_per_sample * self.numsamples)
	
	
	if len(self.bindata)<(self.bytes_per_sample * self.numsamples):
	    return(False);
	
	
	
	
	wavelist = struct.unpack('%dH'%(self.numsamples),self.bindata)
	self.wave=numpy.array(wavelist)
	wavelist = self.header[headerlocation[0]][headerlocation[1]][headerlocation[2]][headerlocation[3]]['Data']
	wavelist.append(self.wave)
	
	
	
	return(True)
	
    
    def ls2(self,parent,pname,level):
        
	
        if level>5: return
	
	#print 'level %d'%(level)
	
	print pname
	
	
	try:
	    dirs=parent.keys()
	    for d in dirs:
	        pname2='%s[\'%s\']'%(pname,d)
		parent2=parent[d]
		self.ls2(parent2,pname2,level+1)
	   
	except:
	    #no keys, so it must be a float or list or array or something
	    
	    #see if it is a list
	    islist = type(parent) is list
	    
	    if islist==False:
	        print parent 
	    else:
	        print "List of length %d"%(len(parent))
	
    
    def ls(self):
    
    	
        
	parent=self.header
	pname ='.header'
	
	
	
	self.ls2(parent,pname,0)
    
    
    def readData(self):
    
        self.readHeader2()
	
	self.wavecounter=0;
	
	while(self.readWave()):
	    self.wavecounter=self.wavecounter+1
	    #print self.wavecounter
	
	print "Read %d records"%(self.wavecounter)
	self.fp.close()
	
    
    def numChannels(self):
        return(len(self.channel_list))
    
    
    def getRecord(self,channelfoundnum,recnum):
    
    	headerlocation = self.channel_list[channelfoundnum]
        wavelist = self.header[headerlocation[0]][headerlocation[1]][headerlocation[2]][headerlocation[3]]['Data']
	return(wavelist[recnum])

    def numRecords(self,channelfoundnum):
       	headerlocation = self.channel_list[channelfoundnum]
        wavelist = self.header[headerlocation[0]][headerlocation[1]][headerlocation[2]][headerlocation[3]]['Data']
	return(len(wavelist))
	

    def getRecLen(self, chan):
    	reclen = len(self.getRecord(chan,0))
	return(reclen)
	
    def joinRecords(self,chan,skipsamples,numsamples):
    
    	
	
	reclen = self.getRecLen(chan)
	skiprecs = int(float(skipsamples)/float(reclen))
	getrecs = int(1.0 + float(numsamples)/float(reclen))
	
	print "skipping %d records, getting %d records"%(skiprecs,getrecs)
	
	noise = numpy.array([])
	for k in range(skiprecs,(skiprecs+getrecs),1):
	    
	    try: noise = numpy.append(noise, self.getRecord(chan,k))
	    except: break
	    
	print "Num samples retuirned %d"%(len(noise))
	return(noise)
	
	
	
    
    	
	

filename='/home/oxygen26/TMADDEN/ROACH/NistDevData/2011_07_13_G_chan1.ljh'

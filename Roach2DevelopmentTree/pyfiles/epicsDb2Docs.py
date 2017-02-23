"""


db = readDb('pco.template')
printDb(db)

dbToHtmlDoc(db)
#open table.html

"""


import copy

execfile('epicsclass.py')


#read template file, make list of epics pv obhs
def readDb(filename):
    epicsdb = []
    f=open(filename,'r')
    
    
    stat =0
    while(stat==0):
        pv = epicspv()
        stat = pv.parseEpicsDb(f)
        if stat==0:
            epicsdb.append(pv)

    return(epicsdb)
    
 
#print epics database   
def printDb(db):
    for pv in db:
        pv.printEpicsDb()


def writeDb(db,filename):
    fp = open(filename,'w')
    for pv in db:
        pv.genEpicsDb(fp)
  
    fp.close()
    
                
#group pvs and corresponding RBV pvs in tuples. return list of tuples
def groupDbRBV(db):                
    dbgr = []

   
    dbfound = []
    for pv in db:
        #make sure we have not alreayd dealt with this pv
        print pv.getPvName()
        if pv not in dbfound:
            #we have a fresh pv not already grouped.
            dbfound.append(pv)
            
            #see if we have correspopngind RBV PV, or Non RBV PV.
            if pv.isRBV():
                #find non rbv pv
                print 'isrbv'
                pname = pv.getPvNameStrRBV()
                pv2 = findPv(db,pname)
                if pv2!=None:
                    tup=(pv,pv2)
                    dbfound.append(pv2)
                    print 'found nonrbv'
                    
                else:
                    tup = (pv,)
            else:         
                pname = pv.getPvName()+'_RBV'
                pv2 = findPv(db,pname)
                print 'not rbv'
                if pv2!=None:
                    tup=(pv,pv2)
                    dbfound.append(pv2)
                    print 'fiound rbv'
                    
                else:
                    tup = (pv,)
                    
            dbgr.append(tup)
                    
    return( dbgr  )
                
        
    

def findPv(db,namestr):
    for pv in db:
        if namestr==pv.getPvName():
            return(pv)    
    return(None)
    


def dbToHtmlDoc(db,filename='table.html'):
    html=[]
    dbgrp = groupDbRBV(db)
    
    #start table
    html.append('<table style="text-align: left; height: 1522px; width: 1106px;" border="1" cellpadding="2" cellspacing="2">')  
    #start body
    html.append('<tbody>')
    
    #headings
    html.append('<tr>')
    html.append('<td colspan="8" align="center"> <b>Parameter Definitions in andorCCD.h and EPICS Record Definitions in andorCCD.template</b> </td>')
    html.append('</tr>')
    html.append('<tr>')
    html.append('<th> Parameter index variable</th>')
    html.append('<th> asyn interface</th>')
    html.append('<td style="vertical-align: top;"></td>')
    html.append('<th> Access</th>')
    html.append('<th> Description</th>')
    html.append('<th> drvInfo string</th>')
    html.append('<th> EPICS record name</th>')
    html.append('<th> EPICS record type</th>')
    html.append('</tr>')
    
    #go thru PVs
    
    for pvg in dbgrp:
        
        print pvg[0].getPvName()
        html.append('<tr>')
        asynspec = pvg[0].getAsynSpec()
       
        if asynspec!=None:
            html.append('<td>%s<br>'%(asynspec['param']))
        else:
            html.append('<td> N/A <br>')
            
        html.append('</td>')
        
        
        html.append('<td> %s</td>'%( pvg[0].getField('DTYP') ))
        html.append('<td style="vertical-align: top;"></td>')
        
        if len(pvg)==2:
            html.append('<td> WR</td>')
        else:
            if 'out' in pvg[0].getRecType():
                html.append('<td> W</td>')
            else:
                html.append('<td> R</td>')
        
        html.append('<td> Descripttion <br>')
        html.append('</td>')
        if asynspec!=None:
            
            html.append('<td>%s<br>'%(asynspec['param']))
        else:
            html.append('<td> N/A <br>')
            
        html.append('</td>')
        
        if len(pvg)==1:
            html.append('<td> %s</td>'%(  pvg[0].getPvName()))
            html.append('<td>%s</td>'%(pvg[0].getRecType()))
        else:
            html.append('<td> %s\r\n%s</td>'%(  pvg[0].getPvName() , pvg[1].getPvName()))
            html.append('<td>%s\r\n%s</td>'%(pvg[0].getRecType(),pvg[1].getRecType()))     
       
        html.append('</tr>')
    #end body
    html.append('</tbody>')
    #end table
    html.append('</table>')                        

   
    f = open(filename,'w')
    for line in html:
        f.write(line + '\n')
    f.close()
    
    return( html )
"""

execfile('agt33250A.py')

agt=agt33250A()

agt.open()

agt.write('*IDN?\n')

agt.readline()

agt.setOutOn(1)

agt.getId()

agt.setVolts(2.7)

agt.getVolts()



agt.close()




"""
import serial


class agt33250A:

    def __init__(self):
    
        self.dev = "/dev/ttyUSB0"
        
        self.portnum = 8
        
    def open(self):
        
        self.comport = serial.Serial(self.dev)
        
    def getId(self):
    
        self.write('*IDN?\n')

        return(self.readline())

        
        
        
    def close(self):
        
        self.comport.close()
        
    def write(self,c):
        self.comport.write(c)
        
    def setVolts(self,v):
    
        self.write('VOLT %f\n'%v)
    
    
    def setOutOn(self,ison):
    
        if ison:
            self.write('OUTP ON\n')
        else:
            self.write('OUTP OFF\n')
    def setRamp(self):
        self.write('FUNC RAMP\n')

    def getFunc(self):
        self.write('FUNC? \n')
        return(self.readline())

 
    def setFreq(self,f):
        self.write('FREQ %f\n'%f)
 
 
    def getFreq(self):
        self.write('FREQ?\n')
        return(self.readline())

    def getVolts(self):
        self.write('VOLT?\n')
        v=float(self.readline())
        return(v)
               
    def readline(self):
        rsp = self.comport.readline()
        return(rsp)
    
    
    
    
    
    
    

class agtNULL:

    def __init__(self):
    
        self.dev = "null"
        
        self.portnum = 8
        
    def open(self):
        pass
        
        
    def getId(self):
    
        

        return('NULL Vsource')

        
    def setRamp(self):
        pass

    def getFunc(self):
        pass

 
    def setFreq(self,f):
        pass
 
 
    def getFreq(self):
        pass
    
    
        
        
    def close(self):
        
        pass
        
    def write(self,c):
        pass
        
    def setVolts(self,v):
    
        pass
    
    
    def setOutOn(self,ison):
        pass
    
    
    def getVolts(self):
        
        return(0.0)
               
    def readline(self):
       
        return('')
    
print "Loaded agt33250A.py"

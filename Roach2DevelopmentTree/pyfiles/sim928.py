"""

execfile('sim928.py')

sim=sim928()

sim.open()

sim.write('*IDN?\n')

sim.readline()

sim.setOutOn(1)

sim.getId()

sim.setVolts(2.7)

sim.getVolts()

sim.connport(8)

sim.disconnport()

sim.close()




"""
import serial


class sim928:

    def __init__(self):
    
        self.dev = "/dev/ttyS0"
        
        self.portnum = 8
        
    def open(self):
        
        self.comport = serial.Serial(self.dev)
        
    def getId(self):
    
        self.write('*IDN?\n')

        return(self.readline())

        
    def connport(self,pn):
        self.portnum = pn
        self.comport.write('CONN %d,"xyz"\n'%self.portnum)
    
    
    def disconnport(self):
        self.comport.write('xyz\n')
        
        
    def close(self):
        
        self.comport.close()
        
    def write(self,c):
        self.comport.write(c)
        
    def setVolts(self,v):
    
        self.write('VOLT %f\n'%v)
    
    
    def setOutOn(self,ison):
    
        if ison:
            self.write('OPON\n')
        else:
            self.write('OPOF\n')
    
    
    
    def getVolts(self):
        self.write('VOLT?\n')
        v=float(self.readline())
        return(v)
               
    def readline(self):
        rsp = self.comport.readline()
        return(rsp)
    
    
    
    
    
    
    

class simNULL:

    def __init__(self):
    
        self.dev = "null"
        
        self.portnum = 8
        
    def open(self):
        pass
        
        
    def getId(self):
    
        

        return('NULL Vsource')

        
    def connport(self,pn):
        pass
    
    
    def disconnport(self):
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
    
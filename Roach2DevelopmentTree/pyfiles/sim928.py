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
    
        sim.write('*IDN?\n')

        return(sim.readline())

        
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
    
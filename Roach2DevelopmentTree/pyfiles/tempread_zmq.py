


import sys
import zmq
import time


class tempread_zmq:

    def __init__(self,str_ip='164.54.101.7',str_port='5555',isconn=False):
        self.ip = str_ip
        self.port = str_port
        self.isconn = isconn
        self.temperature = 0.0
        self.isrunning=False

        if isconn:
            self.connect()

    def disconnect(self):
        self.socket.close()
        self.context.destroy()

    def connect(self):
         self.context = zmq.Context()
         self.socket = self.context.socket(zmq.SUB)
         self.socket.connect ("tcp://%s:%s" %(self.ip,self.port))
         self.socket.setsockopt(zmq.SUBSCRIBE, "")

    def getTemp(self):
        if not isconn:
            self.connect()

        self.temperature = socket.recv()            

        if not isconn:
            self.disconnect()
        
        return(self.temperature)


    def daemon(self):
        while self.isrunning:
            self.getTemp()

    def startDaemon(self):
        self.isrunning = True
        
        




 

 

while(1):

    message = socket.recv()

    print "ADR 50mK temp: %s K" % message

    time.sleep(1)

 

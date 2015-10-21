"""



execfile('calibration.py')

cal = calibration()

cal.timex()

cal.timex2()

cal.phasetest()

cal.phasetest2()

"""

class calibration:

    def __init__(self):
        pass
        


    ##################################################################3
    #
    # bb loopback time delay cal, move by 10ps
    #
    ##################################################################


    def timex(self):
        times = arange(-0.5,0.5 , 0.010)
        self.minpower = 1e9
        self.mintime = 0.0
        sram.Q_phase_offs = 0
        
        for tt in times:
            sram.Q_time_delay=tt
            sram.setLutFreqs(sram.frequency_list, sram.amplist)
            FF = scoper()
            Fa=abs(FF)
            P = Fa*Fa
            power = sum(P[:256])
            if power<self.minpower: 
                self.minpower = power
                self.mintime = tt            
            draw()
            print tt
            #time.sleep(0.5)
        return(self.mintime)


    def timex2(self):
        times = arange(-0.5,0.5 , 0.010)
        self.minpower = 1e9
        self.mintime = 0.0
        sram.Q_phase_offs = 0
        
        for tt in times:
            sram.Q_time_delay=tt
            sram.setLutFreqs(sram.frequency_list, sram.amplist)
          
            print tt
            time.sleep(0.5)
        return(self.mintime)


    def phasetest(self):
        sram.Q_time_delay=0
        phofs = arange(-20.0,20.0,1)
        for pp in phofs:
            print '############## %f ##################'%pp
            sram.Q_phase_offs=(pi/180) *pp
            sram.setLutFreqs(sram.frequency_list, sram.amplist)
            time.sleep(0.5)
            
            
    def phasetest2(self):
        sram.Q_time_delay=0
        phofs = arange(-20.0,20.0,1)
        for pp in phofs:
            print '############## %f ##################'%pp
            sram.Q_phase_offs=(pi/180) *pp
            #sram.setLutFreqs(arange(10e6,200e6,10e6), 2000)
            sram.setLutFreqs(sram.frequency_list, sram.amplist)
            FF = scoper()
            draw()
            #time.sleep(2.0)
            
            
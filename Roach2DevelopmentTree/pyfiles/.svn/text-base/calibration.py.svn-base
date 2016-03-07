"""



execfile('calibration.py')

cal = calibration()

cal.timex()

cal.timex2()

cal.phasetest()

cal.phasetest2()




################################################################
#pos sideband
sram.Q_phase_offs=0.02 * -18.5
sram.Q_amp_factor = -1.0
sram.setLutFreqs(arange(10e6,200e6,10e6), 3000)



####################################################################
#neg sideband

#LO at 3.5G
#sram.Q_phase_offs=0.02 * 18.5
#LO at 4.5G
#sram.Q_phase_offs=0.02 * 10


sram.Q_phase_offs=(pi/180) *0
sram.Q_amp_factor = -1.0
sram.Q_time_delay = 0
sram.setLutFreqs(arange(10e6,200e6,10e6), 2000)

sram.Q_phase_offs=(pi/180) *18
sram.setLutFreqs(arange(10e6,200e6,10e6), 2000)


a=scoper()


#####################################
# cal the 1st tone
#


sram.setLutFreqs([200e6], 20000)


freq =  sram.frequency_list[0]
pbin = 512.0*freq / sram.dac_clk
nbin = 512 - pbin

nph = angle(FF[nbin])
namp = abs(FF[nbin])

pph = angle(FF[pbin])
pamp = abs(FF[pbin])


#make a sine and cos to add to the wavetable to cancle pbin.
cal_amp = sram.amplist[0] * pamp / namp
cal_ph = pi + (pph - nph) - sram.lut_phase_list[0]


sram.lut_i=sram.lut_i + sram.singleFreqLUT(freq, 'I', sram.dac_clk,sram.lut_length , cal_ph, cal_amp)
sram.lut_q=sram.lut_q + sram.singleFreqLUT(freq, 'Q', sram.dac_clk,sram.lut_length , cal_ph, cal_amp)
sram.lut_binaryIQ=sram.convertToBinary128(sram.lut_i,sram.lut_q)
sram.writeSram(sram.lut_binaryIQ)
sram.streamSram()
        


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
            
            
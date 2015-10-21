"""

execfile('mkiddac.py')
dac = MKIDDac(roach2, 'MKID_DAC')

dac.setReset();dac.setSync(0,0);dac.setSync(1,1)

phase = 55
dac.setSync(0,0);dac.setDllPhase(phase);dac.setSync(1,1);phase = phase+5

dac.setDllInvClk(1)

"""

class MKIDDac:

    def __init__(self,roach_,fw_block_name_):
    
        self.fw_block_name=fw_block_name_
	self.roach = roach_

	#_settings_reg bits	
	self.synci_bit = 0
	self.syncq_bit = 1
	self.sdenb_bit = 2
	self.reset_bit = 3
	
	
	#
	# settings reg bits
	#
	self.synci=0
	self.syncq=0
	self.sdenb=0
	self.reset = 0
	
	
	self.setregval = 0
	
	#
	# config reg 10 bits
	#
	
	#dictionary of degrees, reg vals for DLL_delay on DAC5681 data sheet
	self.dll_delay_vals = { 50:8 , 55:9, 60:10, 65:11, 70:12, 75:13, 80:14, 
			85:15, 90:0, 95:1, 100:2, 105:3, 110:4, 115:5, 120:6, 125:7  }
	
	self.dll_degrees = 90
	self.dll_val = 0
	
	self.dll_invclk = 0
	
	self.configregval=0


    def setDllInvClk(self,is_inv):
        self.dll_invclk=is_inv
        self.configregval = self.configregval&0xF7
	self.configregval = self.configregval | (self.dll_invclk << 3)
	self.setConfigReg()
	
    def setDllPhase(self,degrees):
    
    
	#round to nearest 5 degrees	
	degrees = float(degrees)
	degrees = 5.0 * round(degrees/5.0)
	
	degrees = int(degrees)
    
    
        if (degrees<50): degrees=50
	
	if (degrees>125): degrees = 125
	
	self.dll_degrees=degrees
	self.dll_val=self.dll_delay_vals[self.dll_degrees]
	
	
	self.configregval = self.configregval&0xF
	
	self.configregval = self.configregval | (self.dll_val << 4)
	
	print "DAC Phase: %d"%(self.dll_degrees)
	self.setConfigReg()
	
    def setConfigReg(self):
    
        self.roach.write_int('%s_config'%(self.fw_block_name),self.configregval)	
	self.sdenb=0
	self.progSettings()
	self.sdenb=1
	self.progSettings()
	
	
	
    def setSync(self,si,sq):
    	
        
	self.synci=si
	self.syncq=sq
	self.progSettings()
	

    def setReset(self):
    
    	self.reset = 1
	self.progSettings()
	self.reset = 0
	self.progSettings()
	
	
    def progSettings(self):
    
    	self.setregval=(self.synci<<self.synci_bit) | \
		(self.syncq<<self.syncq_bit) | \
		(self.sdenb<<self.sdenb_bit) | \
		(self.reset<<self.reset_bit);	
	

	self.roach.write_int('%s_settings_reg'%(self.fw_block_name),self.setregval)
	
	
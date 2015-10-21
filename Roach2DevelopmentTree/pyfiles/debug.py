at.atten_U6=0;at.atten_U7=15;progAtten(roach,at);progRFSwitches(roach,rf)

at.atten_U6=0;at.atten_U7=15;progAtten(roach,at);progRFSwitches(roach,rf)



self.at.atten_U6=30;self.at.atten_U7=30;progAtten(roach,self.at);progRFSwitches(roach,self.rf)


self.na.startOutputDac=0;self.na.progRoach()

self.na.setFreq(100e6)

FirstRes_LO3.26G_St22.33E6_G15_00001.hdf





hdffile = h5py.File('crap.hdf','w')
hdf_grp_iqdata=hdffile.create_group("IQData")
hdf_grp_settings=hdffile.create_group("Settings")
		
hdf_dset_iq = hdf_grp_iqdata.create_dataset("IQ", (4096,2,2048), dtype='f8', maxshape=(None, None,None))
hdf_dset_iq_timestamps = hdf_grp_iqdata.create_dataset("Times", (4096,), dtype='S26', maxshape=(None))


hdf_dset_set_timestamps = hdf_grp_settings.create_dataset("Times", (4096,), dtype='S26', maxshape=(None))
hdf_dset_settings = hdf_grp_settings.create_dataset("Sets", (4096,), dtype='S4096', maxshape=(None))



hdf_dset_iq[0,0]=iq[0]
hdf_dset_iq[0,1]=iq[1]



hdffile.flush()
hdffile.close()




FirstRes_LO3.26G_St22.33E6_G15_00001.hdf


hdffile = h5py.File('FirstRes_LO3.26G_St22.33E6_G15_00001.hdf','r')
hdffile.keys()
hdffile.values()

hdffile['IQData'].keys()

hdffile['IQData']['IQ']
hdffile['IQData']['IQ'][0]

hdffile.close()




	def hdfOpen(self,name,number):
		
		self.hdfClose()
		hdffile = h5py.File('%s_%05d.hdf'%(name,number),'w')

		hdf_grp_iqdata=hdffile.create_group("IQData")
		hdf_grp_settings=hdffile.create_group("Settings")

		hdf_dset_iq = hdf_grp_iqdata.create_dataset("IQ", (4096,4096,2), dtype='f8', maxshape=(None, None,None))
		hdf_dset_iq_timestamps = hdf_grp_iqdata.create_dataset("Times", (4096,), dtype='S26', maxshape=(None))


		hdf_dset_set_timestamps = hdf_grp_settings.create_dataset("Times", (4096,), dtype='S26', maxshape=(None))
		hdf_dset_settings = hdf_grp_settings.create_dataset("Sets", (4096,), dtype='S4096', maxshape=(None))
		
		self.iq_index=0
		self.set_index=0	
			
	



na.hdfOpen("powerSweep_10_30_res1",1)
powerSweep(21.5e6,23e6,10,30,1)
na.hdfClose()





    self.attStart=attSt
	    self.attEnd=attEd
	    self.numSweeps=sweeps
	    self.attIncr=0.5
	
	    self.thread=NetThread(0);
	  

self.iqdata=iq









		
self.hdf_dset_attU6 = 
self.hdf_dset_attU6 = 
self.hdf_dset_attU28 =


self.hdf_dset_bbloop =
self.hdf_dset_rfloop =
self.hdf_dset_clkinternal =
self.hdf_dset_lointernal 
self.hdf_dset_losource 



self.hdf_dset_attU6 
self.hdf_dset_attU6 
self.hdf_dset_attU28


self.hdf_dset_SweepStFreq 
self.hdf_dset_SweepEdFreq 

self.hdf_dset_SweepIncFreq
self.hdf_dset_DFTLen 
self.hdf_dset_Delay =
self.hdf_dset_sdmod =


self.hdf_dset_LO =

self.hdf_dset_CLK 










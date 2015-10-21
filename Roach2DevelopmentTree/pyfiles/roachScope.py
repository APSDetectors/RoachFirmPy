
class roachScope:

    def __init__(self,rch_,fwn_):
        self.fwname = fwn_

        self.roach = rch_
        self.plotdata=0
        self.spect_mag=0
        self.is_hold=True

        self.is_octo=False

        self.xmin=0;self.xmax=10
        self.ymin=-5;self.ymax=5
        
        self.colorcycle = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        self.ncolors = len(self.colorcycle)
        self.current_color = 0
        
        self.text_x = 8.0
        self.text_y = 4.5
        
        self.clrscope()

    #trigin from 0,1,2,3 to trig on those inputs.
    #trig in -1 to ignore trig.
    #inpt is 0,1,2,3,4,5,6,7
    def trigScope(self,trigin=-1, inpt=0):
        
        if trigin ==-1:
         ig_tr = 1
         trigin = 0
        else:
         ig_tr = 0
    
       
        we_in = 0
        inputsel = inpt + trigin*16  + we_in*64;
        self.roach.write_int(self.fwname + "_inputsel",inputsel);

        print "Trigger roachscope"
        #clear trace
        self.roach.write(self.fwname + '_snapshot_bram','\0'*4096)
      
        ig_we = 1
      
        ctrl = ig_we*4 + ig_tr*2;

        self.roach.write_int(self.fwname + '_snapshot_ctrl',ctrl)


        stat = self.roach.read_int(self.fwname + '_snapshot_status')
        print 'stat = %x'%stat

        ctrl+=1;
        self.roach.write_int(self.fwname + '_snapshot_ctrl',ctrl)
        time.sleep(0.01)

        stat = self.roach.read_int(self.fwname + '_snapshot_status')
        print 'stat = %x'%stat
        print "END Trigger Roachscope"



    def readScope(self):
        binstr = self.roach.read(self.fwname + '_snapshot_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.plotdata = ccopy.deepcopy(shorts)

        self.is_octo=False


    def readScopeOcto(self):
        
        
        binstr = self.roach.read(self.fwname + '_snapshot_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        
        self.multiplotdata = [shorts]

        binstr = self.roach.read(self.fwname + '_snapshot1_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))

        self.multiplotdata.append(shorts)
        
        binstr = self.roach.read(self.fwname + '_snapshot2_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.multiplotdata.append(shorts)


        binstr = self.roach.read(self.fwname + '_snapshot3_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.multiplotdata.append(shorts)

        binstr = self.roach.read(self.fwname + '_snapshot4_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.multiplotdata.append(shorts)

        binstr = self.roach.read(self.fwname + '_snapshot5_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.multiplotdata.append(shorts)

        binstr = self.roach.read(self.fwname + '_snapshot6_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.multiplotdata.append(shorts)

        binstr = self.roach.read(self.fwname + '_snapshot7_bram',4096)
        shorts = list(struct.unpack('>2048h',binstr))
        self.multiplotdata.append(shorts)

        self.plotdata = ccopy.deepcopy(self.multiplotdata[0])
        
        self.is_octo=True;


    def interleave(self,chans):
    
        self.plotdata = [0] * (len(chans) * len(self.multiplotdata[0]))
        
        nc = len(chans) 
        
        for k in range(nc):
            self.plotdata[k::nc] =  self.multiplotdata[chans[k]]
            

    def plotSpectrum(self,pllen = 2048,signbit = -1,replot=False,log='No'):

        if replot==False:
            self.readScope()
            shorts = ccopy.deepcopy(self.plotdata)           
        else:
            shorts = ccopy.deepcopy(self.plotdata)           
                
        if signbit!=-1:
            for kk in range(len(shorts)):
                sgn = shorts[kk] & (1<<signbit)
                if sgn!=0:
                    shorts[kk] = shorts[kk] - (1 << (signbit+1))

        
        self.shorts = ccopy.deepcopy(shorts    )

        figure(1)

        if self.is_hold==False: clf()

        w=numpy.hamming(pllen)
        self.spect_mag =numpy.abs(numpy.fft.fft(w*shorts[:pllen]))
        if log=='No':
            plot(self.spect_mag)
        else:
            semilogy(self.spect_mag)



    def clrscope(self):
    
        figure(1)
        clf()
       
        
        axis([self.xmin, self.xmax, self.ymin, self.ymax])
        grid(b=True,which=u'major')
        autoscale(False)
      
       
        #self.colorcycle = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        #self.ncolors = len(colorcycle)
        self.current_color = 0
        self.text_x = 8.0
        self.text_y = 4.5
        
    def splot(self,
        data,
        is_fit=False,
        volts_per_div=1.0,
        volt_offset = 0.0, 
        samples_per_div=1.0, 
        sample_delay=0):
    
        if self.is_hold==False: self.clrscope()
        
        
        if is_fit:
            samples_per_div =  float(len(data))/10.0
            sample_delay=0.0
            vrange = float(numpy.max(data) - numpy.min(data))
            volts_per_div = vrange / 10.0
            volt_offset = (vrange / 2.0) -  numpy.min(data) 
            
        
        
        x=(numpy.arange(len(data))-sample_delay) / float(samples_per_div)
        
        y = (data - volt_offset) / volts_per_div
        
        plot(x,y,self.colorcycle[self.current_color],drawstyle = 'steps')
        text(self.text_x, self.text_y, 
            '%5.2f V/div,%5.2f S/div'%(volts_per_div,samples_per_div),
            color=self.colorcycle[self.current_color])
        
        if volts_per_div==0.0: 
            volts_per_div=1.0
            
        plot(0,-volt_offset/volts_per_div,'%sD'%(self.colorcycle[self.current_color]))
        
        self.text_y=self.text_y - 0.5
        
        self.current_color = (self.current_color + 1) % self.ncolors
        
        
        
        
        
    def plotScope(self,pllen = 2048,
        is_usebits = False, 
        bits = '15:11;10:10;9:9;8:8',
        isprint = False,
        isprintsh=False,
        shskip = 1,
        shoffset=0,
        signbit=-1,        
        replot=True,
        isfit_=True):


        if replot==False:
            self.readScope()
            shorts = ccopy.deepcopy(self.plotdata)
        else:
            shorts = ccopy.deepcopy(self.plotdata)           
        
        
        shorts = shorts[shoffset::shskip]        
        if signbit!=-1:
            for kk in range(len(shorts)):
                sgn = shorts[kk] & (1<<signbit)
                if sgn!=0:
                    shorts[kk] = shorts[kk] - (1 << (signbit+1))

        self.shorts = ccopy.deepcopy(shorts    )
        
        #figure(1)



        #if self.is_hold==False: clf()

        if isprint:
            print binstr
            print len(binstr)
    
        if isprintsh:
            print shorts
            print len(shorts)


        if is_usebits==False:
            self.splot(numpy.array(shorts[:pllen]),is_fit = isfit_)

        else:
            bitwidths=bits.split(';')
            stbit = 15
            smax = 0
            graphnum = 0.0
            ngraphs = len(bitwidths)
            
            
            hsave = self.is_hold
            self.is_hold = True
            
            
            for k in range(ngraphs):
                couple = bitwidths[k].split(':')
                stbit=int(couple[0])
                edbit=int(couple[1])
                print '%d %d'%(stbit,edbit)
                width = 1 + stbit - edbit
                y=numpy.array([0.0]*pllen)
                if width>0:
                    mask = (1<<width) - 1

                
                for i in range(pllen):
                    sval = shorts[i]


                    datash = sval>>edbit
                    datash = datash & mask
                    datash = double(datash)

                    factor = double((1<<width));

                    if len(bitwidths)<2:
                        factor = 1.0

                    y[i] = (2.0*graphnum) + (datash/factor)
                    vpd = 2.0*ngraphs / 10.0
                    voffs = ngraphs
                    spd = pllen/10.0
                    sof = 0.0

                self.splot(numpy.array(y),
                    is_fit = False, 
                    volts_per_div=vpd,
                    volt_offset=voffs,
                    samples_per_div=spd,
                    sample_delay=sof)
                    
                    
                graphnum = graphnum+1.0
                stbit = stbit - width
            
            
            self.is_hold = hsave
            
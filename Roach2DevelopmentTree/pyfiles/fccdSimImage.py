
"""

execfile('fccdSimImage.py')

fccdi = fccdSimImage(None,960,962)

fname = '/localc/fccd/raw_scrambled_rawImm_12001-13000.imm'

aa=fccdi.loadImgImmRaw(fname,100)



"""


class fccdSimImage:

    def __init__(self,sram_,x_,y_):
        self.sram = sram_
        self.sx=x_
        self.sy=y_
        
        #1 dlong is 8 byte
        #wait between packets
        self.waitdlongs=32
        
        self.bdvld = 0
        self.beof=1
        self.bmux=2
        self.bfrinc=3
        self.bpinc=4
        self.bpacketrst = 5
        
        self.packetlen_dlong = 170
        self.packetlen_byte = self.packetlen_dlong*8
        self.packetlen_short = self.packetlen_dlong*4
        
        self.packetimglen_dlong=self.packetlen_dlong-1
        
        self.packetimglen_short=self.packetimglen_dlong*4
        
        
        
        self.imglen_short = self.sx*self.sy
        
        self.numpackets =  self.imglen_short/self.packetimglen_short
        
        self.leftovershort =self.imglen_short- (self.numpackets * self.packetimglen_short)
        self.leftoverdlong =self.leftovershort/4
        
        self.chan2out = {0:5 , 1:4, 2:7,3:6, 4:1, 5:0,6:3, 7:2 }
     
        
    def loadImgImmRaw(self,fname,imgnum):
    
        hsize=1024
        dsize=self.sx * self.sy * 2
        npix=dsize/2
        
        dstart = imgnum*(hsize + dsize) + hsize
        
        fp=open(fname,'rb')
        fp.seek(dstart)
        imgbin=fp.read(dsize)
        self.imgsh=list(struct.unpack('H'* npix,imgbin))
        fp.close()
        
        return(self.imgsh)
        
        
    def makePackets(self):
    
       
       
        ptrst = 0
        
        self.bdata = ''
        
        
        #
        # image packets, stat w/ header dlong, then 1023 image dlongs
        #
        
        for p in range(self.numpackets):
            self.onePacket(ptrst)
            ptrst=ptrst + self.packetimglen_short
            self.waitPacket()
           
             
        #
        # last bit of image in shorter packet
        #
        self.onePacket(ptrst,self.leftoverdlong)
        self.waitPacket()
        self.incFrame()
        self.waitPacket()
        
        
         
    def onePacket(self,offsetshort,plenshort =0):       

        if plenshort==0:
            plenshort=self.packetimglen_short
        
        plendlong = plenshort/4
        plenshort = plendlong*4
        
        ptrst = offsetshort
        ptren = offsetshort+plenshort
     #1023 * 4 shorts
        imgchunk = self.imgsh[ptrst:ptren]
        
        #1 dlong for header, + 1023 dlongs, inerleaved.
        data0=[0] + imgchunk[0::4]
        data1=[0] + imgchunk[1::4]
        data2=[0] + imgchunk[2::4]
        data3=[0] + imgchunk[3::4]
        data4=[]

        data4.append(   ( (1<< self.bdvld)  +  (0<< self.bmux) )  )

        data4.append(   ( (1<< self.bdvld)  +  (1<< self.bmux)  + (1<<self.bpinc))  )
        data4 = data4 + [ ( (1<< self.bdvld)  +  (1<< self.bmux) ) ] * (plendlong-1)

        zeros=  [0] *   ( plendlong+1)

        data4[-1] = data4[-1] + (1 << self.beof)

        datalist =[[],[],[],[],[],[],[],[]]
        

        datalist[self.chan2out[0]]=data0;
        datalist[self.chan2out[1]]=data1;
        datalist[self.chan2out[2]]=data2;
        datalist[self.chan2out[3]]=data3;
        datalist[self.chan2out[4]]=data4;
        datalist[self.chan2out[5]]=zeros;
        datalist[self.chan2out[6]]=zeros;
        datalist[self.chan2out[7]]=zeros;
       
        
        bb = self.sram.convertToBinary128_4(
            datalist[0], datalist[1],datalist[2],datalist[3],
            datalist[4],datalist[5],datalist[6],datalist[7])
            

        self.bdata= self.bdata + bb
        print len(self.bdata)
        
        

    def testRamp(self,chan):
        llen=65536
        zeros = [0] * llen 
        data=range(-llen/2,llen/2)
        
        datalist = [zeros] *8
        datalist[chan]=data
        
        self.bdata = self.sram.convertToBinary128_4(
            datalist[0],datalist[1],datalist[2],datalist[3],
            datalist[4],datalist[5],datalist[6],datalist[7])
            
        self.writeSram()
        self.streamSram()
        
        
              
    def incFrame(self):  
      
        zeros=  [0]
        data4=  [ (  (1<<self.bfrinc) + (1<<self.bpacketrst)  ) ]
            
           
        datalist =[zeros] *8
        

        datalist[self.chan2out[4]]=data4;
       
        
        bb = self.sram.convertToBinary128_4(
            datalist[0], datalist[1],datalist[2],datalist[3],
            datalist[4],datalist[5],datalist[6],datalist[7]) 
        
     
       

        self.bdata= self.bdata + bb

    
           
    def waitPacket(self):       
        zeros=  [0] *    self.waitdlongs

        bb = self.sram.convertToBinary128_3(
            zeros,zeros,zeros,zeros,
            zeros,zeros,zeros,zeros)

        self.bdata= self.bdata + bb

    def writeSram(self):
    
        self.sram.writeSram(self.bdata)
        
    def streamSram(self):
        self.sram.streamSram()
        
        
    def estat(self):
        sreg = sram.roach.read_int('status_reg')
        
        led_up=sreg&1
        led_rx = sreg&2
        led_tx = sreg&4
        tx_afull = sreg&8
        tx_ov = sreg&16
        tx_vld=sreg&32
        rx_eof = sreg&64
        rst=sreg&128
        
        print 'led_up %d led_rx %d led_tx %d tx_afull %d tx_ov %d tx_vld %d rx_eof %d rst %d \n'%\
            ( led_up,led_rx ,led_tx ,tx_afull ,tx_ov , tx_vld,rx_eof ,rst )
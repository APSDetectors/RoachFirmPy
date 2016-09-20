
"""

execfile('sigdel.py')

sd = sigdel()

sd.quantize(2,.2)

for k in numpy.arange(0.0,1.1,0.1):
    print sd.quantize(5,k)
    
    
sdout = sd.sdmFirstOrd(6,u)

a_ = [-rand(), -rand()]

sdout = sd.sdmSecOrd(2,u,a=a_)


2nd ord, u=0.3, good numbers
([-0.8611386829779479, -0.9719416461567895], 0.002635591041196894)

u = 0.5 + 0.5* numpy.cos(20.0* 2*pi* arange(1000.0)/1000.0  )

u = numpy.arange(0.0,1.0,0.001)


clf()

plot(sdout)


clf()

a_ = [-rand(), -rand()]
sdout = sd.sdmSecOrd(2,u,a=a_)
clf()
semilogy( 1e-6+abs(fft.fft(sdout)))


def doit(): 
    amp = 0.3  
    u = 0.5 + amp* numpy.cos(round(50*rand())* 2*pi* arange(1000.0)/1000.0  )
    #a_ = [-rand(), -rand()]
    (a_,er_)= ([-0.8611386829779479, -0.9719416461567895], 0.005635591041196894)
    #er_=0.01 * rand()
    sdout = sd.sdmSecOrd(2,u,a=a_,er=er_)
    clf()
    semilogy( 1e-6+abs(fft.fft(sdout)))
    return( (a_,er_))



def doit():   
    amp = 0.1  
    u = 0.5 + amp* numpy.cos(10.0* 2*pi* arange(1000.0)/1000.0  )
    a_ = [-rand(), -rand(), -rand()]
    g_ = [0.5*rand(), 0.2*rand(), 0.1*rand()]  
    er_=0.01 * rand()
    sdout = sd.sdmThrdOrd(2,u,a=a_,g = g_,er=er_)
    clf()
    semilogy( 1e-6+abs(fft.fft(sdout)))
    return( (a_,g_,er_))


amp = 0.1 3rd
([-0.8868241663381813, -0.6374236655380534, -0.5759672488755259],
 [0.37927169935915983, 0.14564016579669106, 0.010526620024450884],
 0.008347220547984393)


sd.snr()

dd=sd.snr(
order=2,
isrand=False,
amp=.2,
a_=[-1.0, -1.0],
g_=[0.4,0.0],
er_=0.05,
lplot=0.005)


doit()



6 levels, 3rd order sdm below works, u=0.1
([-0.8760862692067424, -0.5707470226746265, -0.8304969112906833],
 0.005057214496137713)

a_=[-0.8760862692067424, -0.5707470226746265, -0.8304969112906833]
sdout = sd.sdmThrdOrd(4,u,a=a_,er=0.005)
clf()
semilogy( 1e-6+abs(fft.fft(sdout)))


def doit():


"""
import numpy

class sigdel:

    def __init__(self):
        self.integrator=[0.0]*32
        
    ##
    # x is signal in, 0 to 1.0
    def quantize(self,nlev,x):
    
        M = numpy.double(nlev - 1)
        v= round(x*M)/M
        if v>1.0: v=1.0
        if v<0.0: v=0.0
        return(v) 
        
        
        
        
        
    def integrate(self,N,x):
        self.integrator[N] = self.integrator[N]  + x
        return(self.integrator[N])
        
    def sdmFirstOrd(self,nlev,data,a=[-1.0]):
    
        self.integrator[0] = 0.0
        
        L = len(data)
        dataout = numpy.zeros(L)
        vz = 0.0
        
        for k in range(L):
            u = data[k]
            
            y =  self.integrate(0, u + a[0]*vz)
            v = self.quantize(nlev,y)
            
            dataout[k] = v
            vz = v
        return(dataout)
                      
                      
                      
      
    def sdmSecOrd(self,nlev,data,a=[-1.0,-1.0],g = [0.0, 1.0], er=0.0):
    
        self.integrator[0] = 0.0
        self.integrator[1] = 0.0
        
        L = len(data)
        dataout = numpy.zeros(L)
        vz = 0.0
        
        for k in range(L):
            u = data[k]
            
            y0 =  self.integrate(0, u + a[0]*vz)
            
            y1 = self.integrate(1, y0+ a[1]*vz)
            err = er*rand()
            v = self.quantize(nlev,g[0]*y0 + g[1]*y1+err)
            
            dataout[k] = v
            vz = v
        return(dataout)
                       
              
      
    def sdmThrdOrd(self,nlev,data,a=[-1.0,-1.0,-1.0],g = [0.0, 0.0,1.0], er=0.0):
    
        self.integrator[0] = 0.0
        self.integrator[1] = 0.0
        self.integrator[2] = 0.0
        
        L = len(data)
        dataout = numpy.zeros(L)
        vz = 0.0
        y0z = 0
        y1z = 0
        y2z = 0
        
        for k in range(L):
            u = data[k]
            
            y0 =  self.integrate(0, u + a[0]*vz)
            
            y1 = self.integrate(1, y0+ a[1]*vz)
            y2 = self.integrate(2, y1+ a[2]*vz)

            err = er*rand()
            v = self.quantize(nlev,g[0]*y0z + g[1]*y1z +   g[2]*y2z+err)
            
            dataout[k] = v
            vz = v
            y0z = y0
            y1z=y1
            y2z=y2
            
        return(dataout)




    def snr(self,
        amp= 0.1,
        lplot=0.01,
        L=100000.0,
        sig="sine",
        order = 3,
        nlev = 2,
        isrand=False,
        a_ = [-0.8868241663381813, -0.6374236655380534, -0.5759672488755259],
        g_ = [0.37927169935915983, 0.14564016579669106, 0.010526620024450884],
        er_=0.000):  
          
        f =  round(lplot*L*rand())  
        if sig=="sine":
            u = 0.5 + amp* numpy.cos(f* 2*pi* arange(L)/L  )
  
        if isrand:
            if order==3:
                a_ = numpy.array([rand(), rand(), rand()])*numpy.array(a_)
                g_ = numpy.array([rand(), rand(), rand()])*numpy.array(g_)
                er_= rand()*er_
            if order==2:
                a_ = numpy.array([rand(), rand()])*numpy.array(a_)
                g_ = numpy.array([rand(), rand()])*numpy.array(g_)
                er_= rand()*er_
            
            
        if order==3:
            sdout = self.sdmThrdOrd(nlev,u,a=a_,g = g_,er=er_)
    
        if order==2:
            sdout = self.sdmSecOrd(nlev,u,a=a_,er=er_)
           
        figure(2)
        clf()
        plot(sdout[:(lplot*L)])   
        figure(1)    
        clf()
        F = abs(fft.fft(sdout))/L
        FF = F*F
        plot(10*log10( 1e-12+FF)[1:lplot*L])    
        #plot(1e-10+FF[1:lplot*L])    
        #plot(FF[1:lplot*L])
        Sig = FF[f]        
        Noise =  sum(FF[1:lplot*L])  -  Sig  
        print '%f %f %f'%(Sig,Noise,10*log10(Sig/Noise))  
        #print FF[0:lplot*L] 
        #print FF[f]
        print     
        return( (a_,g_,er_,FF))


                             
import numpy as np
from scipy import linalg
import random as rnd
import matplotlib
import matplotlib.pyplot

'''

execfile('pca.py')


p = pulseTrain(1000)
e = eigens(p)

plot(e['eigenvectors'][0])

plot(e['eigenvectors'][1])

testan(e,2);


'''

print 'running pca.py'

def makePulse(L=100.0,t1=10.0,t2=1.0,a1=1.0,a2=1.0,n=0.1):
    rnd.seed(None)
    e1=a1*np.exp(-1*np.arange(L)/t1);
    e2=a2*(1.0 - np.exp(-1*np.arange(L)/t2));
    p1=e1*e2
    noise=[]
    for k in range(int(L)): noise.append(rnd.gauss(0.0,n))
    noise=np.array(noise)
    p1=p1+noise
    return(p1)
 
    
def pulseTrain(N=100):
    
    plist=[]
    for n in range(N):
        amp = 0.5 + 0.02*rnd.random()
        amp2 = 0.2 + 0.02*rnd.random()
        xx=rnd.random()
        if xx>=0.5: tc = 10
        else: tc = 4
        
        pls=makePulse(
            a1=amp,
            a2=amp2,
            t2=4,
            t1=tc,
            n=0.001)
        plist.append(pls.tolist())
        
    D=np.array(plist).transpose()
    
    plotTrain(D)
    return(D)
    
def plotTrain(D):
    
    matplotlib.pyplot.figure(1)
    N=D.shape[0]
    L=D.shape[1]
    matplotlib.pyplot.clf()
    for k in range(N):
        matplotlib.pyplot.plot(D.transpose()[k])
    
    matplotlib.pyplot.figure(2)
    matplotlib.pyplot.clf()
    matplotlib.pyplot.pcolor(D)
    
 

def eigens(D): 
    Z=np.dot(D,D.transpose() )
    #Z =np.cov(D)
    evals,evecs=linalg.eig(Z)
    evals = np.real(evals)
    evecs = np.real(evecs)
    
    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.clf()
    matplotlib.pyplot.plot(np.real(evals))
    matplotlib.pyplot.figure(2)
    matplotlib.pyplot.clf()
    matplotlib.pyplot.pcolor(evecs * evals)
    matplotlib.pyplot.figure(3)
    matplotlib.pyplot.clf()
    matplotlib.pyplot.pcolor(Z)
    
    matplotlib.pyplot.figure(4)
    matplotlib.pyplot.plot(evecs * evals)
    

    retdata = {}
    retdata['eigenvalues'] = np.real(evals)
    retdata['eigenvectors'] = np.real(evecs).transpose()
    retdata['covariance'] = Z
    
    return(retdata)
    
      
def eigenPulseTrain(eigendata,numcomponents=2,N=100):

    pulsestruct =np.array( [ [0.1,1.0],[1.0,0.1] , [0.5,0.5] , [0.1,-1.0]])
    pulses = []
    for n in range(N):
        pulse = np.array([0.0] *  len(eigendata['eigenvectors'][0]) )
        r = rand()
        psindex = floor(rand() * len(pulsestruct))
       
        ps = pulsestruct[psindex]
      
        
        ps = ps* (1.0 + 0.2*rand(numcomponents))
        
        for c in range(numcomponents):
            
            eigpulse = eigendata['eigenvectors'][c]
            pulse = pulse + eigpulse * ps[c]          
           
        pulses.append(pulse)
    pulses = np.array(pulses)
    figure(1)
    clf()
    plot(pulses.transpose())
   
    return(pulses)
           

    
def testan(eigendata,numcomponents):
    
    
    #p = pulseTrain().transpose()
    p = eigenPulseTrain(eigendata)
   
    
    figure(10)
    
    
    Rvals = []
    for pulse in p:
        rvalp = [0.0] * (1+numcomponents)
        energy = 0.0
        for c in range(numcomponents):
            
            filt = eigendata['eigenvectors'][c]
            fp = np.convolve(pulse,filt)
            rvalp[c] =(np.dot(fp,fp))
            #rvalp[c] =max(fp)
            energy = energy + rvalp[c]
         
        rvalp[numcomponents]  =  energy
        Rvals.append(rvalp)
        if numcomponents==2:
            plot(rvalp[0],rvalp[1],'.')
        
    return(np.array(Rvals)             )
    
   
    
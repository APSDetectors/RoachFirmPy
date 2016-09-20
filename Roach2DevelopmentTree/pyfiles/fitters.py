import os

import scipy        
import scipy.linalg
import mpfit

import struct
from numpy import *
import time,fractions, math,inspect,random
import threading

import numpy

import h5py


print "Loading fitters.py"



########################################################################
#
#
#
#
#######################################################################

                
        


class fitters:

    def __init__(self):

            #hdf file to write
            self.hdffile=None
            #hdffile to read
            self.hdffile_r=None

            self.reslist=[]

            self.device_name='NULL'


            self.resonator=resonatorData(0,self.device_name)

            #plot when doing fitting for status...0 mean no plots
            self.fit_plots=1
            self.fit_prints=1


    def fitprint(self,stx):
             if self.fit_prints==1:
                print stx


    def setResonator(self,res):
            self.resonator=res

    def setResIndex(self,ii):
            self.resonator=self.reslist[ii]

    def addRes(self,res):
            self.reslist.append(res)


    def clearResList(self):
            self.reslist=[]


    def listResonators(self):
            for rr in self.reslist:
                    rr.info()



    def plotIQNoiseCircle(self,noise_tr_indx):

        resdata = self.resonator

        tsr=resdata.iqnoise[noise_tr_indx]

        tsr_tr=fit.trans_rot3(resdata, tsr)

        figure(15);clf()

        plot(resdata.trot_xf,resdata.trot_yf,'x')
        plot(resdata.iqdata[0],resdata.iqdata[1],'x')
        plot(tsr[0],tsr[1],'x')
        plot(tsr_tr[0],tsr_tr[1],'x')





    def addMkidList(self):
        for mkid in MKID_list:
            self.addResList(mkid.reslist)


    def plotResonators(self):

            #8 per plot, 4x4 plots
            #amp  amp amp amp
            #ph   ph  ph  ph
            #amp amp amp amp
            #ph ph ph ph

            fignum=13;
            figure(fignum)
            fignum=fignum+1;
            clf()

            #count rows
            plotrow=0

            prows=2
            for rr in self.reslist:
                try:
                    rr.info()

                    if (rr.lorentz_fr==0):

                        #fits not run

                        IQ=rr.iqdata

                        freqs=rr.freqs

                        IQp=rr.RectToPolar(IQ)


                        pcols=2
                        subplot(prows,pcols,plotrow*pcols+1); 


                        plot(freqs,IQp[0])
                        ylabel('Magnitude')

                        txt_y=(max(IQp[0]) + min(IQp[0]))/2.0;
                        txt_x=rr.rough_cent_freq;
                        text(txt_x,txt_y,"%4f"%(rr.rough_cent_freq/1e6))



                        subplot(prows,pcols,plotrow*pcols+2);
                        plot(freqs,rr.removeTwoPi(IQp[1]))
                        ylabel('Phase')

                    else:


                        mags=rr.phig_mag2s21
                        freqs=rr.freqs
                        params=rr.lorentz_params

                        mag2s21fit = lorentzFunc(freqs,params);


                        phase=rr.phig_phase

                        frindx=min(where(rr.lorentz_fr<=rr.freqs)[0])

                        pcols=3
                        subplot(prows,pcols,plotrow*pcols+1,polar=False); 

                        plot(freqs,mag2s21fit,'r')
                        plot(freqs,mags,'x')
                        #plot(self.resonator.lorentz_fr,lorentzFunc(self.resonator.lorentz_fr,params),'^')
                        plot(freqs[frindx],mags[frindx],'o')
                        ylabel('Magnitude')



                        txt_y=(max(mag2s21fit) + min(mag2s21fit))/2.0;
                        txt_x=rr.rough_cent_freq;
                        text(txt_x,txt_y,"%4f"%(rr.lorentz_fr/1e6))




                        subplot(prows,pcols,plotrow*pcols+2,polar=False); 

                        plot(freqs,phase,'x')
                        ylabel('Phase')

                        plot(freqs,phaseFunc(freqs,rr.phig_phase_guesses[0],rr.phig_phase_guesses[1],rr.phig_phase_guesses[2] ,rr.phig_phase_guesses[3]),'g')
                        plot(freqs,phaseFunc(freqs,rr.ph_Qf,rr.ph_fr,rr.ph_theta,rr.ph_sgn ),'r')


                        subplot(prows,pcols,plotrow*pcols+3,polar=False); 


                        #pp=self.RectToPolar([rr.trot_xf,rr.trot_yf ])


                            #polar(pp[1],pp[0],'x')

                            #polar(pp[1][frindx],pp[0][frindx],'o')
                        plot(rr.trot_xf,rr.trot_yf,'x' )
                        plot(rr.trot_xf[frindx],rr.trot_yf[frindx],'o')


                        for noise_trace in rr.iqnoise:
                            tsr=noise_trace

                            tsr_tr=fit.trans_rot3(rr, tsr)
                            ts_tr = self.RectToPolar(tsr_tr)
                            #polar(ts_tr[1],ts_tr[0],'rx')

                            plot(tsr_tr[0],tsr_tr[1],'.')






                    plotrow=plotrow+1
                    if (plotrow==prows):
                            plotrow=0;
                            figure(fignum)
                            clf()
                            fignum=fignum+1

                except:
                    print "problem w/ plotting resonator"



    def addResList(self,rl):
            for r in rl:
                    self.reslist.append(r)


    def extractResonators(self,res,nsd):
            self.setResonator(res)

            a=self.findResPhase(nsd);

            if a[0]!=None:
                    res.info()


                    indices=a[0]
                    flist=a[1]

                    dfreq=res.freqs[1]-res.freqs[0]

                    #span of res in Hz, 1/2 span actually
                    hlfspan=4e5

                    #num indices for 1/2 span
                    ihspan=ceil(hlfspan/dfreq)

                    reslist=[]

                    for ii in indices:
                        ist=int(max(ii-ihspan,0))
                        ied=int(min(1+ii+ihspan,res.datalen))

                        newres=resonatorData(ii,self.device_name);
                        newres.setData([res.iqdata[0][ist:ied],res.iqdata[1][ist:ied]],res.freqs[ist:ied],res.delayraw,res.carrierfreq)
                        reslist.append(newres)

                    return(reslist)




    #trim the freq span of data, and add to reslist
    def trimAddResonator(self,res,freqindex):
            self.setResonator(res)



            res.info()


            indices=[freqindex]
            flist=[res.freqs[freqindex]]

            dfreq=res.freqs[1]-res.freqs[0]

            #span of res in Hz, 1/2 span actually
            hlfspan=4e5

            #num indices for 1/2 span
            ihspan=ceil(hlfspan/dfreq)

            ii=indices[0]


            ist=int(max(ii-ihspan,0))
            ied=int(min(1+ii+ihspan,res.datalen))

            newres=resonatorData(ii,self.device_name);
            newres.setData([res.iqdata[0][ist:ied],res.iqdata[1][ist:ied]],res.freqs[ist:ied],res.delayraw,res.carrierfreq)
            self.addRes(newres)

            return(newres)

    #do median filter on I and Q to take out impulse noise
    def medianFilter(self):
        for res in self.reslist:
            self.setResonator(res)
            x = self.resonator.iqdata[0]
            y = self.resonator.iqdata[1]
            self.resonator.iqdata[0] = scipy.signal.medfilt(x,5)
            self.resonator.iqdata[1] = scipy.signal.medfilt(y,5)

    #do median filter on I and Q to take out impulse noise
    def medianFilter2(self,x,y):            
     
        xf = scipy.signal.medfilt(x,5)
        yf = scipy.signal.medfilt(y,5)
        return( (xf,yf) )

    #do median filter on I and Q to take out impulse noise
    def lowPassFilter2(self,x,y):

       
        xf = scipy.signal.lfilter([0.5,0.5],[1],x)
        yf = scipy.signal.lfilter([0.5,0.5],[1],y)
        xf[0] = xf[1]
        yf[0] = yf[1]
        return( (xf,yf) )

            


    #do median filter on I and Q to take out impulse noise
    def lowPassFilter(self):
        for res in self.reslist:
            self.setResonator(res)
            x = self.resonator.iqdata[0]
            y = self.resonator.iqdata[1]
            self.resonator.iqdata[0] = scipy.signal.lfilter([0.5,0.5],[1],x)
            self.resonator.iqdata[1] = scipy.signal.lfilter([0.5,0.5],[1],y)
            self.resonator.iqdata[0][0] = self.resonator.iqdata[0][1]
            self.resonator.iqdata[1][0] = self.resonator.iqdata[1][1]


    def IQvelocityCalc(self):
            for res in self.reslist:
                    self.setResonator(res)
                    x = self.resonator.iqdata[0]
                    y = self.resonator.iqdata[1]
                    
                    (x,y)=self.medianFilter2(x,y)
                    (x,y)=self.lowPassFilter2(x,y)
                    
                    maxIQvel = 0
                    maxIQIndex=0
                    self.resonator.maxIQVel_z=[]
                    for i in range(0,len(x)-2): ### correct range?
                            z = sqrt((x[i+1]-x[i])**2 + (y[i+1]-y[i])**2)
                            self.resonator.maxIQVel_z.append(z)
                            if z > maxIQvel:
                                    maxIQvel = z
                                    maxIQIndex=i
                    self.resonator.maxIQvel = maxIQvel
                    self.resonator.maxIQvel_freq=self.resonator.freqs[maxIQIndex]

                    self.resonator.maxIQVel_gz=numpy.gradient(numpy.array(self.resonator.maxIQVel_z)).tolist()

                    s=numpy.sort(self.resonator.maxIQVel_z)[::-1]
                    self.resonator.maxIQvel_ratio=s[0]/(s[1]+1e-12)


    def clearFitsFlag(self):

        for res in self.reslist:
            res.is_ran_fits=0


    def fitResonators(self):

            self.fitprint("HELLO")

            for res in self.reslist:

                #fit the res if not a noise trace
                
                if res.is_ran_fits==0:
                    self.setResonator(res)
                    res.is_fit_error=0

                    try:
                    #if 1==1:
                      if self.fit_plots:
                          figure(11)
                          clf()
                          subplot(2,1,1)
                          plot(self.resonator.iqdata[0],self.resonator.iqdata[1])
                          subplot(2,1,2)
                          plot(self.resonator.freqs,self.resonator.iqdata[0])
                          plot(self.resonator.freqs,self.resonator.iqdata[1])
                          legend("I","Q")


                      #tim madden- if the time delay is bad, phase has a lean to it.
                      #we correct the lean...    
                      #self.addLineToPhase()    

                      self.NinoInitialGuess()
                      self.fitprint("self.NinoInitialGuess() done")
                      self.NinoFitPhase()
                      self.fitprint("self.NinoFitPhase() done")
                      self.NinoLorentzGuess()
                      self.fitprint("self.NinoLorentzGuess()")
                      self.NinoFitLorentz()
                      self.fitprint("self.NinoFitLorentz() done")
                      self.lorentzEndCalcs()
                      self.fitprint("self.lorentzEndCalcs()done")
                      self.CecilSkewcircleGuess()
                      self.fitprint("self.CecilskewcircleGuess() done")
                      self.CecilfitSkewcircle()
                      self.fitprint("self.CecilfitSkewcircle() done")
                      self.SkewcircleEndCalcs()
                      self.fitprint("self.SkewcircleEndCalcs() done")
                      if self.fit_plots:
                          self.lorentzPlots()
                          self.SkewcirclePlots() 
                          
                      res.is_ran_fits=1
      
                    except:
                    #else:
                      self.fitprint("Problem fitting Resonator")
                      res.is_fit_error=1



    def saveResonators(self,fname):

            fp=self.resonator.openHDF(fname)


            ii=1                
            for res in self.reslist:
                res.writeHDF(fp,'res%d'%(ii))
                ii=ii+1

            self.resonator.closeHDF(fp)


    def loadResonators(self,fname):

            fp=self.resonator.openHDFR(fname)


            ii=1
            self.reslist=[]

            for k in fp.keys():
                if k[0:7]=='ResData':
                  res=resonatorData(int(random.random()*1000000),self.device_name)

                  res.readHDF(fp,k[8:])
                  self.addRes(res)


            self.resonator.closeHDF(fp)



    #
    # correct for bad xmission line delay meas. add line to the phase to change its slope to flat.
    #
    def addLineToPhase(self):


        print 'fit.addLineToPhase'
        iqp=self.resonator.RectToPolar(self.resonator.iqdata)

        phase=iqp[1];
        phase = self.removeTwoPi(phase)
        lx=len(phase)

        slope=(phase[lx-1] - phase[0])/lx

        newline=arange(0,lx)*slope
        phase = phase-newline;
        iqp[1]=phase
        self.resonator.iqdata=self.resonator.PolarToRect(iqp)


        #rf band freq of noise data
        fv=self.resonator.fftcarrierfreq[0] - self.resonator.srcfreq[0]

        #find the offset of newline at that freq.
        dfreq=self.resonator.freqs[1] - self.resonator.freqs[0]
        freq0=self.resonator.freqs[0]

        #noise freqoffset
        npoints=(fv-freq0)/dfreq;

        #noise phase change
        nphase=npoints*slope

        ntr = int(self.resonator.num_noise_traces)


        for k in range(ntr):
            iqn=self.resonator.iqnoise[k]
            iqnp=self.resonator.RectToPolar(iqn)
            phase=iqnp[1]-nphase
            iqnp[1] = phase;
            self.resonator.iqnoise[k]=self.resonator.PolarToRect(iqnp)        

        #store to resonator...
        self.resonator.newline=newline

        self.resonator.newline_slope=slope

        self.resonator.noise_linephase=nphase



    #self.fitprint(na.findResPhase(na.iqdata,0,3500e6)
    #self.fitprint(na.findResAmp(na.iqdata,0,3500e6)

    def findResAmp(self,thresh):
            iqp=self.resonator.RectToPolar(self.resonator.iqdata)
            freqs=self.resonator.freqs


            #take 2nd dirivitive and take over thresh.
            # 2nd diriv is the "acceleration" or curvature of the amp versus freq curve
            # the max of the 2nd deriv will be at centers of resonance.
            iqpd2=diff(diff(iqp[0]))

            if self.fit_plots:
                figure(3);clf();plot(iqpd2)


            if thresh==0.0:
                    baseline=median(iqpd2)
                    thresh=2*std(iqpd2) + baseline


            #add 1 because diff() takes the 1st point away from array
            indices=1+where(iqpd2>thresh)[0]




            return([indices, freqs[indices] , freqs[indices]])

    #assume ascending order numbers. group into 
    #gropups for numbers less then dstx apart
    def toGroups(self,data,dstx):

            allgroups=[]
            group=[]

            lastitem=data[0]
            group.append(lastitem)

            for k in range(1,len(data)):



                    if (data[k]-lastitem) <dstx:
                            group.append(data[k])

                    else:

                            allgroups.append(array(group))
                            group=[]
                            group.append(data[k])

                    lastitem=data[k]

            allgroups.append(array(group))
            return(allgroups)


    def removeTwoPi(self,phases):
            offset=0;
            for k in range(len(phases)-1):


                    dphs=phases[k+1]-phases[k]
                    if abs(dphs)>3.1416:
                            offset= (-1.0 * sign(dphs) * 2*3.141592653589793)

                            for k2 in range(k,len(phases)-1):
                                    phases[k2+1]=phases[k2+1] + offset

            return(phases)





    def findResPhase(self,nsd=2.0):

            thresh=0.0

            iq=self.resonator.iqdata


            iqp=self.RectToPolar(iq)
            freqs=self.resonator.freqs




            #take out 2pi jumps in phase generated by atan function.
            phases=iqp[1];

            #unwrap the phaes- remove the 2pi jumps
            phases=self.removeTwoPi(phases)


            #take  dirivitive and take over thresh.


            #iqpd1=diff(iqp[1])

            iqpd1 = sqrt(( diff(iq[0]) )**2 + (diff(iq[1]))**2)




            iqpd2=numpy.copy(iqpd1)
            baseline=median(iqpd1)


            #because the 1st bin has a spike for some reason., set to median.
            iqpd2[0]=baseline
            iqpd1[0]=baseline

            #set  300 largest values to median. so the resonator does not contribute
            #to the std. this allows searching data w/ no resonator. so only noise contrib
            #to std and tresh, and not res itself.

            for kk in range(300):
                    ii=numpy.argmax(iqpd2);
                    iqpd2[ii]=baseline



            #calc thresh on the version of data w/ max'es removed.

            thresh=nsd*std(iqpd2) + baseline

            if self.fit_plots:

                figure(4);clf();
                subplot(3,1,1)

                plot(iqpd1);
                subplot(3,1,2)
                plot(iqp[0])

                subplot(3,1,3)
                plot(phases,'g')

                #threshold line
                tline=thresh*ones(len(phases))

                subplot(3,1,1)
                plot(tline,'y')


            #add 1 because diff() takes the 1st point away from array
            _indices=1+where(iqpd1>thresh)[0]


            if (len(_indices)>0):
                    allgroups=self.toGroups(_indices,20)

                    self.fitprint("Number of Resonances Found: %d"%(len(allgroups)))


                    indices=[]

                    for group in allgroups:
                            idx=int(round(median(group)))
                            indices.append(idx)

                            if self.fit_plots:
                                subplot(3,1,1)
                                plot(idx,iqpd1[idx-1],'rx')
                                subplot(3,1,3)
                                plot(idx,phases[idx],'rx')

                                subplot(3,1,2)
                                plot(idx,iqp[0][idx],'rx')

                    self.resonator.ig_numresfreq=len(indices)
                    self.resonator.ig_indices=indices
                    self.resonator.ig_bump=iqpd1
                    self.resonator.ig_resfreqlist=freqs[indices]



                    return([indices, freqs[indices] ])

            else:
                    return([None,None])





    def RectToPolar(self,data):

            mags = numpy.sqrt(data[0]*data[0] + data[1]*data[1])
            phase=numpy.arctan2(data[1],data[0])
            return([mags,phase])

    def PolarToRect(self,data):
            mags=data[0]
            phase=data[1]
            re=mags*numpy.cos(phase)
            im=mags*numpy.sin(phase)
            return([re,im])











    def report(self):
        contents= inspect.getmembers(self)
        for c in contents:
                 self.fitprint(c)


    def report2(self):
        contents= inspect.getmembers(self)
        return(contents)

    def getTimestamp(self):        
            timestamp = "T".join( str( datetime.datetime.now() ).split() )
            return(timestamp)








    ####################################################
    #Calculate center and radius of a circle given x,y
    #   Uses circle fitting routine from Gao dissertation
    #From publication Chernov and Lesort, Journal of Mathematical Imaging and
    #Vision 23: 239-252, 2005. Springer Science
    # Updated: 01-09-2012 - alterted to work with 'Resonator' IQ data structure

    #The eigenvalue problem is to determine the nontrivial solutions of the 
    #equation Ax = ?xwhere A is an n-by-n matrix, x is a length n column vector, 
    #and ? is a scalar. The n values of ? that satisfy the equation are 
    #the eigenvalues, and the corresponding values of x are the right 
    #eigenvectors. The MATLAB function eig solves for the eigenvalues ?, 
    #and optionally the eigenvectors x. The generalized eigenvalue problem 
    #is to determine the nontrivial solutions of the equation Ax = ?Bx
    #where both A and B are n-by-n matrices and ? is a scalar. The values 
    #of ? that satisfy the equation are the generalized eigenvalues and 
    #the corresponding values of x are the generalized right eigenvectors.
    #If B is nonsingular, the problem could be solved by reducing it to a
    # standard eigenvalue problem B?1Ax = ?x

    #Because B can be singular, an alternative algorithm, called the QZ method, 
    #is necessary.
    #        
    #############################################

    def fit_circle2(self):
            self.resonator.applyDelay()
            x = self.resonator.iqdata_dly[0]
            y = self.resonator.iqdata_dly[1];


            n = len(x);
            w =(x**2+y**2);
            M=zeros([4,4])
            #create moment matrix
            M[0,0] = sum(w*w);
            M[1,0] = sum(x*w);
            M[2,0] = sum(y*w);
            M[3,0] = sum(w);
            M[0,1] = sum(x*w);
            M[1,1] = sum(x*x);
            M[2,1] = sum(x*y);
            M[3,1] = sum(x);
            M[0,2] = sum(y*w);
            M[1,2] = sum(x*y);
            M[2,2] = sum(y*y);
            M[3,2] = sum(y);
            M[0,3] = sum(w);
            M[1,3] = sum(x);
            M[2,3] = sum(y);
            M[3,3] = n;

            #constraint matrix
            B = array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]])



            #Calculate eigenvalues and functions

            #[V,D] = eig(M,B); %calculate eigens

            VX=scipy.linalg.eig(M, B)

            X=VX[0]
            V=VX[1]

            #X = linalg.diag(D);  %creates column array of eigenvalues
            #X=diag(D)



            #[C,IX] = sort(X); %sorts iegen values into Y, places index in IX 


            C=sort(X,0)
            IX=argsort(X,0)


            #Values = V[:,IX[2]]); % we want eigenfunction of first positive eigenvalue (IX(2)) becuase IX(1) is neg

            Values = V[:,IX[1]]
            #% Column vector Values is then [A,B,C,D] from Gao dissertaion
            xc = -Values[1]/(2*Values[0]);
            yc = -Values[2]/(2*Values[0]);
            R = (xc**2+yc**2-Values[3]/Values[0])**0.5;


            #store to res structure
            self.resonator.cir_xc=xc
            self.resonator.cir_yc=yc
            self.resonator.cir_R=R

            return([xc,yc,R])









    ####################################################
    #Calculate center and radius of a circle given x,y
    #   Uses circle fitting routine from Gao dissertation
    #From publication Chernov and Lesort, Journal of Mathematical Imaging and
    #Vision 23: 239-252, 2005. Springer Science
    # Updated: 01-09-2012 - alterted to work with 'Resonator' IQ data structure

    #The eigenvalue problem is to determine the nontrivial solutions of the 
    #equation Ax = ?xwhere A is an n-by-n matrix, x is a length n column vector, 
    #and ? is a scalar. The n values of ? that satisfy the equation are 
    #the eigenvalues, and the corresponding values of x are the right 
    #eigenvectors. The MATLAB function eig solves for the eigenvalues ?, 
    #and optionally the eigenvectors x. The generalized eigenvalue problem 
    #is to determine the nontrivial solutions of the equation Ax = ?Bx
    #where both A and B are n-by-n matrices and ? is a scalar. The values 
    #of ? that satisfy the equation are the generalized eigenvalues and 
    #the corresponding values of x are the generalized right eigenvectors.
    #If B is nonsingular, the problem could be solved by reducing it to a
    # standard eigenvalue problem B?1Ax = ?x

    #Because B can be singular, an alternative algorithm, called the QZ method, 
    #is necessary.
    #
    #supply resonator objhect. give center freq we think whre res is, then fit only a span
    #this is for plots w/ curles at end of the res, and for data w/ wide span.        
    #############################################

    def fit_circle3(self,resdata,fc_rf_Hz,span_Hz):

            self.resonator= resdata

            #get index in freqs where fc is in Hz, rf freq.
            fc_i = int(len(self.resonator.freqs)/2)
            for i in range(len(self.resonator.freqs)):
                if self.resonator.freqs[i] < fc_rf_Hz:
                    fc_i = i

            d_i = (span_Hz/2.0)/self.resonator.incrFreq_Hz

            st=fc_i - d_i
            ed = fc_i + d_i

            if st<0: st=0
            if ed>len(self.resonator.freqs): ed = len(self.resonator.freqs)

            self.resonator.applyDelay()

            x = self.resonator.iqdata_dly[0][st:ed]
            y = self.resonator.iqdata_dly[1][st:ed]


            n = len(x);
            w =(x**2+y**2);
            M=zeros([4,4])
            #create moment matrix
            M[0,0] = sum(w*w);
            M[1,0] = sum(x*w);
            M[2,0] = sum(y*w);
            M[3,0] = sum(w);
            M[0,1] = sum(x*w);
            M[1,1] = sum(x*x);
            M[2,1] = sum(x*y);
            M[3,1] = sum(x);
            M[0,2] = sum(y*w);
            M[1,2] = sum(x*y);
            M[2,2] = sum(y*y);
            M[3,2] = sum(y);
            M[0,3] = sum(w);
            M[1,3] = sum(x);
            M[2,3] = sum(y);
            M[3,3] = n;

            #constraint matrix
            B = array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]])



            #Calculate eigenvalues and functions

            #[V,D] = eig(M,B); %calculate eigens

            VX=scipy.linalg.eig(M, B)

            X=VX[0]
            V=VX[1]

            #X = linalg.diag(D);  %creates column array of eigenvalues
            #X=diag(D)



            #[C,IX] = sort(X); %sorts iegen values into Y, places index in IX 


            C=sort(X,0)
            IX=argsort(X,0)


            #Values = V[:,IX[2]]); % we want eigenfunction of first positive eigenvalue (IX(2)) becuase IX(1) is neg

            Values = V[:,IX[1]]
            #% Column vector Values is then [A,B,C,D] from Gao dissertaion
            xc = -Values[1]/(2*Values[0]);
            yc = -Values[2]/(2*Values[0]);
            R = (xc**2+yc**2-Values[3]/Values[0])**0.5;


            #store to res structure
            self.resonator.cir_xc=xc
            self.resonator.cir_yc=yc
            self.resonator.cir_R=R

            return([xc,yc,R])










    # function width = fwhm(x,y)
    #
    # Full-Width at Half-Maximum (FWHM) of the waveform y(x)
    # and its polarity.
    # The FWHM result in 'width' will be in units of 'x'
    #
    #
    # Rev 1.2, April 2006 (Patrick Egan)
    # Remove portion about if not pulse and only one edge (Nino)


    def fwhm(self,x,y):


        y = y / max(y);
        N = len(y);

        # lev50 = 0.5;
        lev50 = 1-abs(max(y)-min(y))/2.0;
        # find index of center (max or min) of pulse
        if y[0] < lev50:                  
            garbage=max(y);
            centerindex = where(y==garbage)[0][0]
            Pol = +1;
        else:
            garbage=min(y);
            centerindex = where(y==garbage)[0][0]    
            Pol = -1;

        i = 1;
        while sign(y[i]-lev50) == sign(y[i-1]-lev50):
            i = i+1;

        interp = (lev50-y[i-1]) / (y[i]-y[i-1]);
        tlead = x[i-1] + interp*(x[i]-x[i-1]);
        #start search for next crossing at center
        i = centerindex+1;                    
        while ((sign(y[i]-lev50) == sign(y[i-1]-lev50)) & (i <= N-1)):
            i = i+1;

        interp = (lev50-y[i-1]) / (y[i]-y[i-1]);
        ttrail = x[i-1] + interp*(x[i]-x[i-1]);
        width = ttrail - tlead;
        return(width)









    #[xf,yf] Rotates and translates circle to origin
    #   Step 3 in Gao fitting procedure
    #   Takes intial x,y circle data and center and radius from fit_circle.m
    # Updated 01-09-2012: changed to work with 'Resonator' IQ data structure
    # and function 'fit_circle2' to generat 'Circle' structure.

    def trans_rot2(self):

            xc=self.resonator.cir_xc
            yc=self.resonator.cir_yc
            r=self.resonator.cir_R

            #Import data
            x = self.resonator.iqdata_dly[0];
            y = self.resonator.iqdata_dly[1];

            #correct data
            alpha = arctan2(yc,xc);
            xf = (xc-x)*cos(alpha) + (yc-y)*sin(alpha);
            yf = -(xc-x)*sin(alpha) + (yc-y)*cos(alpha);

            #find S21 and Fcenter
            mag2s21 = xf**2+yf**2;
            #This is the data format to work with for fitting |s21|^2 in dB
            mag2s21dB = 10*log10(mag2s21/max(mag2s21)); 

            c= min(mag2s21);
            cidx= argmin(mag2s21);

            self.resonator.trot_S21=mag2s21dB
            self.resonator.trot_xf=xf
            self.resonator.trot_yf=yf
            self.resonator.trot_Fcenter=self.resonator.freqs[cidx]



            return([xf,yf])



    def trans_rot3(self,resdata, iq):


            xc=resdata.cir_xc
            yc=resdata.cir_yc
            r=resdata.cir_R

            #Import data
            x = iq[0];
            y = iq[1];

            #correct data
            alpha = arctan2(yc,xc);
            xf = (xc-x)*cos(alpha) + (yc-y)*sin(alpha);
            yf = -(xc-x)*sin(alpha) + (yc-y)*cos(alpha);



            return([xf,yf])


    #Ninos code converted to py

    # Using FitAllLMFnlsq (no Toolbox needed!) ... Perform the following Fits to IQ resonator data
    #   1.) Phase fit on centered IQ data
    #   2.) Skewed Lorentz
    #
    # Notes: 
    #         1.) The second optional argument is a filename to save the output
    #             to a PDF file.
    #
    #         2.) Data should already be DC subtracted and cable delay applied
    #         already by other functions (e.g., DCbias_subtract() and IQ_cable_delay()
    #
    #         3.) Each fitting does an initial fit some reasonable gueses, then
    #         we randomly vary the initial fitted parameters some reasonable
    #         amount and re-run the fit to see if the ssq improves. This is add
    #         some robustness to the fit since it can sometimes get stuck in a
    #         local minimum
    # 
    #  2/15/2012 Much code derived from Tom's Lorentz_fitter6 Nino
    #


    def NinoInitialGuess(self):

        
        
        NUM_GUESSES_PHASE = 5000;
        NUM_GUESSES_LORENTZ = 1000;

        iq=self.resonator.iqdata

        #array of offset baseband freqs for each I Q sample
        freqs=self.resonator.freqs


        j=complex(0,1)

        #I = iq[0][::-1]
        #Q = iq[1][::-1] 
        I = iq[0]
        Q = iq[1]
        z = I +j*Q;

        mag2s21 = I**2+Q**2;

        mag2s21dB = 10*log10(mag2s21/max(mag2s21)); 
        mindex = where(mag2s21==min(mag2s21))[0][0];
        Fcenter = freqs[mindex];
        S21 = mag2s21dB;


        self.fitprint('PHASE FITTING!!!!!!')
        #### Phase Angle Fit 
        #### ---- First fit circle and then translate and rotate to center.

        #ise self.resonator.iqdata
        circle = self.fit_circle2(); #fit a circle to data



        #use self.resonator.iqdata, prev. circle fit stored in self,resonator
        IQcentered = self.trans_rot2(); #move coordinate system to center of circle


        z_centered = IQcentered[0] + j*IQcentered[1];

        phase = self.removeTwoPi(self.RectToPolar(IQcentered)[1]);



        # Using fwhm function in MKID\Matlab_code\Borrowed Code (from MathWorks
        # Exchange
        # figure(1000);
        # plot(Resonator.freq, mag2s21,'r--');
        Qguess = Fcenter/self.fwhm(freqs, mag2s21);
        self.fitprint('Qguess for phase fit: %f\n'%(Qguess))



            #tim added this: guess sign.
        sgn=1.0
        if phase[0] > phase[len(phase)-1]:
                sgn=-1.0

        phase_guesses = [Qguess,  Fcenter,  median(phase),sgn];

        phzfit=phaseFunc(freqs,Qguess,Fcenter,median(phase),sgn )

        if self.fit_plots:
            figure(50);
            clf();
            plot(freqs,phase,'x')

            plot(freqs,phzfit,'g')


        self.resonator.phig_phase_guesses=phase_guesses

        self.resonator.phig_phase=phase
        self.resonator.phig_IQcentered=IQcentered
        self.resonator.phig_mag2s21=mag2s21
        self.resonator.phig_mag2s21dB=mag2s21dB

        return([phase_guesses, IQcentered,phase,freqs])



    def NinoFitPhase(self):   


        ###########################################################################
        ### PHASE FITTING!!!!!!
        # Fitting function: phase(x) = theta0 - 2*atan(2*Q* (1-x/fr))
        #     param(1) = Q
        #     param(2) = fr
        #     param(3) = theta0
        # Reference: Gao's thesis Equation E.11 (Also: Petersan, P. J. and Anlage, S.
        # M. 1998, J. Appl. Phys., 84, 3392 250)


        #!! changed sign...


        phase_guesses = self.resonator.phig_phase_guesses;
        phase=self.resonator.phig_phase
        freqs=self.resonator.freqs


        #parinfo = [{'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.]}]*10
        parinfo=[ {'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.], 'parname':'NULL'} for i in range(4) ]

        #       Q = p[0]          ;  Q
        #       f0 = p[1]         ;  resonance frequency
        #       phasecenter = p[2]      ;  amplitude of leakage






        #Q
        parinfo[0]['parname']='Q factor'
        parinfo[0]['value'] = phase_guesses[0]
        parinfo[0]['limits'] = [100,1e6]

        #f0
        parinfo[1]['parname']='f0, Res freq'
        parinfo[1]['value'] = phase_guesses[1]
        parinfo[1]['limits'] = [ min(freqs),max(freqs)]

        parinfo[2]['parname']='phase median'
        parinfo[2]['value'] = phase_guesses[2]
        parinfo[2]['limits'] = [-20.0,20.0]

        parinfo[3]['parname']='phase sign'
        parinfo[3]['value'] = phase_guesses[3]
        parinfo[3]['limits'] = [-1.0,1.0]
        parinfo[3]['fixed'] = 1


        weights = ones(len(freqs))
        fa = {'x':freqs, 'y':phase, 'err':weights}

        m = mpfit.mpfit(residPhase,functkw=fa,parinfo=parinfo,quiet=1)



        #now wqe run fitter many times w/ random guesses. 
        q_guess = abs(m.params[0]);
        f_guess = m.params[1];

        # Frequency parameter was out of the range for some reason; Set back to the
        # Fcenter
        if (m.params[1] < min(self.resonator.freqs)) or (m.params[1] > max(self.resonator.freqs)):
            m.params[1] = self.resonator.trot_Fcenter;

        chisq = m.fnorm

        iter_phase=m.niter

        phase_func_params=m.params
        #  Randomly change the fit parameters and re-run the fitter....
        for ii in range(int(self.resonator.NUM_GUESSES_PHASE)):
            q_guess =     abs(q_guess + 2*q_guess*(random.random()-0.5));
            freq_guess =  f_guess + (max(self.resonator.freqs) - min(self.resonator.freqs))*(random.random()-0.5);

            if freq_guess > max(self.resonator.freqs) or  freq_guess < min(self.resonator.freqs):
                freq_guess = self.resonator.trot_Fcenter;

                phase_guess = phase_func_params[2] + 2*phase_func_params[2]*(random.random()-0.5);

            if random.random()>0.5:
                sgn=1.0
            else:
                sgn=-1.0

            phase_guesses = [q_guess,  freq_guess,  phase_guess, sgn];




            parinfo[0]['value'] = phase_guesses[0]        
            parinfo[1]['value'] = phase_guesses[1]                
            parinfo[2]['value'] = phase_guesses[2]                
            parinfo[3]['value'] = phase_guesses[3]


            mtry = mpfit.mpfit(residPhase,functkw=fa,parinfo=parinfo,quiet=1)

            newchisq = mtry.fnorm

            if (mtry.niter>0 and newchisq<chisq and  (mtry.params[1] > min(self.resonator.freqs)) and (mtry.params[1] < max(self.resonator.freqs))):

                phase_func_params = mtry.params;
                chisq = newchisq;
                iter_phase = mtry.niter; 
                self.fitprint('**** Phase fitting: Newest Ssq_phase: %.8f, iteration: %d\n'%(chisq,ii))
                self.fitprint('**** Phase fitting: fr:%f, q:%f iter_phase: %d \n'%(phase_func_params[1],phase_func_params[0], iter_phase))






        if self.fit_plots:
            figure(100)
            clf()


            plot(freqs,phase,'x');
            plot(freqs,phaseFunc(freqs,self.resonator.phig_phase_guesses[0],self.resonator.phig_phase_guesses[1],self.resonator.phig_phase_guesses[2] ,self.resonator.phig_phase_guesses[3]),'g')
            plot(freqs,phaseFunc(freqs,m.params[0],phase_func_params[1],phase_func_params[2],phase_func_params[3] ),'r')


        self.resonator.ph_Qf=phase_func_params[0]
        self.resonator.ph_fr=phase_func_params[1]
        self.resonator.ph_theta=phase_func_params[2]
        self.resonator.ph_sgn=phase_func_params[3]


        return(phase_func_params)




    ###########################################################################
    #### SKEWED LORENTZ!!!!
    #### -- NB: requires data that is NOT centered!!!!  
    #### -- Only DC offset has to be removed!!!!
    #### Reference: Gao's thesis Equation E.17
    # # A(1) = A
    # # A(2) = B
    # # A(3) = C
    # # A(4) = D
    # # A(5) = fr
    # # A(6) = Q
    # # f = A(1) + A(2).*(x-A(5))+((A(3)+A(4).*(x-A(5)))./(1+4.*(A(6).^2).*((x-A(5))./A(5)).^2));


    def NinoLorentzGuess(self):




        iq=self.resonator.iqdata

        #array of offset baseband freqs for each I Q sample
        freqs=self.resonator.freqs


        j=complex(0,1)

        mag2s21 = self.resonator.phig_mag2s21

        lorentz_guesses =[0,0,0,0,0,0]
        lorentz_guesses[0] = sum(mag2s21[0:50])/50.0
        lorentz_guesses[1] = 0.5/self.resonator.ph_fr
        lorentz_guesses[2] = 1.0
        lorentz_guesses[3] = 1.0/self.resonator.ph_fr
        lorentz_guesses[4] = self.resonator.ph_fr
        lorentz_guesses[5] = self.resonator.ph_Qf



        self.fitprint('lorentz_guess_params \n')
        self.fitprint(lorentz_guesses)

        self.resonator.lrnzig_params=lorentz_guesses


        if self.fit_plots:
            figure(101)
            clf()
            plot(freqs,lorentzFunc(freqs,lorentz_guesses),'r')
            plot(freqs,mag2s21,'x')



        return(lorentz_guesses)




    def NinoFitLorentz(self):   


        ###########################################################################
        ### PHASE FITTING!!!!!!
        # Fitting function: phase(x) = theta0 - 2*atan(2*Q* (1-x/fr))
        #     param(1) = Q
        #     param(2) = fr
        #     param(3) = theta0
        # Reference: Gao's thesis Equation E.11 (Also: Petersan, P. J. and Anlage, S.
        # M. 1998, J. Appl. Phys., 84, 3392 250)


        #!! changed sign...


        lorentz_guesses = self.resonator.lrnzig_params;
        mags=self.resonator.phig_mag2s21
        freqs=self.resonator.freqs


        #parinfo = [{'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.]}]*10
        parinfo=[ {'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.], 'parname':'NULL'} for i in range(6) ]

        #       Q = p[0]          ;  Q
        #       f0 = p[1]         ;  resonance frequency
        #       phasecenter = p[2]      ;  amplitude of leakage






        #Q
        parinfo[0]['parname']='A'
        parinfo[0]['value'] = lorentz_guesses[0]
        parinfo[0]['limits'] = [-10.,10.]

        #f0
        parinfo[1]['parname']='B'
        parinfo[1]['value'] = lorentz_guesses[1]
        parinfo[1]['limits'] = [-10.,10.]

        parinfo[2]['parname']='C'
        parinfo[2]['value'] = lorentz_guesses[2]
        parinfo[2]['limits'] = [-10.,10.]

        parinfo[3]['parname']='D'
        parinfo[3]['value'] = lorentz_guesses[3]
        parinfo[3]['limits'] = [-10.,10.]


        parinfo[4]['parname']='fr'
        parinfo[4]['value'] = lorentz_guesses[4]
        parinfo[4]['limits'] = [ min(self.resonator.freqs),max(self.resonator.freqs)]


        parinfo[5]['parname']='Qf'
        parinfo[5]['value'] = lorentz_guesses[5]
        parinfo[5]['limits'] = [1.0,1.0e7]



        weights = ones(len(freqs))
        fa = {'x':freqs, 'y':mags, 'err':weights}

        m = mpfit.mpfit(residPhase,functkw=fa,parinfo=parinfo,quiet=1)

        lorentz_func_params=m.params
        chisq = m.fnorm
        iter_lrnz=m.niter



        # Frequency parameter was out of the range for some reason; Set back to the
        # Fcenter
        if (lorentz_func_params[4] < min(self.resonator.freqs)) or (lorentz_func_params[4] > max(self.resonator.freqs)):
            m.lorentz_func_params[4] = self.resonator.trot_Fcenter;
            self.fitprint('SKEWED LORENTZ FITTING: First Fr out of span.. setting to Fcenter....\n')

        fitgood=lorentzFunc(self.resonator.freqs,lorentz_func_params);

        #  Randomly change the fit parameters and re-run the fitter....
        for ii in range(int(self.resonator.NUM_GUESSES_LORENTZ)):
            self.fitprint(ii)

            A = lorentz_func_params[0] + 10.0*lorentz_func_params[0]*(random.random()-0.5);
            B = lorentz_func_params[1] + 10.0*lorentz_func_params[1]*(random.random()-0.5);
            C = lorentz_func_params[2] + 10.0*lorentz_func_params[2]*(random.random()-0.5);
            D = lorentz_func_params[3] + 10.0*lorentz_func_params[3]*(random.random()-0.5);


            q_guess =     abs(self.resonator.ph_Qf + self.resonator.ph_Qf*(random.random()-0.5));
            freq_guess =  lorentz_func_params[4] + (max(self.resonator.freqs) - min(self.resonator.freqs))*(random.random()-0.5);

            if freq_guess > max(self.resonator.freqs) or  freq_guess < min(self.resonator.freqs):
                freq_guess = self.resonator.trot_Fcenter;



            lorentz_guesses = [A, B, C, D, freq_guess, q_guess ];

            parinfo[0]['value'] = lorentz_guesses[0]        
            parinfo[1]['value'] = lorentz_guesses[1]                
            parinfo[2]['value'] = lorentz_guesses[2]                
            parinfo[3]['value'] = lorentz_guesses[3]
            parinfo[4]['value'] = lorentz_guesses[4]
            parinfo[5]['value'] = lorentz_guesses[5]


            mtry = mpfit.mpfit(residLorentz,functkw=fa,parinfo=parinfo,quiet=1)

            newchisq = mtry.fnorm


            fitx=lorentzFunc(self.resonator.freqs,mtry.params);

            if self.fit_plots:
                figure(60);clf();
                plot(freqs, fitx,'g')
                plot(freqs, fitgood,'r')
                plot(freqs, mags,'x')
                draw()


            if (mtry.niter>0 and newchisq<chisq and  (mtry.params[4] > min(self.resonator.freqs)) and (mtry.params[4] < max(self.resonator.freqs))):

                lorentz_func_params = mtry.params;


                fitgood=lorentzFunc(self.resonator.freqs,lorentz_func_params);
                chisq = newchisq;
                iter_lrnz = mtry.niter; 


                self.resonator.lorentz_params=lorentz_func_params
                self.resonator.lorentz_fr = lorentz_func_params[4];
                self.resonator.lorentz_ssq = chisq;
                self.resonator.lorentz_iter = iter_lrnz;
                self.fitprint('**** LRnz fitting: Newest Ssq_phase: %.8f, iteration: %d\n'%(chisq,ii))
                self.fitprint('**** LRnz fitting: fr:%f, q:%f iter_phase: %d \n'%(lorentz_func_params[4],lorentz_func_params[5], iter_lrnz))






        return(lorentz_func_params)

    def lorentzEndCalcs(self):

        lorentz_func_params=self.resonator.lorentz_params
        mag2s21 = self.resonator.phig_mag2s21

        # Calculate Qc and Qi from s21min from the Lorentz fit
        mag2s21fit = lorentzFunc(self.resonator.freqs,lorentz_func_params);
        mag2s21norm = mag2s21/max(mag2s21fit);
        mag2s21fitnorm = mag2s21fit/max(mag2s21fit);
        mag2s21dB = 10*log10(mag2s21norm);
        mag2s21fitdB = 10*log10(mag2s21fitnorm);
        s21min = 10**(min(mag2s21fitdB)/20);
        # Use min of s21 from the data if the fit min is 1dB (i.e., 0 in absolute units) 
        if s21min == 1.0:
               s21min = 10^(min(mag2s21dB)/20); 
               self.fitprint('** lorentz WARNING: Using min21 from data, not fit... \n')

        Qr = abs(lorentz_func_params[5]);
        Qc = Qr/(1-s21min); 
        Qi = (Qc*Qr)/(Qc-Qr);


        ### self.resonator
        self.resonator.lorentz_Q = Qr;
        self.resonator.lorentz_Qc = Qc;
        self.resonator.lorentz_Qi = Qi;

        # get theta from Fr using Lorentz fit (I think theta is different from the
        # theta from the phase fit!!! Figure out the differnce!!!
        self.fitprint('self.resonator.lorentz_fr: %f\n'%(self.resonator.lorentz_fr))

        #self.resonator.lorentz_theta = theta_find_fr(self.resonator.lorentz_fr,Resonator);
        #temporarily deactivated for the fit IQ traces from VNA. There is an error
        #message not well understood. For the purpose of the paper on noise
        #reduction with thickness we don't need theta. Rememeber to reactivate when
        #needed to fit data from the IQ mixer. 09-17-2012


        self.resonator.lorentz_s21min = s21min;







    def lorentzPlots(self):

        mags=self.resonator.phig_mag2s21
        freqs=self.resonator.freqs
        params=self.resonator.lorentz_params

        mag2s21fit = lorentzFunc(freqs,params);


        phase=self.resonator.phig_phase

        frindx=min(where(self.resonator.lorentz_fr<=self.resonator.freqs)[0])

        figure(102)
        clf()
        subplot(2,1,1)

        plot(freqs,mag2s21fit,'r')
        plot(freqs,mags,'x')
        plot(self.resonator.lorentz_fr,lorentzFunc(self.resonator.lorentz_fr,params),'^')
        plot(freqs[frindx],mags[frindx],'o')
        subplot(2,1,2)
        plot(freqs,phase,'x')

        figure(103)
        pp=self.RectToPolar([self.resonator.trot_xf,self.resonator.trot_yf ])

        clf()
        polar(pp[1],pp[0],'x')

        polar(pp[1][frindx],pp[0][frindx],'o')



        figure(100)
        clf()


        plot(freqs,phase,'x');
        plot(freqs,phaseFunc(freqs,self.resonator.phig_phase_guesses[0],self.resonator.phig_phase_guesses[1],self.resonator.phig_phase_guesses[2] ,self.resonator.phig_phase_guesses[3]),'g')
        plot(freqs,phaseFunc(freqs,self.resonator.ph_Qf,self.resonator.ph_fr,self.resonator.ph_theta,self.resonator.ph_sgn ),'r')





###########################################################################
    #### SKEWED Circle!!!! # added by cecil
    #### -- NB: requires data that is NOT centered!!!!  
    #### -- Only DC offset has to be removed!!!!
    #### Reference: Geerlings et al Applied Physics letters 100, 192601 (2012)
    # # A(0) = Qo
    # # A(1) = Qc
    # # A(2) = wr
    # # A(3) = dw
    # # A(4) = mag2S21 offset
    # # f (S21) = 1+ ((A(1)/A(2)-2j*A(1)*A(4)/A(3))/(1+2j*A(1)*(w-A(3))/A(3)));


    def CecilSkewcircleGuess(self):

        iq=self.resonator.iqdata

        #array of offset baseband freqs for each I Q sample
        freqs=self.resonator.freqs


        j=complex(0,1)
        I = iq[0]
        Q = iq[1]
        #S21 = abs(I + j*Q)
        #S21norm = S21/S21[0] #normalize to 'off resonance' value
        mag2s21 = I**2 + Q**2
        mag2s21norm = mag2s21/mag2s21[0]
        mag2S21dB = 10*log10(mag2s21norm)
        mags = mag2S21dB

        skewcircle_guesses =[0,0,0,0]
        skewcircle_guesses[0] = self.resonator.lorentz_Q
        skewcircle_guesses[1] = self.resonator.lorentz_Qc
        skewcircle_guesses[2] = self.resonator.lorentz_fr
        #skewcircle_guesses[3] = self.resonator.lorentz_fr/self.resonator.lorentz_Q
        skewcircle_guesses[3] = 0.0
        #skewcircle_guesses[4] = sum(mag2S21dB[0:50])/50.0

        self.fitprint('skewcircle_guess_params \n')
        self.fitprint(skewcircle_guesses)

        self.resonator.skewcircle_params=skewcircle_guesses


        if self.fit_plots:
            figure(401)
            clf()
            plot(freqs,SkewcircleFunc(freqs,skewcircle_guesses),'r')
            plot(freqs,mag2S21dB,'x')



        return(skewcircle_guesses)





    def CecilfitSkewcircle(self):   


        ###########################################################################
        ### Skewed Circle FITTING!!!!!!
        # uses S21 equation from Appl. Phys. Lett. 100, 192601 (2012)

        j=complex(0,1)

        self.fitprint("Skewed circle fitting")
        skewcircle_guesses = self.resonator.skewcircle_params;
        I = self.resonator.iqdata[0]
        Q = self.resonator.iqdata[1]
        #S21 = abs(I + j*Q)
        #S21norm = S21/S21[0] #normalize to 'off resonance' value
        mag2s21 = I**2 + Q**2
        mag2s21norm = mag2s21/mag2s21[0]
        mag2S21dB = 10*log10(mag2s21norm)
        mags = mag2S21dB

        freqs=self.resonator.freqs


        #parinfo = [{'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.]}]*10
        parinfo=[ {'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.], 'parname':'NULL'} for i in range(4) ]


        #Fitter parameters
        parinfo[0]['parname']='Q0'
        parinfo[0]['value'] = skewcircle_guesses[0]
        parinfo[0]['limits'] = [1.0,1.0e7]

        parinfo[1]['parname']='Qc'
        parinfo[1]['value'] = skewcircle_guesses[1]
        parinfo[1]['limits'] = [1.0,1.0e7]

        parinfo[2]['parname']='fr'
        parinfo[2]['value'] = skewcircle_guesses[2]
        parinfo[2]['limits'] = [ min(self.resonator.freqs),max(self.resonator.freqs)]

        parinfo[3]['parname']='dw'
        parinfo[3]['value'] = skewcircle_guesses[3]
        parinfo[3]['limits'] = [-1.0e6,1.0e6]

        #parinfo[4]['parname']='mag2S21_offset'
        #parinfo[4]['value'] = skewcircle_guesses[4]
        #parinfo[4]['limits'] = [skewcircle_guesses[4]-10.0,skewcircle_guesses[4]+10.0]



        weights = ones(len(freqs))
        fa = {'x':freqs, 'y':mags, 'err':weights}

        m = mpfit.mpfit(residSkewcircle,functkw=fa,parinfo=parinfo,quiet=1)

        skewcircle_func_params=m.params
        chisq = m.fnorm
        iter_swcrl=m.niter


        # Frequency parameter was out of the range for some reason; Set back to the
        # Fcenter
        if (skewcircle_func_params[2] < min(self.resonator.freqs)) or (skewcircle_func_params[2] > max(self.resonator.freqs)):
            m.skewcircle_func_params[2] = self.resonator.trot_Fcenter;
            self.fitprint('SKEWED CIRCLE FITTING: First Fr out of span.. setting to Fcenter....\n')

        fitgood=SkewcircleFunc(self.resonator.freqs,skewcircle_func_params);

        #  Randomly change the fit parameters and re-run the fitter.... multiples by up to 5X and adds
        for ii in range(int(self.resonator.NUM_GUESSES_SKEWCIRCLE)):
            self.fitprint(ii)
            self.fitprint( chisq)

            A = skewcircle_func_params[0] + 2.0*skewcircle_func_params[0]*(random.random()-0.5);
            B = skewcircle_func_params[1] + 2.0*skewcircle_func_params[1]*(random.random()-0.5);
            C = skewcircle_func_params[2] + 1.0e-4*skewcircle_func_params[2]*(random.random()-0.5);
            D = skewcircle_func_params[3] + 1.0e5*(random.random()-0.5);
                #D = skewcircle_func_params[3] + 1e4*skewcircle_func_params[3]*(random.random()-0.5);
            #E = skewcircle_func_params[4]# + 10.0*skewcircle_func_params[4]*(random.random()-0.5);
            #self.fitprint(ii, chisq, A, B, C, D

            if C > max(self.resonator.freqs) or  C < min(self.resonator.freqs):
                #freq_guess = self.resonator.trot_Fcenter;
                    C = self.resonator.trot_Fcenter;


            skewcircle_guesses = [A, B, C, D];  ### should I be using f_guess and q_guess in here

            parinfo[0]['value'] = skewcircle_guesses[0]        
            parinfo[1]['value'] = skewcircle_guesses[1]                
            parinfo[2]['value'] = skewcircle_guesses[2]                
            parinfo[3]['value'] = skewcircle_guesses[3]
            #parinfo[4]['value'] = skewcircle_guesses[4]


            mtry = mpfit.mpfit(residSkewcircle,functkw=fa,parinfo=parinfo,quiet=1)

            newchisq = mtry.fnorm


            fitx=SkewcircleFunc(self.resonator.freqs,mtry.params);

            if self.fit_plots:
                figure(402);clf();
                plot(freqs, fitx,'g')
                plot(freqs, fitgood,'r')
                plot(freqs, mags,'x')
                draw()


            if (mtry.niter>0 and newchisq<chisq and  (mtry.params[2] > min(self.resonator.freqs)) and (mtry.params[2] < max(self.resonator.freqs))):

                skewcircle_func_params = mtry.params;


                fitgood=SkewcircleFunc(self.resonator.freqs,skewcircle_func_params);
                chisq = newchisq;
                iter_swcrl = mtry.niter; 


                self.resonator.skewcircle_params=skewcircle_func_params
                self.resonator.skewcircle_fr = skewcircle_func_params[2];
                self.resonator.skewcircle_ssq = chisq;
                self.resonator.skewcircle_iter = iter_swcrl;
                self.fitprint('**** Skewcircle fitting: Newest Ssq_phase: %.8f, iteration: %d\n'%(chisq,ii))
                self.fitprint('**** Skewcircle fitting: fr:%f, q:%f iter_phase: %d \n'%(skewcircle_func_params[2],skewcircle_func_params[0], iter_swcrl))






        return(skewcircle_func_params)

    def SkewcircleEndCalcs(self):

        skewcircle_func_params=self.resonator.skewcircle_params
        mag2s21 = self.resonator.phig_mag2s21

        Qr = abs(skewcircle_func_params[0]);
        Qc = abs(skewcircle_func_params[1]); 
        Qi = (Qc*Qr)/(Qc-Qr);
        Pg = -5.0 - self.resonator.atten_U6 - self.resonator.atten_U7 - self.resonator.cryoAtt
        Pdiss = Pg*(2.0/Qi)*(Qr**2.0/Qc)
        Pint = Pg*(2.0/pi)*(Qr**2.0/Qc)


        ### self.resonator
        self.resonator.skewcircle_Q = Qr;
        self.resonator.skewcircle_Qc = Qc;
        self.resonator.skewcircle_Qi = Qi;
        #self.resonator.skewcircle_s21min = s21min;


    def SkewcirclePlots(self):
        j = complex(0,1)
        I = self.resonator.iqdata[0]
        Q = self.resonator.iqdata[1]
        S21 = abs(I + j*Q)
        S21norm = S21/S21[0] #normalize to 'off resonance' value
        mag2s21 = S21norm**2 #don't think I need this
        mag2S21dB = 20.0*log10(S21norm)
        mags = mag2S21dB            

        mags=self.resonator.phig_mag2s21
        freqs=self.resonator.freqs
        params=self.resonator.skewcircle_params

        mag2s21dBfit = SkewcircleFunc(freqs,params);


        phase=self.resonator.phig_phase

        frindx=min(where(self.resonator.lorentz_fr<=self.resonator.freqs)[0])

        figure(403)
        clf()
        subplot(2,1,1)

        plot(freqs,mag2s21dBfit,'r')
        plot(freqs,mag2S21dB,'x')
        subplot(2,1,2)
        plot(freqs,mags,'x')
        #plot(self.resonator.skewcircle_fr,SkewcircleFunc(self.resonator.skewcircle_fr,params),'^')
        plot(freqs[frindx],mags[frindx],'o')
        #subplot(2,1,2)


       #plot(freqs,phase,'x')

       # figure(333)
       # pp=self.RectToPolar([self.resonator.trot_xf,self.resonator.trot_yf ])

       # clf()
       # polar(pp[1],pp[0],'x')

       # polar(pp[1][frindx],pp[0][frindx],'o')







    #mazin code
    def smooth(self, x, window_len=10, window='hanning'):
    # smooth the data using a window with requested size.
    #
    # This method is based on the convolution of a scaled window with the signal.
    # The signal is prepared by introducing reflected copies of the signal 
    # (with the window size) in both ends so that transient parts are minimized
    # in the begining and end part of the output signal.
    #
    # input:
    #     x: the input signal 
    #     window_len: the dimension of the smoothing window
    #     window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
    #         flat window will produce a moving average smoothing.
    #
    # output:
    #     the smoothed signal
    #
    # example:
    #
    # import numpy as np        
    # t = np.linspace(-2,2,0.1)
    # x = np.sin(t)+np.random.randn(len(t))*0.1
    # y = smooth(x)
    #
    # see also: 
    #
    # numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    # scipy.signal.lfilter
    #
    # TODO: the window parameter could be the window itself if an array instead of a string   
    # 

        if x.ndim != 1:
            raise ValueError, "smooth only accepts 1 dimension arrays."

        if x.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."

        if window_len < 3:
            return x

        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

        s=np.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]
        #self.fitprint(len(s))

        if window == 'flat': #moving average
            w = np.ones(window_len,'d')
        else:
            w = getattr(np, window)(window_len)
        y = np.convolve(w/w.sum(), s, mode='same')
        return y[window_len-1:-window_len+1]


    def FitLoopMP(self):                    # Fit the sweep using the full IQ data with MPFIT!

        import mpfit
        # find center from IQ max


        #array of offset baseband freqs for each I Q sample
        freqs=self.startFreq_Hz + (numpy.arange(self.memLen4) * self.incrFreq_Hz)
        # as we use the negative sideband, we suybtract
        freqs=self.carrierfreq - freqs;


        I=self.iqdata[0]
        Q=self.iqdata[1]
        I=I[::-1]
        Q=Q[::-1]
        freqs=freqs[::-1]
        fsteps=len(I)


        vel = np.sqrt( (diff(I))**2 + (diff(Q))**2)

        svel = self.smooth(vel)
        cidx = (np.where(svel==max(svel)))[0]
        vmaxidx = cidx[0]

        if self.fit_plots:
            figure(12)
            clf()
            subplot(4,1,1)
            plot(svel);plot(vmaxidx,svel[vmaxidx],'rx')

        #center=self.findResPhase();

        # Try to pass fsteps/2 points but work even if closer to the edge than that
        low = cidx - fsteps/4
        if low < 0:
            low = 0

        high = cidx + fsteps/4
        if cidx > fsteps :
            high = fsteps

        #self.fitprint(cidx,low,high

        idx = freqs[low:high]
        #I = self.I[low:high]-self.I0
        #Q = self.Q[low:high]-self.Q0


        I = I[low:high]
        Q = Q[low:high]

        if self.fit_plots:
            figure(12);subplot(4,1,2)
            plot(I);plot(Q,'g')
            plot(self.RectToPolar([I,Q])[0],'r')

        s21 = np.zeros(len(I)*2)
        s21[:len(I)] = I
        s21[len(I):] = Q

        sigma = np.zeros(len(I)*2)

        #is this sd mening st deviation? Is it a point by point std based on noise?
        #sigma[:len(I)] = self.Isd[low:high]
        #sigma[len(I):] = self.Qsd[low:high]

            #just make some stupid guess as I dont know what Isd is....
            #we set weights to all 1. We should have more weight at the center....
        #sigma[:len(I)] = ones(len(I))
        #sigma[len(I):] = ones(len(I))
        erweight= 1.0 + 5.0*(svel/max(svel))
        erweight = erweight[low:high]
        sigma[:len(I)]=erweight
        sigma[len(I):]=erweight


        # take a guess at center
        Iceng = (max(I)-min(I))/2.0 + min(I)
        Qceng = (max(Q)-min(Q))/2.0 + min(Q)

        self.fitprint('Iceng %f  Qceng %f'%(Iceng,Qceng))

        ang = np.arctan2( Q[fsteps/4] - Qceng, I[fsteps/4] - Iceng )
        self.fitprint(ang)

        if ang >= 0 and ang <= np.pi:
            ang -= np.pi/2
        if ang >= -np.pi and ang < 0:
             ang += np.pi/2



        #self.fitprint(Q[self.fsteps/4]-self.Qceng, I[self.fsteps/4]-self.Iceng
        #self.fitprint(ang

        #parinfo = [{'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.]}]*10
        parinfo=[ {'value':0., 'fixed':0, 'limited':[1,1], 'limits':[0.,0.], 'parname':'NULL'} for i in range(10) ]

        #       Q = p[0]          ;  Q
        #       f0 = p[1]         ;  resonance frequency
        #       aleak = p[2]      ;  amplitude of leakage
        #       ph1 = p[3]        ;  phase shift of leakage
        #       da = p[4]         ;  variation of carrier amplitude
        #       ang1 = p[5]       ;  Rotation angle of data
        #       Igain = p[6]      ;  Gain of I channel
        #       Qgain = p[7]      ;  Gain of Q channel
        #       Ioff = p[8]       ;  Offset of I channel
        #       Qoff = p[9]       ;  Offset of Q channel

        #Q
        parinfo[0]['parname']='Q factor'
        parinfo[0]['value'] = 50000.0
        parinfo[0]['limits'] = [5000.0,1e6]

        #f0
        parinfo[1]['parname']='f0, Res freq'
        parinfo[1]['value'] = mean(idx) 
        parinfo[1]['limits'] = [ min(idx),max(idx)]

        parinfo[2]['parname']='amplitude of leakage'
        parinfo[2]['value'] = 1.0
        parinfo[2]['limits'] = [1e-4,1e2]

        parinfo[3]['parname']='phase shift of leakage'
        parinfo[3]['value'] = 800.0 
        parinfo[3]['limits'] = [1.0,4e4]

        parinfo[4]['parname']='variation of carrier amplitude'
        parinfo[4]['value'] = 500.0 
        parinfo[4]['limits'] = [-5000.0,5000.0]

        parinfo[5]['parname']='Rotation angle of data'
        parinfo[5]['value'] = ang 
        parinfo[5]['limits'] = [-np.pi*1.1,np.pi*1.1]

        parinfo[6]['parname']='Gain of I channel'
        parinfo[6]['value'] = max(I[low:high]) - min(I[low:high]) 
        parinfo[6]['limits'] = [parinfo[6]['value'] - 0.5*parinfo[6]['value']  , parinfo[6]['value'] + 0.5*parinfo[6]['value'] ]

        parinfo[7]['parname']='Gain of Q channel'
        parinfo[7]['value'] = max(Q[low:high]) - min(Q[low:high]) 
        parinfo[7]['limits'] = [parinfo[7]['value'] - 0.5*parinfo[7]['value']  , parinfo[7]['value'] + 0.5*parinfo[6]['value'] ]

        parinfo[8]['parname']='Offset of I channel'
        parinfo[8]['value'] = Iceng
        parinfo[8]['limits'] = [parinfo[8]['value'] - np.abs(0.5*parinfo[8]['value'])  , parinfo[8]['value'] + np.abs(0.5*parinfo[8]['value']) ]

        parinfo[9]['parname']='Offset of Q channel'
        parinfo[9]['value'] = Qceng
        parinfo[9]['limits'] = [parinfo[9]['value'] - np.abs(0.5*parinfo[9]['value'])  , parinfo[9]['value'] + np.abs(0.5*parinfo[9]['value']) ]

        fa = {'x':idx, 'y':s21, 'err':sigma}

        self.fitprint(parinfo)

        #pdb.set_trace()

        # use magfit Q if available        
        #try:
        #        Qguess = np.repeat(self.mopt[0],10) 
        #except:
        Qguess = np.repeat(arange(10)*10000,10)

        chisq=1e50

        if self.fit_plots:
            figure(100);
            clf()
            plot(I,'bx')
            plot(Q,'gx')

        for x in range(20):
            # Fit
            self.fitprint('---------')
            self.fitprint('iteratin: %d'%(x))
            #self.fitprint(parinfo


            Qtry = Qguess[x] + 20000.0*np.random.normal()
            if Qtry < 5000.0:
                Qtry = 5000.0
            parinfo[0]['value'] = Qtry
            parinfo[2]['value'] = 1.1e-4 + np.random.uniform()*90.0
            parinfo[3]['value'] = 1.0 + np.random.uniform()*3e4            
            parinfo[4]['value'] = np.random.uniform()*9000.0 - 4500.0    
            if x > 5:
                parinfo[5]['value'] = np.random.uniform(-1,1)*np.pi
            # fit!
            m = mpfit.mpfit(RESDIFFMP,functkw=fa,parinfo=parinfo,quiet=1)

            #self.fitprint('-------')
            #self.fitprint(m

            popt = m.params    

            fit = RESDIFF(idx,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7],popt[8],popt[9])
            if self.fit_plots:
                figure(100);
                plot(fit[:len(fit)/2],'b')
                plot(fit[len(fit)/2:],'g')
                draw();

            newchisq = m.fnorm            
            if newchisq < chisq:
                chisq = newchisq
                bestpopt = m.params






        try:
            popt = bestpopt
        except:
            popt = m.params

        popt = popt
        Icen = popt[8]
        Qcen = popt[9]

        fit = RESDIFF(idx,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6],popt[7],popt[8],popt[9])

        Ifit=fit[:(len(fit)/2)]
        Qfit=fit[(len(fit)/2):]

        if self.fit_plots:
            figure(12);
            subplot(4,1,3)
            plot(Ifit,'b' )
            plot(Qfit,'g' )
            plot(na.RectToPolar([Ifit,Qfit])[0],'r')

            figure(12);
            subplot(4,1,4)
            plot(na.RectToPolar([Ifit,Qfit])[1],'g')


        return(popt)

        #pdb.set_trace()

        # compute dipdb,Qc,Qi
        radius = abs((popt[6]+popt[7]))/4.0
        diam = (2.0*radius) / (np.sqrt(popt[8]**2 + popt[9]**2) +  radius)
        Qc = popt[0]/diam
        Qi = popt[0]/(1.0-diam)
        dip = 1.0 - 2.0*radius/(np.sqrt(popt[8]**2 + popt[9]**2) +  radius)
        dipdb = 20.0*np.log10(dip)

        # internal power
        power = 10.0**((-self.atten1-35.0)/10.0)
        Pint = 10.0*np.log10((2.0 * self.popt[0]**2/(np.pi * Qc))*power)

        #self.fitprint(popt
        #self.fitprint(radius,diam,Qc,Qi,dip,dipdb

        self.Qm = popt[0]
        self.fm = popt[1]
        self.Qc = Qc
        self.Qi = Qi
        self.dipdb = dipdb
        self.Pint = Pint

        self.fpoints = len(I)
        self.fI = fit[:len(I)]
        self.fQ = fit[len(I):]
        self.ff = self.freq[low:high]







def RESDIFF(x,Q,f0,aleak,ph1,da,ang1,Igain,Qgain,Ioff,Qoff):
#       Q = p[0]          ;  Q
#       f0 = p[1]         ;  resonance frequency
#       aleak = p[2]      ;  amplitude of leakage
#       ph1 = p[3]        ;  phase shift of leakage
#       da = p[4]         ;  variation of carrier amplitude
#       ang1 = p[5]       ;  Rotation angle of data
#       Igain = p[6]      ;  Gain of I channel
#       Qgain = p[7]      ;  Gain of Q channel
#       Ioff = p[8]       ;  Offset of I channel
#       Qoff = p[9]       ;  Offset of Q channel

    l = len(x)
    dx = (x - f0) / f0

    # resonance dip function
    s21a = (np.vectorize(complex)(0,2.0*Q*dx)) / (complex(1,0) + np.vectorize(complex)(0,2.0*Q*dx))
    s21a = s21a - complex(.5,0)
    
    if False:        
        figure(13);
        clf()
        subplot(3,1,1);
        plot(np.abs(s21a),'r')
        plot(np.real(s21a),'b')
        plot(np.imag(s21a),'g')

    s21b = np.vectorize(complex)(da*dx,0) + s21a + aleak*np.vectorize(complex)(1.0-np.cos(dx*ph1),-np.sin(dx*ph1))


    if False:
        figure(13);subplot(3,1,2)
        plot(abs(s21b))

    # scale and rotate
    Ix1 = s21b.real*Igain
    Qx1 = s21b.imag*Qgain
    nI1 = Ix1*np.cos(ang1) + Qx1*np.sin(ang1)
    nQ1 = -Ix1*np.sin(ang1) + Qx1*np.cos(ang1)

    #scale and offset
    nI1 = nI1 + Ioff
    nQ1 = nQ1 + Qoff

    s21 = np.zeros(l*2)
    s21[:l] = nI1
    s21[l:] = nQ1

    if False:
        figure(13);subplot(3,1,3)
        plot(abs(s21))

    return s21

def RESDIFFMP(p, fjac=None, x=None, y=None, err=None):

    Q = p[0]          #  Q
    f0 = p[1]         #  resonance frequency
    aleak = p[2]      #  amplitude of leakage
    ph1 = p[3]        #  phase shift of leakage
    da = p[4]         #  variation of carrier amplitude
    ang1 = p[5]       #  Rotation angle of data
    Igain = p[6]      #  Gain of I channel
    Qgain = p[7]      #  Gain of Q channel
    Ioff = p[8]       #  Offset of I channel
    Qoff = p[9]       #  Offset of Q channel

    l = len(x)
    dx = (x - f0) / f0

    # resonance dip function
    s21a = (np.vectorize(complex)(0,2.0*Q*dx)) / (complex(1,0) + np.vectorize(complex)(0,2.0*Q*dx))
    s21a = s21a - complex(.5,0)
    s21b = np.vectorize(complex)(da*dx,0) + s21a + aleak*np.vectorize(complex)(1.0-np.cos(dx*ph1),-np.sin(dx*ph1))

    # scale and rotate
    Ix1 = s21b.real*Igain
    Qx1 = s21b.imag*Qgain
    nI1 = Ix1*np.cos(ang1) + Qx1*np.sin(ang1)
    nQ1 = -Ix1*np.sin(ang1) + Qx1*np.cos(ang1)

    #scale and offset
    nI1 = nI1 + Ioff
    nQ1 = nQ1 + Qoff

    s21 = np.zeros(l*2)
    s21[:l] = nI1
    s21[l:] = nQ1

    status=0
    return [status, (y-s21)/err]



def phaseFunc(x,Qf,fr,theta0,sgn):

    ###########################################################################
    ### PHASE FITTING!!!!!!
    # Fitting function: phase(x) = theta0 - 2*atan(2*Q* (1-x/fr))
    #     param(1) = Q factor
    #     param(2) = fr
    #     param(3) = theta0
    # Reference: Gao's thesis Equation E.11 (Also: Petersan, P. J. and Anlage, S.
    # M. 1998, J. Appl. Phys., 84, 3392 250)


    #!! changed sign...
    phz = sgn*(theta0 - 2*arctan(2*Qf* (1-x/fr)));


    return(phz)    
        

def residPhase(p, fjac=None, x=None, y=None, err=None):        

    #residuals_phase = @(param) (phase_func(param) - phase)./phase; 
    #normalize residual for data size
    diff = y - phaseFunc(x,p[0],p[1],p[2],p[3]);
    status=0;
    return([status, diff/err])


#
# Nino, Gao lorenz function
#
def lorentzFunc(x,A):
    lrnz0= A[0]+A[1]*(x-A[4])
    lrnz1=  (A[2]+A[3]*(x-A[4]))  /  (1+    4*(A[5]**2) * ( (x-A[4])/A[4] )**2   )  ;
    lrnz=lrnz0+lrnz1
    return(lrnz)
    

def residLorentz(p, fjac=None, x=None, y=None, err=None):  

    lrnz=lorentzFunc(x,p)
    
    diff = y-lrnz
    status=0;
    return([status, diff/err])
    
# Skewed circle fitting # added by cecil

# Skewed circle function
def SkewcircleFunc(x,A):
    j=complex(0,1)
    sc1= A[0]/A[1] - 2*j*A[0]*A[3]/A[2]
    sc2= 1+ 2*j*A[0]*(x-A[2])/A[2]
    #skewcircle = A[4]*ones(len(x)) + 20*log10(abs(1-(sc1/sc2)))
    #skewcircle = A[4] + 20*log10(abs(1-(sc1/sc2)))
    skewcircle = 20*log10(abs(1-(sc1/sc2)))    

    return(skewcircle)

# Skewed circle residuals
def residSkewcircle(p, fjac=None, x=None, y=None, err=None):  

    skewcircle=SkewcircleFunc(x,p)
    
    diff = y-skewcircle
    status=0;
    return([status, diff/err])    
    


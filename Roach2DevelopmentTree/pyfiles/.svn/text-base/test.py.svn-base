res=MKID_list[0].reslist[2]

na.setSweepResonator(res)


trnum=12

na.iqdata=res.iqnoise[trnum]
fbase=res.srcfreq[trnum]
na.frequency_list = [fbase]
na.fftBinsFreqs()


na.fftsynctime=res.fftsynctime[trnum]

frindx=min(where(na.sweepres.lorentz_fr<=na.sweepres.freqs)[0])

pp=na.RectToPolar([na.sweepres.trot_xf,na.sweepres.trot_yf ])

figure(103)

clf()
polar(pp[1],pp[0])

polar(pp[1][frindx],pp[0][frindx],'o')

iqp=na.RectToPolar(na.sweepres.iqdata)
polar(iqp[1],iqp[0])


ts = na.extractTimeSeries(na.frequency_list[0]);

figure(212)
clf()
plot(ts[1])

figure(103)
#angle of ts is 0, set by software. add angle of fres to ts angle.
#put at 180 deg off the res for now
#
#ts[1]=ts[1] + pp[1][frindx] + pi
#ts[1]=ts[1] +  pi

#now cloud is at center-radius, where center on -x axis.
#center is this:
xc=na.sweepres.cir_xc
yc=na.sweepres.cir_yc
z=sqrt(xc**2 + yc**2)
print z
r=na.sweepres.cir_R



#find angle from origin to center.
sweep_cir_ang= numpy.angle(complex(xc,yc))
#get angle from origin to res freq.


nindx=max(where(fbase<=(na.sweepres.carrierfreq- na.sweepres.freqs))[0])

sweep_res_ang = numpy.angle(
	complex(
	    na.sweepres.iqdata[0][nindx],
	    na.sweepres.iqdata[1][nindx]))


sweep_delta_ang=sweep_res_ang - sweep_cir_ang


polar(sweep_cir_ang,z,'x')
polar(pp[1][nindx],pp[0][nindx],'o')


polar(ts[1],ts[0],'gx')
#get res_ang for noise data.
noise_res_ang = median(ts[1])

#calc what the circle angle should be
noise_cir_ang = noise_res_ang -sweep_delta_ang


polar(noise_cir_ang,z,'+')





#calc the center of noise circle 

xc_noise=z * cos(noise_cir_ang)
yc_noise=z * sin(noise_cir_ang)


#
#draw a circle where noise cloud should be on
#
phz=(numpy.pi*2/360.0)*arange(0.0,360.0,10.0)
ncirx=xc_noise + r*cos(phz)
nciry=yc_noise + r*sin(phz)
ncirp=na.RectToPolar([ncirx,nciry])
polar(ncirp[1],ncirp[0])


ts_r=na.PolarToRect(ts);


noise_xf = (xc_noise-ts_r[0])*cos(noise_cir_ang) + (yc_noise-ts_r[1])*sin(noise_cir_ang);
noise_yf = -(xc_noise-ts_r[0])*sin(noise_cir_ang) +  (yc_noise-ts_r[1])*cos(noise_cir_ang);



#gainadj=(z-r) / mean(ts[0])

#print 'gain adj %4.4fdB, %4.4f'%(20.0*log10(gainadj),gainadj)


#translate the data, w/ angle at 180deg. 
#ts_r[0] = ts_r[0] - mean(ts_r[0]) +r
#ts_r[0] = ts_r[0] + z 

ts2=na.RectToPolar([noise_xf, noise_yf])

#now add the amgle
#ts2[1]=ts2[1] + pp[1][frindx]

polar(ts2[1],ts2[0],'rx')



#at.report()

figure(200)
clf()

plot(na.sweepres.iqdata[0], na.sweepres.iqdata[1],'x')
plot(0,0,'o')

plot(na.sweepres.trot_xf,na.sweepres.trot_yf,'gx')
plot(noise_xf, noise_yf,'rx')



#MKID_list[0].reslist[0].report()

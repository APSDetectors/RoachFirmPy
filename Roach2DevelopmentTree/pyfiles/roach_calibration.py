# preferred tone power at resonator dbm
tone_power_at_resonator_dbm = -85.0



#hard codeed, watts output for full scale sinewave. 
dac_watts_sinewave = 0.00198
#max amp 0p in counts outptu from dac
dac_max_counts_0p = 32766

#12 buit adc 0-p
adc_max_counts_0p=2046
#sine wave fill scale, W
adc_watts_sinewave = 0.00427

#mixer input desired powerin dbm
in_mixer_desired_power_dbm = 1.0




#atten in db if both output attens are set to 0dB atenuation
# negative atten means ATTENUATION. Positive means GAIN
if_board_out_fudge = 2
if_board_minimum_outatten = -1.0 -3.0 -1.0 -0.5 - 5.5 - 3.0 - 3.0 -1.5 + if_board_out_fudge 

#gain of inut amp+atten u28 at 0db. Gein from input to input of mixer on ifboard.
if_board_rfin_2_mixerin = 15.0-3.0


if_board_attenu6_minatt = 0.0
if_board_attenu6_maxatt = -31.0
if_board_attenu6_attstep =0.5 

if_board_attenu7_minatt = 0.0
if_board_attenu7_maxatt = -31.0
if_board_attenu7_attstep =0.5 


#if board input. has GAIN, this is gain in db from rfinout, 
#thru mixer to adc input. att28 at 0db atten.
if_board_minimum_inatten = 15.0-3.0-5.5+20.0-0.5-1.0-1.0-1.0


if_board_attenu28_minatt = 0.0
if_board_attenu28_maxatt = -31.0
if_board_attenu28_attstep =0.5 


# Cryostat gains
#atten before resonators
cryo_atten_db = -30
#hemt after resonators
cryo_hemt_gain = 35
#nominal resonator attenatin
cryo_res_nom_atten = -20

#
# FFT Gain. If fft coef is 0.5 for a single sinetone, then what is rms in counts 
#of that sinewave tin ADC couts. Units is  1/counts. The fft bins are in RMS, proportinal
# to voltage. it is not  power spectrum
# 2.5 is a fidge facture from measuring the fft gain. done know why...
roach_fft_rms_per_adccounts= 2.5/adc_max_counts_0p



#
# Phi-0 per radian. roach return radisnas. Hpw many rotations of the 
#SQUID coresponds to 1 RAD of change in res signal
#
phi_naught_per_radian = 1.0








############################################################################################]
#
# All values below calc'ed based on values above.
#
############################################################################################
 

#all based on dac_watts_sinewave
dac_dbm_sinewave = 10*log10(dac_watts_sinewave/0.001)
dac_rmsv_sinewave = sqrt(dac_watts_sinewave*50)
dac_v0p_sinewave = dac_rmsv_sinewave*sqrt(2.0)
dac_vpp_sinewave = dac_v0p_sinewave*2.0


#all based on adc_watts_sinewave
adc_dbm_sinewave = 10*log10(adc_watts_sinewave/0.001)
adc_rmsv_sinewave = sqrt(adc_watts_sinewave*50)
adc_v0p_sinewave = adc_rmsv_sinewave*sqrt(2.0)
adc_vpp_sinewave = adc_v0p_sinewave*2.0
adc_rmscounts_sinewave = adc_max_counts_0p *sqrt(2.0)/2.0








############################################################################################]
#
# Functions for calc'ing calibration values , all for DAC
#
############################################################################################


#
# given sine amp in dac counts, and u6,u7 atten in db, calc dBm power out of IF board RF OUT
#

def calcRfPowerOutputDBm(
    sineamp_counts, 
    atu6_db,
    atu7_db):

    sinevolts_0p = dac_v0p_sinewave*(float(sineamp_counts)/float(dac_max_counts_0p))
    sinevolts_rms = sinevolts_0p/sqrt(2.0)
    sinewatts = (sinevolts_rms*sinevolts_rms)/50.0
    sinedbm = 10*log10(sinewatts/0.001)
    if_atten = if_board_minimum_outatten + (-1.0)*abs(atu6_db) + (-1.0)*abs(atu7_db)
    sineout_dbm = sinedbm + if_atten
    return(sineout_dbm)


def calcSineampAttensFromRfPower(num_tones,desired_power):
    if num_tones==0: num_tones=1

    sineamp_counts = dac_max_counts_0p/num_tones
    max_ifout_dbm = calcRfPowerOutputDBm(sineamp_counts,0,0)
    if (desired_power<=max_ifout_dbm):
        #we work with gains, atten shoudl be <0
        atten = desired_power - max_ifout_dbm
        atu6 = 0.0
        atu7 = 0.0
        atu28 = 0.0
        if atten<if_board_attenu6_maxatt:
            atu6 = if_board_attenu6_maxatt
            atu7 = (atten - if_board_attenu6_maxatt)
            if atu7<if_board_attenu7_maxatt:
                print "calcSineampAttensFromRfPower: Error too much attenuation"
                return(None)
            
            return( (sineamp_counts, atu6, atu7,atu28) )
        else:
            atu6 = atten
            return( (sineamp_counts, atu6, atu7,atu28) )
    else:
        print "calcSineampAttensFromRfPower:  Cannot make that much power"
        return(None)


def calcResPowerDbm(
    sineamp_counts, 
    atu6_db,
    atu7_db):

    rfpwr = calcRfPowerOutputDBm(sineamp_counts,atu6_db,atu7_db)
    respwr = cryo_atten_db + rfpwr
    return(respwr)

def calcSineampAttensFromResPower(num_tones,desired_power):
    rfpwr = desired_power - cryo_atten_db
    return( calcSineampAttensFromRfPower(num_tones,rfpwr ))

##################################################################################################3
#
# Functions for calc'ing power input to digitizers
#
###################################################################################################




##
# convert fftbin, scaler, or numpy array, to scalar dbm, or array of dbm
#
def calcSignalRfInputPowerAtIfboard(fftbinval,atu28_db):
    rms_counts = fftbinval / roach_fft_rms_per_adccounts  
    volts_rms = adc_v0p_sinewave * (rms_counts) / (adc_rmscounts_sinewave)
    watts = (volts_rms*volts_rms)/50.0
    dbm = 10*log10(watts/0.001)
    if_atten =if_board_minimum_inatten  + (-1.0)*abs(atu28_db) 
    in_dbm = dbm - if_atten
    return(in_dbm)




def calcSignalRfInputPowerAtMixer(fftbinval,atu28_db):
    rfdbm = calcSignalRfInputPowerAtIfboard(fftbinval,atu28_db)
    rfatmixerindbm = if_board_rfin_2_mixerin + rfdbm
    return(rfatmixerindbm)


def calcSignalRfInputPowerAtHemt(fftbinval,atu28_db):
    rfdbm = calcSignalRfInputPowerAtIfboard(fftbinval,atu28_db)
    rfhemt = rfdbm - cryo_hemt_gain     
    return(rfhemt)

    



def calcWattsFromDbm(dbm):
    watts = 0.001 * pow(10.0,(dbm/10.0))
    return(watts)

def calcDbmFromWatts(watts):
    dbm = 10*log10(watts/0.001)
    return(dbm)

#
# max power we can oput on a resonator
#

cryo_max_res_power_dbm = calcResPowerDbm(dac_max_counts_0p,0,0)





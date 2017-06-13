# preferred tone power at resonator dbm
tone_power_at_resonator_dbm = -85.0



#hard codeed, watts output for full scale sinewave. 
dac_watts_sinewave = 0.00198
#max amp 0p in counts outptu from dac
dac_max_counts_0p = 32766



#atten in db if both output attens are set to 0dB atenuation
# negative atten means ATTENUATION. Positive means GAIN
if_board_mininum_outatten = -19.0

if_board_attenu6_minatt = 0.0
if_board_attenu6_maxatt = -31.0
if_board_attenu6_attstep =0.5 

if_board_attenu7_minatt = 0.0
if_board_attenu7_maxatt = -31.0
if_board_attenu7_attstep =0.5 


#if board input. has GAIN
if_board_mininum_inatten = 20.0

if_board_attenu28_minatt = 0.0
if_board_attenu28_maxatt = -31.0
if_board_attenu28_attstep =0.5 

# Cryostat gains
#atten before resonators
cryo_atten_db = -30
#hemt after resonators
cryo_hemt_gain = 35
#nominal resonator attenatin
cryo_res_nom_atten = 20



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


############################################################################################]
#
# Functions for calc'ing calibration values 
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
    if_atten = if_board_mininum_outatten + (-1.0)*abs(atu6_db) + (-1.0)*abs(atu7_db)
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







#
# max power we can oput on a resonator
#

cryo_max_res_power_dbm = calcResPowerDbm(dac_max_counts_0p,0,0)





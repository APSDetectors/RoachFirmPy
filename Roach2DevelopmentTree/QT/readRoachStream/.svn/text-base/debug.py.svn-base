roach2.when_callback=range(10000)
roach2.callback_counter = 0
roach2.dram_test_nbuffers=2


sig3=list('ABCDEFGHIJKLMNOP')

#convert the chars to ascii values in the list
sig2=[]
for ss in sig3:
    ss=ord(ss)
    sig2.append(ss)

#make it longer, 16*len(sig3) will be 256 items, or 128 256 bit workds
sig2=numpy.array(sig2*16*roach2.dram_test_nbuffers)

#make AA,BB,CC etc. into a 16 bit workd
sig = sig2*256
sig = sig + sig2

data =  roach2.convertToBinary128_2(sig,7)

dramname="DRAM_LUT"



(bindata , bindata_b) = roach2.convert128To256(data)

control_reg='%s_control'%dramname
lutsize_reg = '%s_LUTSize'%dramname
offs_addr_reg = '%s_offsAddr'%dramname
buffmem0 = '%s_drambuff128_0'%dramname
buffmem1 = '%s_drambuff128_1'%dramname

startdac_bit = 2
sync_bit =3
load_addr_bit = 0
write_bit = 1
rst_dram_bit = 4


datalen=len(bindata)
datalen_word=datalen/16

print 'nbytes %d lutsizewords %d'%(datalen, datalen_word)
#
#set address speeds of bram and dram
#
control = (roach2.rd_toggle<<7) + (roach2.wr_toggle<<5);

roach2.write_int(control_reg, control);

#
#pulse sync in bit
#
control = control + (1<<sync_bit)
roach2.write_int(control_reg, control)

control = control - (1<<sync_bit)
roach2.write_int(control_reg, control);



offaddr = 0
dataptr = 0

#address size iof te buff bram. it is 128 addresses, at 288 bits, or 16 bytes per address
buffsize_word = 128
#the dram addr incs by 8 for each 128bit word (or 144 bit word)
addrinc = buffsize_word*8
#bufsize in bytes
buffsize = buffsize_word*16

#lut size must be datalen_word, or the number of 288 size workds in mem.
# the 8 is because the dram addr must inc by 8, as lower 3 bits are not used.
#we add fudge factor because we want the mem to count farther when we are wrting it
#or else the state machine may overwrite the 1st word... fudge of 16 words
fudge = 8*16;
lutsize = 8*datalen_word + fudge
roach2.write_int(lutsize_reg, lutsize);
while dataptr<datalen:
    #
    #set control to all bits 0 except the rd and wer toggles.
    #
    control = (roach2.rd_toggle<<7) + (roach2.wr_toggle<<5);
    roach2.write_int(control_reg, control)
    #
    #pulse sync in bit
    #
    control = control + (1<<sync_bit)
    roach2.write_int(control_reg, control)

    control = control - (1<<sync_bit)
    roach2.write_int(control_reg, control);

    #get 128 * 16 bytes of data for on bram size of data.
    datawr=bindata[(dataptr):(dataptr+buffsize)]
    datawr_b=bindata_b[(dataptr):(dataptr+buffsize)]


    #
    # write dram start addr for this bloc and load the address
    #

    roach2.write_int(offs_addr_reg, offaddr);

    control =  control  + (1<<load_addr_bit)
    roach2.write_int(control_reg, control);

    control = control  - (1<<load_addr_bit)
    roach2.write_int(control_reg, control);


    #
    # write data to brams
    #
    roach2.write(buffmem0,datawr);
    roach2.write(buffmem1,datawr_b)
    print "write %d bytes: %s"%(len(datawr),datawr[:64])

    #################################################################################
    trigScope(0,7)
    print '################################'
    print 'DRAM_LUT_offsAddr = %d'%( roach2.read_int('DRAM_LUT_offsAddr') )
    #################################################################################

    #
    #put dram/bram in write to dram mode
    # katCallBack()
    control =control + (1<<write_bit)
    roach2.write_int(control_reg, control);


    #
    # start dac which will do the block write to dram
    #
    control = control + (1<<startdac_bit)
    roach2.write_int(control_reg, control);

    #wait for dram to write
    time.sleep(0.01)

    #
    # turn off start sssdac to stop sm.turn off write mode
    #
    control = control - ( (1<<startdac_bit)  +  (1<<write_bit)  )
    roach2.write_int(control_reg, control);

    #
    #inc mem ptrs to get next block of data, and next block address in dram
    #

    #inc ptr into the raw data to send to next bram size block
    dataptr= dataptr + buffsize
    #inc the dram mem
    offaddr = offaddr + addrinc




#lut size must be datalen_word, or the number of 288 size workds in mem.
# the 8 is because the dram addr must inc by 8, as lower 3 bits are not used.
#
lutsize = 8*datalen_word
roach2.write_int(lutsize_reg, lutsize);
#
#set control to all bits 0 except the rd and wer toggles.
#
control = (roach2.rd_toggle<<7) + (roach2.wr_toggle<<5);
roach2.write_int(control_reg, control)
#

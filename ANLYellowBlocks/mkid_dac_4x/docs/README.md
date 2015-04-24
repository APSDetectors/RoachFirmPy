This pcore was created by starting a new ISE project with one .v file.
The file is the pcore verilog file for the dac mkid 4x interface.
The design is based on a design from Santa Barbara, but is updated
to run on a V6 chip, using MMCM rather than DCM.
Tp assure the design will work, it can be synthesized, but not fully
built into a bit file, as no consrainsts are present. To get the correct 
settings for MMCM, the wizard can be used (Project->New source->Core Gen
IP->clock wizard)
Alternativly, the MMCM template can be fetched from 
Edit->language templates->verilog

By synthesizing, all syntax errors can be found, and an RTL schematic
can be generated.
This was done in ISE 14.6

The ods file is an open office (libre office, start in linux with
soffice), of the pinouts. I checked that the dac nets on the FPGA design
matched proper FPGA pins, ZDOK pins on the Roach 2 board, and ZDOK pins
on the DAC board.

The only srouce code that is needed is
dac_mkid_4x_interface.v




To install:
In this dir,  
mlib_dev/xps_base/XPS_ROACH2_base/pcore

cp -r
GitRepo/RoachFirmPy/ANLYellowBlocks/mkid_dac_4x/pcores/dac_mkid_4x_interface_v2_00_a\
mlib_dev/xps_base/XPS_ROACH2_base/pcores/.




In the mlib_dev/xps_library

cp
GitRepo/RoachFirmPy/ANLYellowBlocks/mkid_dac_4x/xps_library/adc_mkid_4x_r2_mask.m\
mlib_devel/xps_library/.

cp -r
GitRepo/RoachFirmPy/ANLYellowBlocks/mkid_dac_4x/xps_library/@xps_dac_mkid_4x_r2\
mlib_devel/xps_library/.






To make a yellow block appear in your Simulink Library Browser, 
cp xps_libaray.mdl xps_libaraymdl.SAVE
chmod +w xps_libary.mdl


open xps_libary.mdl, and unlock libaray.
Open in a 2nd window add_to_xps_librarymdl.mdl
Copy and paste the new block into your xps_libaray.mdl file. Lock the
library.
chmod -w xps_library.mdl



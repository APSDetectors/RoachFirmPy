# RoachFirmPy


**This UNSUPPORTED now!!** 

Argonne Roach FW and Python development for MKID readout


This code is for testing ddr ram for streaming ADC converters.
* The design has a ddr ram block that streams several pipes of 16 bit 
data to an output, for DACs.
* The ddr is loaded from py software through a bram that is written several times.
* Python controls the system; all python is in pyfiles dir.

**testdram.py**
* This is the top level py file. It loads in necessry py files, connects to roach, programs data into dram, then starts streaming dram. 

**katcpNc.py** 
* katcpNc.py is a katcp front end that looks like corr.
It is a fairly small code and uses netcat, or nc, as the network connection.
Two linux pipes are needed: one so python can write to netcat, and one
so python can read from netcat.
* The idea is that nc connects to the roach board borph server, and gets stdin
and stdout from linux fifos on the file system.
* Python then writes and reads text streams from these fifos to write to roach.
The fifos must preexist on the file system, with mkfifo /myfifoname
* This nice little katpcpNc as a sendbof command that will send a bof file
from local directory, and prog the roach2. It is just like roach1. A nc
process is started in the background to do this.
* Why use a custom katcp py wrapper?
 1. Because corr cannot write the dram on Roach2
 2. Because corr cannot send the bof file.
 
**Roachscope**
 * Roachscope is a block that has a snap block that can grab data into BRAM.
 * katcpNc has functions to treat this like a scope, with several imputs and 
triggers muxed in. It is like a poor-man's chip scope.
There is a scope trigger and scope plot data.

**QT**
* This QT code is a C++ QT4.8 app that is a C++ GUI front end to python and
roach. The idea is that it is easy to make a C++ QT gui , but a pain to 
make a python QT gui (you have to type everything...)

* The C program starts up a python interpereter as a separate process, with stdin
from a pipe. QT writes py commands to a pipe. There is a pyPipeServer class
that allows the C program to get data from python, sent over a pipe to the 
QT program. The python interpreter stdout is just a terminal. Sending data
from python to QT is a file write to a linux fifo from pyPipeServer.

* The QT program is useful for debugging things and relieves the developer from
typing all the time. Also, there is a nice interface to RoachScope.

**Bugs**
* One bug in the DDR streaming:
When reading out the DDR, the output mux can be on the wrong output, that is,
lo 144 bits or hi 144 bits, and the data gets reversed. Restarting streaming
fixes this. This should be tied to rdvalid. Next version will fix this.

Tim Madden    
Argonne National Laboratory  

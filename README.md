# RoachFirmPy
Argonne Roach FW and Python development for MKID readout

This code is for testing ddr ram for streaming ADC converters

The design has a ddr ram block that streams several pipes of
16 bit data to an output, for DACs.

The ddr is loaded from py software through a bram that is written
several times.

python controls the system

all python is in pyfiles dir.

katcpNc.py is a katcp front end that looks like corr.
It is a fairly small code and uses netcat, or nc, as te network connection.
Two linux pipes are needed: one so python can write to netcat, and one
so python can read form netcat.

The idea is that nc connects to the roach board borph server, and gets stdin
and stdout from linux fifos on the file suystem

Python then writes and reads text streams from theses fifos to write to roach.
The fifos must preexist on the file sustem, with mkfifo /myfifoname

Why use a custom katcp py wrapper?
1. Because corr cannot write the dram on Roach 2
2. Because corr cannot send the bof file.

This nice little katpcpNc as a sendbof command that will send a bof file
from local directory, and prog the roach 2. It is just like roach 1. A nc
process is started in the background to do this.

The top level py file is

testdram.py

This loads in necessry py files, connects to roach, programs data into dram.
then starts streaming dram. 

Roachscope:
Roachscope is a block that has a snap block that can grab data into BRAM.

katcpNc has functions to treat this like a scope, with several imputs and 
triggers muxed in. It is like a poor-man's chip scope.
There is a scope trigger and scope plot data.


One bug in the DDR streaming:
When reading out the DDR, the output mux can be on the wrong output, that is,
lo 144 bits or hi 144 bits, and ghe data gets reversed. restarting streaming
fixes this. this should be tied to rdvalid. Next version will fix this.

Tim Madden
Argonne Lab


QT:
This QT code is a C++ QT4.8 app that is a C++ GUI front end to python and
roach. The idea is that it is easy to make a C++ QT gui , but a pain to 
make a python QT gui (you have to type everything...)

The C program starts up a py interpereter as a separate process, wth stdin
from a pipe. QT writes py commands to a pipe. There is a piPipeServer class
that allows the C program to get data from pythin, sent over a pipe to the 
QT program. The pythin interpreter stdout is just a terminal. Sending data
from pythign to QT is a file write to a linux fifo from pyPipeServer.

The QT program is usefull for debugging things and relieves the developer from
typing all the time. also, there is a nice interface to RoachScope.





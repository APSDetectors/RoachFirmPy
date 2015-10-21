#!/APSshare/epd/rh6-x86_64/bin/ipython -pylab

import os
import sys
import socket

os.chdir('/home/oxygen26/TMADDEN/ROACH/projcts')

execfile('natAnalGui.py')

num= int(sys.argv[1])

print "\n\n------------HOST %s    FileNum %d--------------"%(socket.gethostname(),num)

#time.sleep(10)


try:
   fitOneResonatorFile(num)
except:
   print "\n\nERROR!!!   HOST %s    FileNum %d\n\n"%(socket.gethostname(),num)

print "\n\n------------HOST %s    FileNum %d----EXITING-----------"%(socket.gethostname(),num)

exit()
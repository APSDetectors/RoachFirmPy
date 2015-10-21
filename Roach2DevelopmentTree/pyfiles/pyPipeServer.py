


class pyPipeServer:

    def __init__(self):

        #names reversed.. in out ref to the client not server
        self.pyoutname = '/local/pyfifoin'


        self.pyout=0

    def openPipes(self):

        self.pyout= open(self.pyoutname,'w')

    def closePipes(self):

        self.pyout.close()

    def getInt(self,var):
        self.pyout.write('getInt\n')
        self.pyout.write('%d\n'%(var))
        self.pyout.write('!getInt\n')

        self.pyout.flush()

    def getByteArray(self,var):
        self.pyout.write('getByteArray\n')
        self.pyout.write('%d\n'%(len(var)))
        self.pyout.write(var)
        self.pyout.write('!getByteArray\n')

        self.pyout.flush()



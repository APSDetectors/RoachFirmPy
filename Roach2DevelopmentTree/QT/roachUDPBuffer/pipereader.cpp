#include "pipereader.h"
#include "stdio.h"
#include "string.h"
pipeReader::pipeReader(QString fname,int rs,packetFifo *f):QObject(0)
{


    //!!fp=fopen(fname.toStdString().c_str(),"rb");
    readsize=rs;
   fifo=f;
    is_write_fifo=false;

}

void pipeReader::readPipe(void)
{
    unsigned char *data;
    int rsize;
    while(true)
    {

        data = fifo->getNewArray();
        if (data)
        {

                rsize = fread(data,1,readsize,stdin);
                if (is_write_fifo)
                    fifo->write(rsize);
        }


    }
}


void pipeReader::isWriteFifo(bool i)
{
    is_write_fifo=i;
}

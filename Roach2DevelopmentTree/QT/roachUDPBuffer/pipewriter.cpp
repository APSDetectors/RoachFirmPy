#include "pipewriter.h"

pipewriter::pipewriter(QString fname,int rs,packetFifo *f):QObject(0)
{

   //!! fp=fopen(fname.toAscii().data(),"wb");
    readsize=rs;
   fifo=f;
}


void pipewriter::writePipe(void)
{
    int length;
    unsigned char *data;
    int wsize;

    while(true)
    {
        usleep(1);
        while (!fifo->isEmpty())
        {


            data = fifo->read(&length);
            if (data)
            {
                   wsize= fwrite(data,1,length,stdout);
            }
        }

    }
}

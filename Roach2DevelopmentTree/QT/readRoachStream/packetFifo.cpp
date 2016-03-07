#include "packetFifo.h"

packetFifo::packetFifo(QObject *parent) :
    QObject(parent)

{
    array_fifo=0;

    fifo_length=0;
    array_max_length=0;
    max_fifo_len=0;
    max_fifo_len2=0;
     is_empty=true;
     is_full=true;


     //read pointer w/ extra bit
    read_counter=0;
     // actual read piounter into the fifo.
    read_location=0;

     //write counter w/ extra buits
     write_counter=0;
     //write ponter into the array
     write_location=0;


}


int packetFifo::getMaxArrayLen(void)
{
    return(array_max_length);
}


void packetFifo::write(int length)
{

    if (!is_full)
    {


        if (length<array_fifo[write_location].max_datalen)
            array_fifo[write_location].datalen=length;
        else
            array_fifo[write_location].datalen=
                    array_fifo[write_location].max_datalen;

        write_counter = (write_counter+1)% max_fifo_len2;
        write_location= (write_location+1)%max_fifo_len;

        calcEmptyFull();


    }



}

unsigned char* packetFifo::getNewArray(void)
{
    unsigned char *data=0;
    if (!is_full)
    {
        data = array_fifo[write_location].data;


    }

    return(data);

}


void packetFifo::calcEmptyFull(void)
{
    fifo_length=write_counter-read_counter;
    if (fifo_length<0)
        fifo_length+=max_fifo_len;


    if (write_counter==read_counter)
    {
        is_empty=true;
        is_full = false;
    }
    else
    {
        is_empty=false;
        if (write_location==read_location)
            is_full=true;
    }

}

unsigned char* packetFifo::read(int *length)
{
    unsigned char *data=0;
    if (!is_empty)
    {
        data = array_fifo[read_location].data;
        *length=array_fifo[read_location].datalen;
        read_counter = (read_counter+1)% max_fifo_len2;
        read_location= (read_location+1)%max_fifo_len;

        calcEmptyFull();


    }

    return(data);

}

void  packetFifo::fillFifo(int flen_pwrtwo, int arraylen)
{

    int flen= (1<<flen_pwrtwo);

    array_fifo=new charArrayInt[flen];
    for (int k=0;k<flen;k++)
    {
        array_fifo[k].data= new unsigned char[arraylen];
        array_fifo[k].datalen=0;
        array_fifo[k].max_datalen=arraylen;
    }

   fifo_length=0;
   array_max_length=arraylen;

   max_fifo_len=flen;
   max_fifo_len2=2*flen;
    is_empty=true;
    is_full=false;



    //read pointer w/ extra bit
   read_counter=0;
    // actual read piounter into the fifo.
   read_location=0;

    //write counter w/ extra buits
     write_counter=0;
    //write ponter into the array
     write_location=0;

}

void  packetFifo::emptyFifo()
{

    for (int k=0;k<max_fifo_len;k++)
    {
        delete array_fifo[k].data;

    }

    delete[] array_fifo;

   fifo_length=0;
   array_max_length=0;
   max_fifo_len=0;
   max_fifo_len2=0;
    is_empty=true;
    is_full=true;



    //read pointer w/ extra bit
   read_counter=0;
    // actual read piounter into the fifo.
   read_location=0;

    //write counter w/ extra buits
     write_counter=0;
    //write ponter into the array
     write_location=0;
}


void packetFifo::clear(void)
{


    //read pointer w/ extra bit
   read_counter=0;
    // actual read piounter into the fifo.
   read_location=0;

    //write counter w/ extra buits
     write_counter=0;
    //write ponter into the array
     write_location=0;

     calcEmptyFull();
}


int packetFifo::length(void)
{

    return(fifo_length);
}


quint32 packetFifo::flipEndian(quint32 in)
{
    quint32 temp;
    quint32 out;

    temp = in;

    out = (temp&0xff) << 24;
    temp = temp >> 8;

    out = out  | ((temp&0xff) << 16);
    temp = temp >> 8;

    out = out  | ((temp&0xff) << 8);
    temp = temp >> 8;

    out = out  | ((temp&0xff));

    return(out);

}


bool packetFifo::isEmpty(void)
{
    return(is_empty);
}


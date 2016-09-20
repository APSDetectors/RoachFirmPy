#include "packetParse.h"
#include <QStringList>
#include <QIODevice>
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "error.h"
#include "errno.h"
#include "string.h"
packetParse::packetParse(
        packetFifo *data_fifo_,
        QObject *parent) :
    QObject(parent),
     raw_data_a(),
   raw_data_b(),
   queue_mutex(),
   lastdatagram(),
   datagram(),
   packet_counters(),
   baddatagram(),
   staterecord(),
   data_a(),
   data_b(),
   pipename("packetParse.pipe")

{

    pipefile=0;
     is_write_pipe=false;



    data_fifo=data_fifo_;

is_dump_fifos=false;



  statereclength=1024;
    statereccount = 0;

    twoint maddog;

    //will create a new obj on append... I think
    for (statereccount=0;statereccount<statereclength;statereccount++)
        staterecord.append( maddog );

statereccount=0;
  resetCounters();

   //max size of datagram
   datagram.resize(65536);
   lastdatagram.resize(65536);

}




void packetParse::writeToPipe(bool is_write)
{
    if (is_write)
    {
        if (!is_write_pipe)
        {
            pipefile=new QFile(pipename);
            pipefile->open(QIODevice::WriteOnly);
            is_write_pipe=true;
        }


    }
    else
    {
        if (is_write_pipe)
        {

            pipefile->close();
            delete pipefile;

            is_write_pipe=false;
            pipefile = 0;
        }
    }
}\


void packetParse::setPipeName(QString pipename_)
{
    pipename=pipename_;
}


QHash<QString,int>* packetParse::getCounters(void)
{
    return(&packet_counters);

}

void packetParse::resetCounters(void)
{
    packet_counters["num_good_packets"]=0;
    packet_counters["searches"] = 0;
    packet_counters["num_found_zzz"] = 0;
    packet_counters["num_data_words"] = 0;
    packet_counters["bind_stat"] = 0;
    packet_counters["n_datagrams"] = 0;
     packet_counters["datagramlen"] =0;


     packet_counters["packet_num_a"] = 0;
     packet_counters["packet_num_b"] = 0;

     packet_counters["packinc_a"] =0;


         packet_counters["lost_packets"]=0;

         packet_counters["ne_packnab"]=0;

}




void packetParse::stopStreams(void)
{
    is_running=false;

}

void packetParse::writeStreams()
{


    int k=0;
    //states
    // 0 look for 8 zz chars om a row of packet
    // 1 in packet
    //2 end of packet
    //3 error at top of packet
    //4 error at end of packet
    //5 good packet done




    //we have 30 long ints of data (64 bits)
    // we have 1 long int of fff at top of packet
    // we have 1 long int of fff at bottom of packet
    // what is k at end of data?

    is_running=true;
    fprintf(stderr,"Started packet Parser\n");
    while(is_running)
    {




        int length;
        unsigned char *datagram = data_fifo->read(&length);

        if (is_write_pipe && datagram)
        {

            pipefile->write((const char*)datagram,length);
            pipefile->flush();

        }

        if (datagram)
        {
            k=0;
             while(k<length)
            {


                staterecord[statereccount].state=state;
                staterecord[statereccount].k=k;
                statereccount = (statereccount+1)%statereclength;

                switch(state)
                {

                    case idle:

                        z_counter=0;
                        if (datagram[k]==0xff)
                             state = search_zzz;
                        else
                        {
                            state = idle;
                            k++;
                            packet_counters["searches"]++;
                            //!!baddatagram=datagram;
                        }

                    break;

                    case search_zzz://1st word -xfffffff's
                            //we should have 8 bytes of xff

                            if (datagram[k]==0xff && z_counter<16)
                            {
                                k++;
                                state = search_zzz;
                                z_counter++;
                            }
                            else if (z_counter==16)
                            {
                                z_counter=0;
                                state=read_packet_number_a;
                                packet_counters["num_found_zzz"]++;
                                data_counter=0;
                                data_counter_a=0;
                                data_counter_b=0;

                                packet_num_a=0;
                                packet_num_b=0;
                            }
                            else
                            {
                                state = idle;

                            }


                    break;

                    case read_packet_number_a:
                    if (z_counter<4)
                    {
                        //packet_num_a = (packet_num_a>>8) | ( (datagram[k]&0xff) <<24);
                        packet_num_a = (packet_num_a<<8) | ( (datagram[k]&0xff) );
                        k++;
                        state = read_packet_number_a;
                        z_counter++;
                    }

                    else
                    {
                        state = read_packet_number_b;
                        z_counter=0;
                    }




                    break;

                    case read_packet_number_b:

                    if (z_counter<4)
                    {
                        //packet_num_b = (packet_num_b>>8) | ( (datagram[k]&0xff) <<24);
                        packet_num_b = (packet_num_b<<8) | ( (datagram[k]&0xff) );
                        k++;
                        state = read_packet_number_b;
                        z_counter++;
                    }

                    else
                    {
                        state = in_data_a;



                        packet_counters["packinc_a"] =packet_num_a - packet_counters["packet_num_a"];
                        // we assume that if it packet_counters["packinc_a is huge, then we start up
                        // parsing just now... so set it to 2. <0 means huge number and it rolled over
                        if (packet_counters["packinc_a"]<0)
                            packet_counters["packinc_a"]=2;

                        if (packet_counters["packinc_a"]>200000)
                            packet_counters["packinc_a"]=2;

                        if (packet_counters["packinc_a"]>1)
                            packet_counters["lost_packets"]+=packet_counters["packinc_a"]-1;


                        packet_counters["packet_num_a"] = packet_num_a;
                        packet_counters["packet_num_b"] = packet_num_b;

                        if (packet_num_a != packet_num_b)
                            packet_counters["ne_packnab"]++;

                        z_counter=0;
                    }





                    break;

                    case in_data_a: // in data

                            data_a.append(datagram[k]);k++;
                            data_counter_a++;

                            if (data_counter_a==4)
                                state=in_data_b;
                            else
                                state=in_data_a;

                    break;

                    case in_data_b: // in data

                                    data_b.append(datagram[k]);k++;
                                    data_counter_b++;

                                    if (data_counter_b==4)
                                        state=data_are_we_done;
                                    else
                                        state=in_data_b;

                            break;

                    case data_are_we_done:
                         data_counter++;
                         packet_counters["num_data_words"]++;
                         data_counter_a=0;
                         data_counter_b=0;
                         //the hard code 180 is the length of one packet sent from
                         // gb enet block on the roach. it can have many events etc..
                         // this code here splits the 64 bit words into two streams A and B,
                         // which correspond to the two fifo readers in the FW.we hardcode
                         // gb enet bloc to have 1440 len packets plus the zzz's on start and end.
                         if (data_counter==180)
                            state=count_end_zzz;
                         else
                             state = in_data_a;


                    break;


                    case count_end_zzz:
                                if (datagram[k]==0xff && z_counter<8)
                                {
                                    k++;
                                    state = count_end_zzz;
                                    z_counter++;
                                }
                                else if ( z_counter==8)
                                {
                                    z_counter=0;
                                    state = end_packet;
                                }
                                else
                                {
                                   packet_counters["num_err_end"]++;
                                   state = idle;
                                }


                    break;

                    case end_packet:
                        packet_counters["num_good_packets"]++;
                        state = idle;
                        break;

                  default:
                                state = idle;
                                break;


                }
            }




            if (data_a.length()>1048576)
        {


            if (raw_data_a.write(data_a))
            {
               emit dataAvailA();
            }
            else
                emit bufferFull();

            data_a.clear();
        }

            if (data_b.length()>1048576)
        {

            if (raw_data_b.write(data_b))
            {
                emit dataAvailB();
            }
            else
                emit bufferFull();

            data_b.clear();
        }



        }
        else
        {
            usleep(1000);


          if (is_dump_fifos)
            {
                state=idle;

                if (data_a.length()>0)
                {
                    if (raw_data_a.write(data_a))
                    {
                       emit dataAvailA();
                    }
                    else
                        emit bufferFull();

                    data_a.clear();
                }

                if (data_b.length()>0)
                {
                    if (raw_data_b.write(data_b))
                    {
                        emit dataAvailB();
                    }
                    else
                        emit bufferFull();

                    data_b.clear();
                }

                is_dump_fifos   =false;
            }



        }


    }

    fprintf(stderr,"Stopped Packet parser\n");

}

void packetParse::dumpFifo(void)
{
    is_dump_fifos=true;
}

dataQueue* packetParse::getOutQueueA(void)
{

    return(&raw_data_a);
}
dataQueue* packetParse::getOutQueueB(void)
{
     return(&raw_data_b);
}

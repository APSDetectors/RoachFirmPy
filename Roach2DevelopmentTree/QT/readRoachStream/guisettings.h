#ifndef GUISETTINGS_H
#define GUISETTINGS_H

#include <QString>
#include <stdlib.h>
#include <stdio.h>


class guiSettings
{
public:
    guiSettings();



    int scopecontrol;





    //xmit dest ip and port
    QString txdestip;


    int txdestport;

    bool txstream;

    //rcv ram
    unsigned char rcvdata[8192];


    //rcv ip
    int rcv_src_ip;
    char rcv_src_ip_str[80];
    int rcv_src_port;



};

#endif // GUISETTINGS_H

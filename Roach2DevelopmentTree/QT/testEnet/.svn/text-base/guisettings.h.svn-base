#ifndef GUISETTINGS_H
#define GUISETTINGS_H

#include <QString>
#include <stdlib.h>
#include <stdio.h>


class guiSettings
{
public:
    guiSettings();

    void setControl0(void);
    void setControl1(void);

    int which_xmit;


    //status of xaui 0
    int statPort0;
    int TxOv0;
    int LedTx0;
    int LedRx0;
    int LedUp0;

    //xmat fsm
    int txframelength;
    unsigned char xmitdata[8192];
    bool is_save_xmitdata;

    //control register

    int txstream;
    int txpacket;
    int xauireset;
    int rewindram;
    int control0;
    int control1;


    //xmit dest ip and port
    int txdestip;
    char txdestipstr[80];

    int txdestport;



    //rcv ram
    unsigned char rcvdata[8192];

    //rcv status
    int statPort1;
    int LedTx1;
    int LedRx1;
    int LedUp1;
    int TxOv1;
    int RxVld1;
    int RxEOF1;

    //rcv ip
    int rcv_src_ip;
    char rcv_src_ip_str[80];
    int rcv_src_port;

    bool read_rcv_ram;

    //true to read regs from roach
    bool get_status;


    // pipes
    char pypipe_out[256];
    char pypipe_in[256];
    bool is_pipe_open;


    //regs to read from roach
    unsigned int RdIsPacket_dbgCount;
    unsigned int RxVld1_dbgCount;
    unsigned int TxEOF0_dbgCount;
    unsigned int capture_rcvmemaddr;
    unsigned int  testData_framelength;




    FILE *pyout;
    FILE *pyin;

    QString readLine(void);
    void writeLine(QString& data);
    QString readInPipe(void);

    bool openPipes(void);
    void closePipes(void);
    void executePython(void);
    void setupPython(void);
    void shutdownPython(void);

    void roachWriteInt(QString regname, int val);
    int roachReadInt(QString regname);
    QString roachRead(QString regname,int count);

    void roachWrite(QString regname, unsigned char *data);

    void getStatusRegs(void);
    int ipStrToInt(QString ip);
    QString ipIntToStr(int int_ip);


};

#endif // GUISETTINGS_H

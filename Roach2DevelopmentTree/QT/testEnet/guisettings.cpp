#include "guisettings.h"

#import <QStringList>

guiSettings::guiSettings()
{


    which_xmit=0;

    //status of xaui 0
     statPort0 = 0;
     TxOv0 = 0;
     LedTx0 = 0;
     LedRx0 = 0;
     LedUp0 = 0;

    //xmat fsm
     txframelength = 64;
    is_save_xmitdata=false;

    //control register

     txstream = 0;
     txpacket = 0;
     xauireset = 0;
     rewindram=0;
     control0 = 0;
     control1=0;


    //xmit dest ip and port
     strcpy(txdestipstr,"192.168.1.102");

     txdestip = ipStrToInt(txdestipstr);
     txdestport = 54321;



    //rcv ram


    //rcv status
     statPort1 = 0;
     LedTx1 = 0;
     LedRx1 = 0;
     LedUp1 = 0;
     TxOv1 = 0;
     RxVld1 = 0;
     RxEOF1 = 0;

    //rcv ip
     rcv_src_ip = 0;
     rcv_src_port = 0;

     read_rcv_ram=false;

     get_status=false;
    is_pipe_open=false;


    //we read from roach regs just ot print on screen
     RdIsPacket_dbgCount=0;
     RxVld1_dbgCount=0;
     TxEOF0_dbgCount=0;
     capture_rcvmemaddr=0;
       testData_framelength=0;



    pyout=0;
    pyin=0;

    strcpy(pypipe_out,"/local/pyfifoout");
    strcpy(pypipe_in,"/local/pyfifoin");
}


void guiSettings::setControl0(void)
{

     control0 = ( txstream <<2) +
             xauireset +
            ( xauireset<<1) +
            ( txpacket<<3) +
             (rewindram<<4);
}


void guiSettings::setControl1(void)
{

     control1 = ( txstream <<2) +
             xauireset +
            ( xauireset<<1) +
            ( txpacket<<3) +
             (rewindram<<4);
}






QString guiSettings::readLine(void)
{
    char strg[256];

    if (pyout==0)
        return(QString("\0"));

    fgets(strg,255,pyin);
    printf("%s\n",strg);
    return(QString((const char*) strg));
}

void guiSettings::writeLine(QString &data)
{
    if (pyout==0)
        return;


    printf("%s\n",data.toStdString().c_str());

    fprintf(pyout,"%s\n",data.toStdString().c_str());

    fflush(pyout);

}

QString guiSettings::readInPipe(void)
{

}

bool guiSettings::openPipes(void)
{
    char cmd[255];


    sprintf(cmd,"sleep 999998 > %s &",pypipe_out);
    system(cmd);

    sprintf(cmd,"sleep 999998 > %s &",pypipe_in);
    system(cmd);

    sprintf(cmd,"xterm -e \"/APSshare/epd/rh6-x86_64/bin/ipython -pylab < %s \" &",pypipe_out);
    system(cmd);



    pyin=fopen(pypipe_in,"r");

    pyout=fopen(pypipe_out,"w");

    if (!pyin)
        return(false);

    if (!pyout)
        return(false);



    setupPython();

    return(true);

}

void guiSettings::closePipes(void)
{


    fclose(pyin);
    fclose(pyout);
    pyin=0;
    pyout=0;
 shutdownPython();
}


void guiSettings::setupPython(void)
{

    if (pyout==0)
        return;

    char cmd[256];
    void *ptr;
    FILE *cmdfile = fopen("../testEnet/roachsetup.py","r");

    ptr = fgets(cmd,255,cmdfile);
    while(ptr)
    {
        QString cmdx=QString(cmd);
            writeLine(cmdx);
            //printf("%s",cmd);
            ptr = fgets(cmd,255,cmdfile);
    }

            fclose(cmdfile);

}



void guiSettings::shutdownPython()
{
    char cmd[255];
    sprintf(cmd,"pkill -9 sleep");
    system(cmd);
    sprintf(cmd,"pkill -9 python");
    system(cmd);

    sprintf(cmd,"pkill -9 nc");
    system(cmd);

}

void guiSettings::roachWriteInt(QString regname, int val)
{
    QString cmd;

    if (pyout==0)
        return;


    cmd = QString("roach2.writeInt('%1',%2)").arg(regname).arg((u_int32_t)val);

    writeLine(cmd);


}


void guiSettings::roachWrite(QString regname, unsigned char* data)
{
    QString cmd;

    if (pyout==0)
        return;


    cmd = QString("roach2.write('%1','%2')").arg(regname).arg((char*)data);

    writeLine(cmd);


}


int guiSettings::roachReadInt(QString regname)
{
    QString cmd;

    if (pyout==0)
        return(0);


    cmd = QString("valx = roach2.readInt('%1')").arg(regname);
    writeLine(cmd);

    cmd = QString("sv.getInt(valx)");
    writeLine(cmd);

    QString line;
    line = readLine();
    line=readLine();
    int val = line.toInt();
    line=readLine();
    return(val);



}


QString guiSettings::roachRead(QString regname,int count)
{
    QString cmd;
    char data[8192];

    if (pyout==0)
        return(QString("\0"));

    if (count>8192)
        count= 8192;

    cmd = QString("valx = roach2.read('%1',%2)").arg(regname).arg(count);
    writeLine(cmd);

    cmd = QString("sv.getByteArray(valx)");
    writeLine(cmd);
    QString line;
    line = readLine();//getByteArray
    line=readLine();//int that is len of the array
    int length = line.toInt();

    if (length>8192)
        length=8192;



    int nread = fread(data, 1, length, pyin);
    printf("nread =%d\n",nread);



    line=readLine();//!getByteArray

    return(QString((const char*) data));

}


void guiSettings::getStatusRegs(void)
{

    if (pyout==0)
        return;


    statPort0=roachReadInt("statPort0");

      #ifdef TWOINTERFACE

    statPort1=roachReadInt("statPort1");
    LedTx1= roachReadInt("LedTx1_dbgCount");
    LedRx1= roachReadInt("LedRx1_dbgCount");
    LedUp1= roachReadInt("LedUp1_dbgCount");

    TxOv1= roachReadInt("TxOv1_dbgCount");
    RxVld1= roachReadInt("RxVld1_dbgCount");
    RxEOF1= roachReadInt("RxEOF1_dbgCount");
    RxVld1_dbgCount= roachReadInt("RxVld1_dbgCount");
    rcv_src_ip = roachReadInt("rxSrcAddrIP1");
    strcpy(rcv_src_ip_str,ipIntToStr(rcv_src_ip).toStdString().c_str());
    rcv_src_port=roachReadInt("rxSrcPort1");

#else
    rcv_src_ip = roachReadInt("rxSrcAddrIP0");
    strcpy(rcv_src_ip_str,ipIntToStr(rcv_src_ip).toStdString().c_str());
    rcv_src_port=roachReadInt("rxSrcPort0");
#endif

    LedTx0= roachReadInt("LedTx0_dbgCount");
    LedRx0= roachReadInt("LedRx0_dbgCount");
    LedUp0= roachReadInt("LedUp0_dbgCount");




     RdIsPacket_dbgCount = roachReadInt("RdIsPacket_dbgCount");
     TxEOF0_dbgCount= roachReadInt("TxEOF0_dbgCount");
     capture_rcvmemaddr= roachReadInt("capture_rcvmemaddr");
      testData_framelength= roachReadInt("testData_framelength");






}


int guiSettings::ipStrToInt(QString ip)
{
    QStringList nums=ip.split('.');

    unsigned int int_ip=0;

    int_ip = (nums[0].toInt()) << 24;
    int_ip += (nums[1].toInt()) << 16;
    int_ip += (nums[2].toInt()) << 8;
    int_ip += (nums[3].toInt());
    return(int_ip);
}


QString guiSettings::ipIntToStr(int int_ip)
{
    QString ip;
    int nums[4];

    nums[0] = (int_ip & 0xff000000)>>24;
    nums[1] = (int_ip & 0x00ff0000)>>16;
    nums[2] = (int_ip & 0x0000ff00)>>8;
    nums[3] = (int_ip & 0x000000ff);


    ip=QString("%1.%2.%3.%4").arg(nums[0]).arg(nums[1]).arg(nums[2]).arg(nums[3]);


    return(ip);
}


void guiSettings::executePython(void)
{



    roachWriteInt("control0",control0);




}



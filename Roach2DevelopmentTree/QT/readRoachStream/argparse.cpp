#include "argparse.h"
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
using namespace std;

argParse::argParse() :

    LocalIP("192.168.1.102"),
    cmd_in_pipe_name("stdin"),
    cmd_out_pipe_name("stdout")
{


    q_packetlen = 10000;
    LocalPort=50000;
    //q len is a power of 2, so it is 2^20 long
         q_length=20;

         is_open_port=true;

        is_open_cmd_pipe=true;
        is_print=false;
}

void argParse::report(void)
{
    cerr << " Startup Settings"<<endl;

    cerr << "Local Port: " << LocalPort << endl;
    cerr << "Q length: " << q_length <<endl;



    cerr << "Local IP: " << LocalIP.toString().toStdString() <<endl;
    cerr << "IsOpenPort: " << is_open_port <<endl;

    cerr << "InCmdPipeName: "<< cmd_in_pipe_name.toStdString() <<endl;
    cerr << "OutCmdPipeName: "<< cmd_out_pipe_name.toStdString() <<endl;
    cerr << "isopenCmdPipe: " << is_open_cmd_pipe <<endl;

    cerr << "is_print: " << is_print <<endl;


}

void argParse::parseArgs(QStringList args)
{
    int num_args = args.size();

    bool ok;


    int curr_arg =1;

    while (curr_arg<num_args)
    {
        QString arg= args.at(curr_arg);

        if (arg=="--cmd_in_pipe_name")
        {
            curr_arg++;
            cmd_in_pipe_name=args.at(curr_arg);
        }
        if (arg=="--cmd_out_pipe_name")
        {
            curr_arg++;
            cmd_out_pipe_name=args.at(curr_arg);
        }




        if (arg=="--LocalIP")
        {
            curr_arg++;
            LocalIP = args.at(curr_arg);
        }



        if (arg=="--LocPort")
        {
            curr_arg++;
            LocalPort = args.at(curr_arg).toInt(&ok,10);
        }



        if (arg=="--qlength")
        {
            curr_arg++;
            q_length = args.at(curr_arg).toInt(&ok,10);
        }


        if (arg=="--openport")
        {
            curr_arg++;
            if (args.at(curr_arg)==QString("true"))
                is_open_port=true;
            else
                 is_open_port=false;
        }

        if (arg=="--is_print")
        {
            curr_arg++;
            if (args.at(curr_arg)==QString("true"))
                is_print=true;
            else
                is_print =false;
        }


        curr_arg++;

    }
}

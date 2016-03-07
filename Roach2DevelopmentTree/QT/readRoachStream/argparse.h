#ifndef ARGPARSE_H
#define ARGPARSE_H

#include <QString>
#include <QStringList>
#include <QHostAddress>
class argParse
{
public:
    argParse();


    void parseArgs(QStringList args);

    void report(void);


    int q_length;
    int q_packetlen;


    QString cmd_in_pipe_name;
    QString cmd_out_pipe_name;

    bool is_open_cmd_pipe;



    QHostAddress LocalIP;
    quint16      LocalPort;

    bool is_open_port;

    bool is_print;

};

#endif // ARGPARSE_H

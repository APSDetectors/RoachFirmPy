#include "filesaver.h"
/**
 * @brief fileSaver::fileSaver
 * @param parent
 */
fileSaver::fileSaver(QObject *parent) :
    QObject(parent),
    fname("/localc/temp/defaultfname")
{
    is_stream = false;
    parser = 0;
    events = 0;

}
/**
 * @brief fileSaver::setEventSource
 *  Sets hash table where data is stored.
 * @param events_ POinter to hash table where we get data.
 */
void fileSaver::setEventSource(roachParser *parse_)
{
    parser = parse_;

}

/**
 * @brief fileSaver::setFileName Sets filenaje where we store data. data is actially a directoryw/ files/
 * @param fname_ string w/ filanem and path.
 */
void fileSaver::setFileName(QString fname_)
{
    fname = fname_;
}

/**
 * @brief fileSaver::setIsStream turn on /off streaming to file in real time
 * @param is_stream_
 */
void fileSaver::setIsStream(bool is_stream_)
{
    is_stream = is_stream_;
}


void fileSaver::doSaveAll(void)
{

    events=parser->getEventList();
    while (events!=0)\
    {
        saveNow();
        events->clear();
        delete events;
        events = parser->getEventList();

    }

    emit saveDone(QString("fileSaver::doSaveAll done\n"));
}


void fileSaver::doSaveThread(void)
{
    while (is_stream)
    {
        events=parser->getEventList();
        if (events==0)\
        {
            usleep(10000);
        }
        else
        {
            saveNow();
            delete events;
            events = 0;

        }
    }
}

/**
 * @brief fileSaver::saveNow
 */
void fileSaver::saveNow(void)
{
    QDir prnt;

    if (events==0)
        return;

        prnt.mkdir(fname);

        if (prnt.exists(fname))
        {
            prnt.cd(fname);

            //QHash<int,QHash<QString,QList<float> > > events;
            QList<int> keys1=(*events).keys();
            for (int i=0;i<keys1.length();i++)
            {
                int chan = keys1[i];

                if ((*events)[chan]["bin"].length() > 0)
                {
                    int bin = (int)((*events)[chan]["bin"][0]);
                    QString dirname = QString("chan_%1_bin_%2").arg(chan).arg(bin);
                    prnt.mkdir(dirname);
                    if (prnt.cd(dirname))
                    {

                    QList<QString> keys2=(*events)[keys1[i]].keys();
                    for (int i2=0;i2<keys2.length();i2++)
                    {
                        QString fname = keys2[i2];
                        fname.prepend(prnt.absolutePath()+"/");
                        QFile file(fname);
                        file.open(QIODevice::Append);

                        //QDataStream out(&file);


                        for (int i3=0;i3< (*events)[keys1[i]][keys2[i2]].length() ; i3++)
                        {
                            //out << events[keys1[i]][keys2[i2]][i3];
                            float v = (*events)[keys1[i]][keys2[i2]][i3];
                            file.write((const char*)&v,sizeof(float));
                        }


                        file.close();

                    }


                    prnt.cdUp();
                    }

                }

            }

        }


}



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


/**
 * @brief fileSaver::getIsStream
 * @return
 */
bool fileSaver::getIsStream(void)
{
    return(is_stream);
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

    bool is_running = is_stream;
    int nwaits = 0;

    //we copy is_stream so we can start saving. if we turn off stream,
    // we only want to stop saving if no evetns left. else we miss end of data.
    // a feature of this is that you cannot stop saving until you stop gathering data.
    while (is_running)
    {
        events=parser->getEventList();
        if (events==0)\
        {
            // every time we have to wait for data, we inc counter.

            // wait .5sec for morre data
            usleep(500000);

            //if waited 2.5 sec end loop if user attempt stop it by is_stream=false
            if (nwaits>5)
            {
                is_running=is_stream;
            }
            else
            {
                 // every time we have to wait for data, we inc counter.
                nwaits++;

            }
        }
        else
        {
            saveNow();
            events->clear();
            delete events;
            events = 0;
            //set num of waits for data to 0.
            nwaits = 0;

        }
    }


    emit saveDone(QString("fileSaver::doSaveThread done\n"));

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



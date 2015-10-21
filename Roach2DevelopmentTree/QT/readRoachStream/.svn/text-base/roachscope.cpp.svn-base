#include "roachscope.h"
#include "ui_roachscope.h"


roachScope::roachScope(guiSettings &gui, QWidget *parent) :
    my_gui(gui),
    QMainWindow(parent),
    ui(new Ui::roachScope),
    poller()
{
    ui->setupUi(this);
    connect(&poller, SIGNAL(timeout()), this, SLOT(on_poll_timer()));

    is_zoom_x=true;
    is_zoom_y = true;

    ui->checkBox_zoomX->setChecked(is_zoom_x);
    ui->checkBox_zoomY->setChecked(is_zoom_y);

}

roachScope::~roachScope()
{
    delete ui;
}

void roachScope::on_pushButton_scopeTrig_clicked()
{
#if 0
    int trigin = ui->spinBox_scopeTrigInput->value() - 1;
    int we_in = ui->spinBox_scopeWeInput->value() - 1;
    int inpt = ui->spinBox_scopeInput->value() - 1;



    int inputsel = inpt + trigin*16  + we_in*64;
    my_gui.roachWriteInt("roachscope_inputsel",inputsel);

    int ctrl;

    int ig_we = (int)(ui->checkBox_scopeCapture->isChecked());
    int ig_tr = (int)(ui->checkBox_scopeIgTrig->isChecked());

    ctrl = ig_we*4 + ig_tr*2;

    my_gui.roachWriteInt("roachscope_snapshot_ctrl",ctrl);
    ctrl+=1;

    my_gui.roachWriteInt("roachscope_snapshot_ctrl",ctrl);


    poller.start(200);

    ui->label_RedLight->setStyleSheet("background-color: rgb(200, 0, 0);");

#endif
}

void roachScope::on_checkBox_scopeCapture_clicked(bool checked)
{



}

void roachScope::on_spinBox_scopeInput_valueChanged(int arg1)
{

}

void roachScope::on_poll_timer()
{
#if 0
    int stat = my_gui.roachReadInt("roachscope_snapshot_status");
    printf("stat 0x%x\n",stat);

    if (stat==4096)
        on_pushButton_scopeData_clicked();

#endif
}

void roachScope::on_pushButton_scopeData_clicked()
{


    ui->label_RedLight->setStyleSheet("background-color: rgb(16, 0, 0);");


    poller.stop();
/**
    my_gui.writeLine("tracestr = roach2.read('roachscope_snapshot_bram',4096)");
    my_gui.writeLine("trace = struct.unpack('2048H', tracestr)");
    my_gui.writeLine("figure(1)");
    my_gui.writeLine("clf()");
    my_gui.writeLine("plot(trace)");
    my_gui.writeLine("draw()");
    my_gui.writeLine("draw()");
*/
    char data[4096];
    // get ram into this c program, in to data
    //!!my_gui.roachRead("roachscope_snapshot_bram",4096,data);

    // only purpose of this is tp make the ram contents print on py window
    //!!my_gui.writeLine("roach2.read('roachscope_snapshot_bram',4096)");


    unsigned short* usptr=(unsigned short*)data;
    unsigned short sval,smax;
    smax=1;
    QVector<double> x(2048), y(2048); // initialize with entries 0..100




    QString plotbits = ui->lineEdit_plotBits->text();
    bool is_plotbits = ui->checkBox_plotBits->isChecked();
    int graphnum = 0;

    QCustomPlot *plot = ui->widget_QPlot;

    plot->clearGraphs();
    if (!is_plotbits)
    {
        for (int i=0; i<2048; ++i)
        {
            sval = usptr[i];
            short svx = sval&255;
            sval = sval>>8;
            sval = sval | (svx<<8);
            if (sval>smax)
                smax=sval;

            x[i] = (double)i;
            y[i] = (double)sval; // let's plot a quadratic function
        }

        plot->addGraph();
        plot->graph(0)->setData(x,y);
    }
    else
    {


        QStringList bitwidths=plotbits.split(';');

        int stbit = 15;
        int datash;
        int mask;
        int edbit;
        for (int k =0; k<bitwidths.length();k++)
        {
            QStringList couple = bitwidths[k].split(':');
            stbit = couple[0].toInt();
            edbit=couple[1].toInt();

            int width =1+stbit - edbit;
            if (width>0)
            {
                plot->addGraph();


                mask = (1<<width)-1;


                for (int i=0;i<2048;i++)
                {
                    sval = usptr[i];
                    short svx = sval&255;
                    sval = sval>>8;
                    sval = sval | (svx<<8);

                    if (sval>smax)
                        smax=sval;

                    datash = sval>>edbit;
                    datash = datash&mask;
                    x[i] = (double)i;

                    double factor = (double)(1<<width);
                    if (bitwidths.length()<2)
                        factor = 1.0;


                    y[i] = 2*graphnum + ((double)(datash) )/factor;
                }
                plot->graph(graphnum)->setData(x,y);
                graphnum++;

                stbit = stbit - width;

            }

        }

    }




    plot->setInteractions(QCP::iRangeDrag | QCP::iRangeZoom);

    setZooming();
    plot->xAxis->setLabel("clocks");
    plot->yAxis->setLabel("samples");
    plot->xAxis->setRange(0,2048);
    if (graphnum == 0)
        plot->yAxis->setRange(0,(double)smax);
    else
        plot->yAxis->setRange(0,(double)(graphnum*2));

    plot->replot();

}

void roachScope::setZooming(void)
{
    QCustomPlot *plot = ui->widget_QPlot;


    if (is_zoom_x & is_zoom_y)
        plot->axisRect()->setRangeZoom(Qt::Horizontal | Qt::Vertical);
    else if (is_zoom_x)
        plot->axisRect()->setRangeZoom(Qt::Horizontal );
    else if (is_zoom_y)
        plot->axisRect()->setRangeZoom(Qt::Vertical);
    else
        plot->axisRect()->setRangeZoom(false);
}

void roachScope::on_checkBox_zoomX_clicked(bool checked)
{

    is_zoom_x=checked;
    setZooming();


}

void roachScope::on_checkBox_zoomY_clicked(bool checked)
{
    is_zoom_y=checked;
    setZooming();
}

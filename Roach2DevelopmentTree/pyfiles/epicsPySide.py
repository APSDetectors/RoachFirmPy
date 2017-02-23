import sys, os, random, math, array, fractions
from PySide.QtCore import *
from PySide.QtGui import *
 

import socket
import matplotlib, time, struct, numpy
from bitstring import BitArray
import matplotlib.pyplot as mpl
mpl.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import h5py




import epics
import os
import subprocess
import time

import threading

widgetdict={}


def onChanges(pvname=None, value=None, char_value=None, **kw):
    #print 'PV Changed!! ', pvname, char_value, time.ctime()
    info = widgetdict[pvname]
    wtype = info['type']
    widget = info['obj']
    
    if wtype=='label':
        widget.set(char_value)
        
    

class epicsButton:
    def __init__(self,label,pvname):
        self.mypv = epics.PV(pvname,auto_monitor=False)
        self.button= QPushButton(label)
        self.button.setMaximumWidth(120)
        self.connect(self.button, SIGNAL('clicked()'), self.put)
    
    def put(self):
        self.mypv.put(1)
               


    
class epicsLabel:
    def __init__(self,pvname):
        self.mypv = epics.PV(pvname,auto_monitor=True)
        self.label = QLabel('xxxxx')
        self.label.setMaximumWidth(100)
        
        widgetdict[pvname]={'type':'label' , 'obj':self}
        mypv.add_callback(onChanges)
        
    def set(self,val)
        self.label.setText(val)
     

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('EPICS')
       
        self.create_main_frame()
       


    def create_main_frame(self):
        self.main_frame = QWidget()
        

        


def main():
    global app
    global form
    print 'hello'
    if app==None:
        app = QApplication(sys.argv)
    
    form = AppForm()
    form.show()
    app.exec_()



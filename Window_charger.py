"""
This file is responsible for creating the main Charger display
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from threading import Thread
import threading

#Bluetooth connection with wheelchair RPi4
from bluedot.btcomm import BluetoothServer
from time import sleep
# from signal import pause
import signal

#Connection with Piccolo
import smbus
import time
import random

from TimerThread import Clock

from StateClass import State
import StateClass as sc

import QT_Helpers as qt_helper

import pymongo
from datetime import datetime

#select I2C bus1 on the Pi, give address for BMS (75)
bus = smbus.SMBus(1)
address = 0x55

clientStatus = 0
stop_thread=False
serverList = []
listT=[]
limit_IV=[10,30,20] #Imax,Vmax,Vmin
delayList = [] #delay threads in the list
delayTime=30 #seconds
updateTime=15*60 #seconds every 15 mins update state in mongo db
# qt_helper.timeoutGlobal = None # timeout thread global (only one timeout should b running at once)

count_start=0
count_stop=0

class Ui_MainWindow(object):
    """
    This class creates the main window displaying charger information
    """
    def setupUi(self, MainWindow):
        """
        This function will set up the UI elements that will be present on this window

        :param MainWindow: the window on which to build the elements
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-1, 170, 801, 150))
        font = QtGui.QFont()
        font.setPointSize(54)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(-1, 260, 801, 150))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(630, 0, 171, 71))
        self.lcdNumber.setObjectName("lcdNumber")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 611, 65))
        font = QtGui.QFont()
        font.setPointSize(38)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_pic = QtWidgets.QLabel(self.centralwidget)
        self.label_pic.setGeometry(QtCore.QRect(0, 440, 211, 131))
        self.label_pic.setObjectName("label_pic")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # loading image
        self.pixmap = QPixmap('ncpic.jpg')
        self.pixmap = self.pixmap.scaledToWidth(211)
        # adding image to label
        self.label_pic.setPixmap(self.pixmap)
        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        clock = Clock([self.lcdNumber])
        clock.start()

    def retranslateUi(self, MainWindow):
        """
        This function will reassign some components' textual content

        :param MainWindow: parent window of the target components
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Charger Available"))
        self.label_2.setText(_translate("MainWindow", "Charger #1 (Centennial)"))
        #self.label_pic.setText(_translate("MainWindow", "TextLabel"))
        #self.label_3.setText("Hello World")
        #print('state is',sc.CState)
        self.stateUpdate()
        t = Thread(target=self._bluetoothRun)
        t.start()
        
    def killTimeout(self):
        """
        This function kills the timeout delay thread
        """
        try:
            print(qt_helper.timeoutGlobal)
            qt_helper.timeoutGlobal.terminate()
            qt_helper.timeoutGlobal = None
        except:
            print("Failed to kill thread")
        
    def stateUpdate(self):
        """
        This function is the 'brains' of the state machine on the Charger side.  Each time it is called it updates the
        relevent components corresponding to the active state as defined by :obj:`StateClass.State`
        """
        global clientStatus, serverList, updateTime
        
        # terminate timeout on state change
        print('kill thread')
        self.killTimeout()
        
        self.label_3.setText("")
        if(sc.CState==State.CHARGER_AVAILABLE):
            self.label.setText("Charger Available")
#             self.label_3.setText("Charger Available")
            #if clientStatus==1:
                # start connection delay thread
             #   print('start connection delay for available charger')        
              #  qt_helper.timeoutGlobal = qt_helper.DelayAction(delayTime,[serverList[0].send,'2'],[serverList[0].disconnect_client,None],timer=self.label_3)
               # qt_helper.timeoutGlobal.start()
                #qt_helper.timeoutGlobal.join()
                
#         if(sc.CState==State.CHARGING_ALLOWED):
#             self.label.setText("Plug in your Unit")
#             self.label_3.setText("Charging Allowed")
        if(sc.CState==State.READY_TO_CHARGE):
            self.label.setText("Ready to Start Charging")

        if(sc.CState==State.CHARGING_IN_PROGRESS):
            self.label.setText("Charging in Progress")
        if(sc.CState==State.CHARGER_FAULTY_PLUGGED):
            self.label.setText("Unplug your Unit")
            self.label_3.setText("Charger Error")
        if(sc.CState==State.CHARGER_FAULTY_UNPLUGGED):
            self.label.setText("Charger Malfunction")
        if(sc.CState==State.WC_FULLY_CHARGED):
            self.label.setText("Battery Fully Charged")
            self.label_3.setText("Unplug your Unit")
        if(sc.CState==State.BATTERY_FAULTY):
            self.label.setText("Unplug your Unit")
            self.label_3.setText("Battery Fault")
        if(sc.CState==State.TERMINATED_BY_USER):
            self.label.setText("Charging Completed")
            self.label_3.setText("Unplug your Unit")
        if(sc.CState==State.AWAITING_CONNECTION):
            self.label.setText("Plug in your Unit")
            self.label_3.setText("Charging Allowed")
            
        
        try:
            print(qt_helper.timeoutMongo)
            qt_helper.timeoutMongo.terminate()
            qt_helper.timeoutMongo.join()
            qt_helper.timeoutMongo = None
        except:
            print("Failed to kill thread")
        # update state in MongoDB every 15 seconds or when state updated
        self.stateUpdateMongo()
        qt_helper.timeoutMongo = qt_helper.DelayAction(updateTime,[print,'5 seconds left'],[self.stateUpdate,None],timer=None)
        qt_helper.timeoutMongo.start()

    def stateUpdateMongo(self):
        """
        This function updates the state in the Mongo Database
        """
        try:
            client = pymongo.MongoClient("mongodb+srv://wheelchair:wheelchair@cluster0.pywpd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

            #Create database
            mydb = client["ChargerData"]  # you can also use dot notation client.mydatabase
            #Create collection with one insertion
            coll = mydb["charger_state"]
#             data = pd.read_csv(nameCSV)
#             payload = json.loads(data.to_json(orient='records'))
#             coll.insert_many(payload)
            dateUpload = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            myquery = {"name": "Charger"}
            newState = {"$set" :{"name": "Charger", "state": str(sc.CState), "last_update": dateUpload}}
            coll.update_one(myquery, newState)
            print(coll.find_one())
            print(coll.count_documents)
        except Exception as e:
            print("no internet connection: ",e)
    
    def _bluetoothRun(self):
        """
        This is a container for all bluetooth functions
        """
        global listT, limit_IV, delayList, delayTime
        
        def data_received(data):
            """
            This function reacts to data received over bluetooth
            :param data: data received over bluetooth
            """
            global stop_thread, count_start, count_stop
            try:
                if listT[0].is_alive()==False:
                    listT.clear()#if after disconnecting the battery, left
                    print("cleared the thread")
                else:
                    print("still alive")
            except:
                print("empty list")
            t2 = Thread(target=self._readI2C)
            listT.append(t2)
            
            BLUSending=1
            print("recv - {}".format(data))
            try:
                if listT[0].is_alive():
                    print("waiting for thred")
                    stop_thread=True
                    listT[0].join()
            except:
                print("no thread in stop")
            
            msgPic=data.split(',')
            msgPic[0]=int(msgPic[0])
            msgPic[1]=int(msgPic[1])
            msgPic[2]=int(msgPic[2])
            
            #Send to Piccolo, after receiving from RPi
            if msgPic[0]==3: #request
                try:
                    if listT[0].is_alive():
                        stop_thread=True
                        listT[0].join()
                except:
                    print("no thread request")
                if msgPic[1]<limit_IV[0] and msgPic[2]<limit_IV[1] and msgPic[2]>limit_IV[2]: 
                    bus.write_byte(address,3)
                    bus.write_byte(address,msgPic[1]) #battery current
                    bus.write_byte(address,msgPic[2]) #battery voltage
                    MSG = bus.read_byte_data(address,1)
                else:
                    MSG="4"
                print(MSG)
                listT.clear()
            
            if msgPic[0]==7: #start
                #Send the data to Piccolo
                print("sending START")
                print(listT[0].is_alive())
                time.sleep(0.5)
                try:
                    if listT[0].is_alive():
                        stop_thread=True
                        listT[0].join()
                except:
                    print("No thread start")
                bus.write_byte(address,7)
                bus.write_byte(address,msgPic[1]) #battery current
                bus.write_byte(address,msgPic[2]) #battery voltage
                MSG = bus.read_byte_data(address,1)
                print(MSG)
                listT.clear()
                
            if msgPic[0]==11:#stop chargin
                print("stop",count_stop,"start",count_start)
                print("sending STOP")
                print(listT[0].is_alive())
                time.sleep(0.5)
                try:
                    bus.write_byte(address,msgPic[0])
                    bus.write_byte(address,msgPic[1]) #battery current
                    bus.write_byte(address,msgPic[2]) #battery voltage
                    MSG = bus.read_byte_data(address,1)
                    print(MSG)
                except Exception as e:
                    print(e)
                listT.clear()
            
            MSG=int(MSG)
            server.send(str(MSG))
            #Send to RPi after receiving from Piccolo
            if MSG==4:
                sc.CState=State.CHARGER_AVAILABLE
                self.stateUpdate()
                time.sleep(2)
                server.disconnect_client()
            if MSG==5:
                sc.CState=State.AWAITING_CONNECTION
                self.stateUpdate()
                qt_helper.timeoutGlobal = qt_helper.DelayAction(delayTime,[serverList[0].send,'2'],[serverList[0].disconnect_client,None],timer=self.label_3)
                
#                 #Create delay thread to make it possible to get from t2
#                 if delayList[0].is_alive():
#                     delayList[0].terminate()
#                     delayList.clear()
                #start new delay thread
                
                #create I2C thread to get respose from TI
                t2 = Thread(target=self._readI2C)
                listT.append(t2)
                stop_thread=False
                listT[0].start()
                count_start=count_start+1
                #kill thread of connection

                print('started delay for msg5')
#                 delayList[0].start(
                #delayList[0].join()
                print('cleared delay')
                #delayList.clear()
            if MSG==6: 
                sc.CState=State.READY_TO_CHARGE
                self.stateUpdate()
            if MSG==7:
                sc.CState=State.CHARGING_IN_PROGRESS
                self.stateUpdate()
                t2 = Thread(target=self._readI2C)
                listT.append(t2)
                stop_thread=False
                listT[0].start()
                count_start=count_start+1
            if MSG==8:
                sc.CState=State.CHARGER_FAULTY_PLUGGED
                self.stateUpdate()
            if MSG==10:
                sc.CState=State.BATTERY_FAULTY
                self.stateUpdate()
            if MSG==11:
                sc.CState=State.TERMINATED_BY_USER
                self.stateUpdate()
                t2 = Thread(target=self._readI2C)
                listT.append(t2)
                stop_thread=False
                listT[0].start()
                count_start=count_start+1

            
            print("Sent is",str(MSG)) 
                

        def client_connected():
            """
            This function sends the confirmation to the wheelchair that the connection was successful
            """
            global clientStatus
            server.send("1")
            print('client status is',clientStatus)
            if clientStatus == 0:
                print("client connected")
                clientStatus=1
            # start connection delay thread
#             qt_helper.timeoutGlobal = qt_helper.DelayAction(delayTime,[server.send,'2'],[server.disconnect_client,None])
#             qt_helper.timeoutGlobal.start()
#             qt_helper.timeoutGlobal.join()

                #server.disconnect_client()
            

        def client_disconnected():
            """
            This function disconnects the client from the Charger
            """
            global clientStatus, stop_thread 
            print("client disconnected")
            clientStatus=0
            # verify the state
            if sc.CState == State.READY_TO_CHARGE or sc.CState == State.AWAITING_CONNECTION:
                try:
                    if listT[0].is_alive():
                        print("waiting for thread")
                        stop_thread=True
                        listT[0].join()
                except:
                    print("no thread in stop")
                time.sleep(0.5)
                bus.write_byte(address, 15) #Reset TI Piccolo
                MSG1 = bus.read_byte_data(address, 1)
                MSG1 = int(MSG1)
                print("message received is", str(MSG1))
                sc.CState=State.CHARGER_AVAILABLE
                self.stateUpdate()
                listT.clear()
            else:
                    #print("disconnected by user")
                print("Need to unplug the unit")
                self.stateUpdate()
            #kill any delay thread
            try:
                self.killTimeout()
#                 if delayList[0].is_alive():
#                     delayList[0].terminate()
#                     delayList.clear()
            except:
                print("no threads left for now")
            
        print("init")
        server = BluetoothServer(
            data_received,
            auto_start = False,
            when_client_connects = client_connected,
            when_client_disconnects = client_disconnected)

        print("starting")
        server.start()
        print(server.server_address)
        print("waiting for connection")
        serverList.append(server)
        try:
            signal.pause()
        except KeyboardInterrupt as e:
            print("cancelled by user")
        finally:
            print("stopping")
            server.stop()
        print("stopped")
    
    def _readI2C(self):
        """
        This function reads and reacts to the I2C communication from the TI Piccolo
        """
        #print('read2c')
        global stop_thread, serverList, listT, count_start, count_stop
        global delayList, delayTime

#         print("thread started")
#         try:
#             print('delay list in thread is',delayList)
#             delayThread=delayList[0]
#         except:
#             print('no delay threads')
        time.sleep(0.5)
        
        while True:
            #print('delay list in while loop',delayThread)
            try:
                bus.write_byte(address,21)
                MSG1 = bus.read_byte_data(address,1)
                MSG1=int(MSG1)
                print("message received is",str(MSG1))
                #print('delay list in thread is',delayThread)
                if MSG1==1: #after error sovled update into available
                    sc.CState=State.CHARGER_AVAILABLE
                    self.stateUpdate()
                  
                if MSG1==6:
                    if sc.CState!=State.READY_TO_CHARGE:
                        print('we are here')
                        serverList[0].send(str(MSG1))
                        sc.CState=State.READY_TO_CHARGE 
                        self.stateUpdate()
                        print("ready to charge")
                        stop_thread=True
                if MSG1==7:
                    if sc.CState!=State.CHARGING_IN_PROGRESS:
                        serverList[0].send(str(MSG1))
                        sc.CState=State.CHARGING_IN_PROGRESS
                        self.stateUpdate()
                        print("ready to charge")
                        stop_thread=True
                    
                if MSG1==8:
                    if sc.CState!=State.CHARGER_FAULTY_PLUGGED:
                        serverList[0].send(str(MSG1))
                        sc.CState=State.CHARGER_FAULTY_PLUGGED
                        self.stateUpdate()
                        
                if MSG1==9:
                    if sc.CState!=State.WC_FULLY_CHARGED:
                        serverList[0].send(str(MSG1))
                        sc.CState=State.WC_FULLY_CHARGED
                        self.stateUpdate()
                if MSG1==10:
                    if sc.CState!=State.BATTERY_FAULTY:
                        serverList[0].send(str(MSG1))
                        sc.CState=State.BATTERY_FAULTY
                        self.stateUpdate()
                if MSG1==12:
                    if sc.CState!=State.CHARGER_FAULTY_UNPLUGGED:
                        sc.CState=State.CHARGER_FAULTY_UNPLUGGED
                        self.stateUpdate()
                        
                if MSG1==14:
                    serverList[0].send(str(MSG1))
                    stop_thread=True
                    if sc.CState==State.CHARGER_FAULTY_PLUGGED:
                        sc.CState=State.CHARGER_FAULTY_UNPLUGGED
                        self.stateUpdate()
                    else:
                        sc.CState=State.CHARGER_AVAILABLE
                        self.stateUpdate()
                    
            except Exception as e:
                #continue
                print(e)
                print('I2C problem')
            if stop_thread:
                count_stop=count_stop+1
                print("thread is stopped")
                #listT.clear()
                break
            time.sleep(2)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())

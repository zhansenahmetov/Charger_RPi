"""
This file contains helper functions and classes that facilitate creation of GUI components and background processes
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
#import WCharging as wc
import time

timeoutGlobal = None
timeoutMongo = None
    
class DelayAction(Thread):
    """
    This class is a generic thread for delaying the execution of an arbitrary quantity of functions
    """

    def __init__(self,duration,*funcs,timer=None):
        """
        This function initializes the delay thread

        :param duration: duration in seconds until the callback functions are run
        :param funcs: callback functions to be run at the end of the duration formatted:[function,parameter]\n
            ``Note: To call functions that do not take parameters, None may be used: [function,None]``
        :param timer: Label element to update with the countdown time
        """
        Thread.__init__(self,name="Delay_Func")
        self.funcs = funcs
#         self.argv = argv   # argument(s)
#         self.argc = argc   # argument count
        self.duration = duration
        self.label = timer
        self._running = True
        print("Starting delay with duration: ",duration)
        
#         print("defining delay")
    def terminate(self):
        """
        This function stops the delay thread
        """
        print("timeout stopped")
        self._running = False

    def run(self):
        """
        This function runs the timer loop that checks for when the delay duration is over, updating the timer each second
        """
#         print("executing delayed action")
        try:
            n=self.duration
            # delay while updating 1 second at a time
            while self._running and n>0:
                if self.label:
                    self.label.setText("Expires in "+str(n)+" seconds.")
                    self.label.update()
                time.sleep(1)
                print("running: "+str(self._running)+"counting down: ",n)
                n-=1
            # if not terminated, run functions
            # i[0] = function
            # i[1] = optional parameter (None for no parameter)
            if self._running:
                for i in self.funcs:
                    print("Executing func:",i[0])
                    if i[1]:
                        i[0](i[1])
                    else:
                        i[0]()
                        
                    time.sleep(0.5)
            #print('thread stopped')
                        
        except Exception as e:
            print("Error in Delay function: ",e)

def makeButton(self,x,y,w,h,fontsize,name,text):
    """
    This function condenses the process of creating buttons

    :param Self: parent window or object
    :param x: Top left x position of the button
    :param y: Top left y position of the button
    :param w: Width of the button
    :param h: Height of the button
    :param fontsize: Fontsize of the button
    :param name: Object name of the button object
    :param text: Text Content of the button
    :return: Created button object
    """
    pushButton = QtWidgets.QPushButton(self)
    pushButton.setGeometry(QtCore.QRect(x, y, w, h))
    font = QtGui.QFont()
    font.setPointSize(fontsize)
    pushButton.setFont(font)
    pushButton.setObjectName(name)
    pushButton.setText(QtCore.QCoreApplication.translate("Dialog", text))
    return pushButton;

def makeTabLabel(self,x,y,w,h,grayscale,fontSize,name,text):
    """
    This function condenses the process of creating tab labels

    :param self: parent window or object
    :param x: Top left x position of the tab label
    :param y: Top left y position of the tab label
    :param w: Width of the tab label
    :param h: Height of the tab label
    :param grayscale: Singular rgb value (0-255) representative of the greyscale rbg(x,x,x)
    :param FontSize: Font size of the tab label
    :param name: Object name of the tab label
    :param text: Text content of the tab label
    :return: Created tab label object
    """
    label = QtWidgets.QLabel(self.centralwidget)
    label.setGeometry(QtCore.QRect(x, y, w, h))
    font = QtGui.QFont()
    font.setPointSize(fontSize)
    label.setFont(font)
    label.setLayoutDirection(QtCore.Qt.LeftToRight)
    label.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb("+str(grayscale)+", "+str(grayscale)+", "+str(grayscale)+");")
    label.setFrameShape(QtWidgets.QFrame.NoFrame)
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setObjectName(name)
    label.setText(QtCore.QCoreApplication.translate("MainWindow",text))
    return label
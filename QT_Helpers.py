from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
#import WCharging as wc
import time

timeoutGlobal = None
timeoutMongo = None

class autoCloseMsg(QtWidgets.QMessageBox):
    
    def __init__(self,*__args):
        QtWidgets.QMessageBox.__init__(self)
        self.lifetime = 0 # message stays for x seconds
        self.time = 0
        
    def showEvent(self, QShowEvent):
        self.time = 0
        if self.lifetime:
            self.startTimer(1000) # start 1 Hz timer with Message box
        
    def timerEvent(self, *args, **kwargs):
        self.time += 1
        if self.time >= self.lifetime:
            self.done(0)                # close after self.lifetime seconds
    
class DelayAction(Thread):

    def __init__(self,duration,*funcs,timer=None):
        """
        funcs format: [function,argument]
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
        print("timeout stopped")
        self._running = False

    def run(self):
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
    pushButton = QtWidgets.QPushButton(self)
    pushButton.setGeometry(QtCore.QRect(x, y, w, h))
    font = QtGui.QFont()
    font.setPointSize(fontsize)
    pushButton.setFont(font)
    pushButton.setObjectName(name)
    pushButton.setText(QtCore.QCoreApplication.translate("Dialog", text))
    return pushButton;

def makeMsgBox(title="This is a Title",text="This is a message",color="yellow",icon=QtWidgets.QMessageBox.Information, duration=2,fontsize=20,buttons=QtWidgets.QMessageBox.NoButton):
    msg = autoCloseMsg()
    msg.lifetime = duration
#     msgSize = msg.sizeHint()
#     print("message size:",msg.sizeHint())
#     screenW = 800
#     screenH = 400
#     msg.move(QtCore.QPoint(screenW/2-msgSize.width()/2,
#                            screenH/2-msgSize.height()/2))
    
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(buttons)
    msg.setIcon(icon)
    msg.setEscapeButton(QtWidgets.QMessageBox.Ok)
    # center the message window (autoclose was not centered by default)
    msg.setStyleSheet("font-size: "+str(fontsize)+"pt; background-color: "+str(color)+";")
    msg.exec()
    return msg
        

def makeTabLabel(self,x,y,w,h,grayscale,fontSize,name,text):
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
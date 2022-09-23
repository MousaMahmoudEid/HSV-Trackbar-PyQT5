#Models from PyQt5 library needed for ui functions loading in python code
#E:\Projects\GUI team tasks\Image processing\Image GUI
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit , QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage , QPixmap
from PyQt5 import uic
#other system libraries and opencv + numpy
import sys, time,  cv2, imutils
import numpy as np

#Class to use our UI file created by qt designer 
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("hsv_trackbar_liveCam.ui",self)
        self.show() # show the ui 

        #Get our computer camera working (port 0 can just be changed with 'IP:PORT' for ip camera)
        self.webcam = cv2.VideoCapture(0)

        #Start our timer that calls camera functions
        timer = QTimer(self)
        timer.timeout.connect(self.camera)
        timer.start(10)

    #Image processing function
    #This function needs further adjustment like blur and such to get better image quality
    #At the moment we only intigrated masking in the camera label screen due to lack of examples 
    #That uses QGraphicView related to camera
    def camera(self):
        #Sliders for HSV changing for lower limits
        minH = self.MinHSlider.value()
        minS = self.MinSSlider.value()
        minV = self.MinVSlider.value()
        #Sliders for HSV changing for upper limits
        maxH = self.MaxHSlider.value()
        maxS = self.MaxSSlider.value()
        maxV = self.MaxVSlider.value()
        
        _, imageFrame = self.webcam.read() #reading the cam have to be local
        imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_RGB2BGR) #inverting the image for final display
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) # converting to HSV for processing
        color_lower = np.array([minH, minS, minV], np.uint8) #Getting lower limits from sliders
        color_upper = np.array([maxH, maxS, maxV], np.uint8) #Getting upper liits from sliders
        color_mask = cv2.inRange(hsvFrame, color_lower, color_upper) #Masking function
        #if you want to add blur, add it here and use the hsvFrame 
        kernal = np.ones((5, 5), "uint8") 
        #Use the kernal for erosion and opening if you want to
        color_mask = cv2.dilate(color_mask, kernal) #in case of using erosion for example change color_mask to the erosion variable name
        res_color = cv2.bitwise_and(imageFrame, imageFrame, mask = color_mask) 
        #flip function, might help, might not, can just remove it and rename every frame onward to res_color
        #or just change res_color to frame for fewer editing 
        frame = cv2.flip(res_color, 1)
        #converting frame to QImage class,  only display output as RGB format or nothing will appear
        #we always convert from RGB to BGR in OpenCV because R and B channels are inverted
        #If this gives you headache just leave it as is, just tell me what you want to add
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        #Display the image in our label called MainCam
        self.MainCam.setPixmap(QPixmap.fromImage(image))
        #Print values in the terminal, using labels to display the numbers in the gui instead
        #ValueList = [minH , minS, minV, maxH, maxS, maxV]
        #print("Max = ",ValueList[0:3],"Min = ",ValueList[3:])
        minValuesHSV= f"Min HSV values = {minH} | {minS} | {minV}"
        maxValuesHSV = f"Min HSV values = {maxH} | {maxS} | {maxV}"
        self.minhsv.setText(minValuesHSV)
        self.maxhsv.setText(maxValuesHSV)


#The following lines must be places with the same order as explained here so that the program doesn't instantly close       
app = QApplication(sys.argv)
window = UI()
app.exec_()

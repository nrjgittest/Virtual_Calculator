# Virtual Calculator

import cv2
from cvzone.HandTrackingModule import HandDetector
import time
class Button:
    def __init__(self , position , width , height , value):

        self.position = position
        self.width = width
        self.height = height
        self.value = value
    def draw(self , img ):

        cv2.rectangle(img, self.position, (self.position[0] + self.width , self.position[1]+self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),(50, 50, 50), 3)
        cv2.putText(img, self.value, (self.position[0] + 40, self.position[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkclick(self , x,y):
        # x1 < x < x1+width
        if self.position[0]<x<self.position[0] + self.width and self.position[1]<x<self.position[1] + self.height:
            cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.position, (self.position[0] + self.width, self.position[1] + self.height),(50, 50, 50), 3)
            cv2.putText(img, self.value, (self.position[0] + 25, self.position[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5,(0, 0, 0), 5)
            return True
        else:
            return False

#WebCam
cap = cv2.VideoCapture(0)
cap.set(3,1280) #Width of an image
cap.set(4,720)  #Height of an image

detector = HandDetector(detectionCon=0.8 , maxHands=1) # Detection of hands

#Creating button
buttonlistvalues = [['7' , '8' , '9' , '*'] , ['4','5','6','-'] , ['1','2','3','+'] , ['0' , '/' , '.' , '=']]
buttonlist = []
for x in range (4):
    for y in range(4):
        xpos = x*100 + 800
        ypos = y*100 + 150
buttonlist.append(Button((xpos,ypos) , 100,100, buttonlistvalues[y][x]))


#Variables
myequation = ''
delaycount=0
while True:
    # Get image,from webcam
    success,img = cap.read()  # image
    img = cv2.flip(img , 1) # flipping image horizontally

    #Detection of Hands
    hands , img = detector.findHands(img , flipType=False) # Right or left hand

    # Draw all button

    cv2.rectangle(img, (800,50), (800+400 , 70+100), (225, 225, 225),cv2.FILLED)
    cv2.rectangle(img, (800,50), (800+400 , 70+100),(50, 50, 50), 3)
    for button in buttonlist:
        button.draw(img)

    # check for hand
    if hands:
        lmList = hands[0]['lmList']
        length,_,img = detector.findDistance(lmList[8] , lmList[12] , img)  #Error in this line
        x,y = lmList[8]
        if length<50:
            for i,button in enumerate(buttonlist):
                if button.checkclick(x,y) and delaycount==0:
                    myvalue = buttonlistvalues[int(i%4)][int(i/4)]
                    if myvalue== '=':
                        myequation = str(eval(myequation))  # Calculation
                    else:
                        myequation+=myvalue
                    delaycount = 1

    # Avoid Duplicates
    if delaycount!=0:
        delaycount+=1
        if delaycount>10:
            delaycount=0

    # Display the result/Equatinon
    cv2.putText(img, myequation, (810,120), cv2.FONT_HERSHEY_PLAIN, 3,(50, 50, 50), 3)

    #display image
    cv2.imshow("Image" , img)
    key = cv2.waitKey(1)
    if key==ord('c'):
        myequation = ''
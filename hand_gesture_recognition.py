import cv2 
import mediapipe as mp
from simple_gesture import simpleGesture,keyBinding,remap
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

############## Initialization ##############
cap = cv2.VideoCapture(cv2.CAP_DSHOW)

mpHands = mp.solutions.hands 
hands = mpHands.Hands(min_detection_confidence=0.80)
mpDraw = mp.solutions.drawing_utils

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin,volMax = volume.GetVolumeRange()[:2]

lms = [4,8,12,16,20]
count = 0
sgList = []
volBar = 400
############################################


while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for lm in handlandmark.landmark:
                h,w,_ = img.shape
                lmList.append([int(lm.x*w),int(lm.y*h)])
                
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

    if lmList!=[]: 
        fingers = []
        if lmList[0][1] < lmList[8][1]:
            cv2.putText(img,'Hand Gesture Not Recognisable!!',(20,50),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
        else:
            if lmList[5][0] < lmList[17][0]:
                fingers.append(True) if lmList[lms[0]][0] < lmList[lms[0]-1][0] else fingers.append(False)
            else:
                fingers.append(True) if lmList[lms[0]][0] > lmList[lms[0]-1][0] else fingers.append(False)

            for lm in range(1,len(lms)):
                fingers.append(True) if lmList[lms[lm]][1] < lmList[lms[lm]-2][1] else fingers.append(False)

            sg = simpleGesture(fingers,lmList[4],lmList[8])
            cv2.putText(img,sg,(20,50),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
            if sg=='NONE':
                pass
            elif sg=='FOUR':
                if lmList[9][0] < 320:
                    vol = remap(lmList[9][1],360,90,volMin,volMax)
                    volume.SetMasterVolumeLevel(vol, None)
                    volBar = remap(lmList[9][1],360,90,400,150,1)
            else:
                if count<640:
                    count+=32
                    cv2.rectangle(img,(0,470),(count,480),(237,149,100),-1)
                    cv2.putText(img,'Keep your hand position as it is for few seconds!',(100,440),cv2.FONT_HERSHEY_COMPLEX,0.5,(237,149,100),2)
                    sgList.append(sg)
                elif count==640:
                    count = 0
                    res = max(set(sgList), key = sgList.count)
                    sgList = []
                    if res=='INDEX':
                        if lmList[8][0] < 320:
                            keyBinding('LEFT')
                        else:
                            keyBinding('RIGHT')
                    else:        
                        keyBinding(res)
    else:
        count = 0
        sgList = []

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),-1)

    cv2.line(img,(320,0),(320,480),(237,149,100),1)
    cv2.line(img,(0,240),(640,240),(237,149,100),1)        
    cv2.imshow('Image',img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break

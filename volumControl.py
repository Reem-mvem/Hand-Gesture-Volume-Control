import cv2
import time 
import numpy as np
import handtrackingmodule as htm
import math
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume


wCam, hCam =640,480


cap= cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector =htm.handDetector(detectionconf=0.7)
   







device = AudioUtilities.GetSpeakers()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = comtypes.cast(interface, comtypes.POINTER(IAudioEndpointVolume))



#print(f"Audio output: {device.FriendlyName}")
#print(f"- Muted: {bool(volume.GetMute())}")
#print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
volRange=volume.GetVolumeRange()
#print(volRange)

minvol=volRange[0]
maxvol=volRange[1]


while True:
        
        
    success,img=cap.read()
    img=detector.findhands(img)
    lmList=detector.findpostion(img, draw=False)#becuse we already draw in findhands
    if len(lmList) !=0:

        #print(lmList[4], lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy= (x1+x2)//2, (y1+y2)//2





        cv2.circle(img,(x1,y1), 10, (255,0,255),cv2.FILLED )
        cv2.circle(img,(x2,y2), 10, (255,0,255),cv2.FILLED )
        cv2.circle(img,(cx,cy), 10, (255,0,255),cv2.FILLED )
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255))


        length=math.hypot(x2-x1, y2-y1)  
        #print(length)

        if length <=50:
            cv2.circle(img,(cx,cy), 10, (0,255,0),cv2.FILLED )


            #Hand range 50-150
            #volume range -96 - 0

        vol = np.interp(length , [50,150], [minvol,maxvol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)












    cTime =time.time()
    fps=1 / (cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)



    cv2.imshow("img", img )
    cv2.waitKey(1)
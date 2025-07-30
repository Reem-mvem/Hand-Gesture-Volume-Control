import cv2
import mediapipe as mp
import time 
class handDetector():
    def __init__(self,mode=False, Maxhands=2, detectionconf=0.5,trackconf=0.5 ):
        self.mode=mode
        self.Maxhands=Maxhands
        self.detectionconf=detectionconf
        self.trackconf=trackconf

        self.mpHands= mp.solutions.hands# acsess the hands methods in mp
        
        self.hands = self.mpHands.Hands(
    static_image_mode=self.mode,
    max_num_hands=self.Maxhands,
    min_detection_confidence=self.detectionconf,
    min_tracking_confidence=self.trackconf
)
# detect hands (hand detector)
        self.mpDraw=mp.solutions.drawing_utils



    def findhands(self,img,draw= True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)# detect hands on the RGB frame which is the cam
    #print(results.multi_hand_landmarks)


        if self.results.multi_hand_landmarks:# if it contains hands 
          for singlehand in self.results.multi_hand_landmarks:
             if draw:
                 
                self.mpDraw.draw_landmarks(img,singlehand,self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findpostion(self, img, handNo=0, draw=True):
           limList=[]
           if self.results.multi_hand_landmarks:
             myHand = self.results.multi_hand_landmarks[handNo]# we can find the postion of spicific hand 

             for id ,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,_=img.shape
                cx,cy=int(lm.x*w), int(lm .y*h)
            
                limList.append([id,cx,cy])
                if draw:
                     cv2.circle(img, (cx,cy), 7, (255,0,0),cv2.FILLED )
           return limList



    
    
    

def main():
    pTime=0
    cTime=0
    cap=cv2.VideoCapture(0)
    detector= handDetector()


    while True:
        success,img=cap.read()
        img= detector.findhands(img)
        limList=detector.findpostion(img)
        if len(limList) !=0:
           print(limList[4])# the tip of the thump
      

        cTime=time.time()
        fps=int(1/(cTime-pTime))#frame per second 
        pTime=cTime  
        cv2.putText(img,str(fps),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)

        cv2.imshow("image",img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()
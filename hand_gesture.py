import cv2
import mediapipe as mp
font = cv2.FONT_HERSHEY_SIMPLEX

import math
def ang(a,b,c):
    x1,y1  = a[0],a[1]
    x2,y2 = b[0],b[1]
    x3,y3 = c[0],c[1]
    if x1 != x2 and x2 != x3:
        m1 = (y1-y2)/(x1-x2)
        m2 = (y3-y2)/(x3-x2)
        if m1*m2 != -1:
            angle = math.atan(abs((m1-m2)/(1+m1*m2)))
            angle = angle * (180) / (math.pi)
        elif m1*m2 == -1:
            angle = 90
        return angle
def dis(a,b):
    x1,y1 = a[0],a[1]
    x2,y2 = b[0],b[1]
    d = (x1-x2)**2 + (y1-y2)**2
    d = d**(0.5)
    return d
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands = 2,
                       min_detection_confidence = 0.5,
                       min_tracking_confidence = 0.5)

while True:
    success,frame = cap.read()

    if not success :
         break
    frame = cv2.flip(frame,1)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(frame)

    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
    out = '....'
    if results.multi_hand_landmarks is not None:

        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = frame.shape
            hand_features = []
            for landmark in hand_landmarks.landmark:
                hand_features.append(int(landmark.x*w))
                hand_features.append(h-int(landmark.y*h))
            wrist = hand_features[0:2]
            thumbcmc = hand_features[2:4]
            thumbmcp = hand_features[4:6]
            thumbip = hand_features[6:8]
            thumbtip = hand_features[8:10]
            indexmcp = hand_features[10:12]
            indexpip = hand_features[12:14]
            indexdip = hand_features[14:16]
            indextip = hand_features[16:18]
            midmcp = hand_features[18:20]
            midpip = hand_features[20:22]
            middip = hand_features[22:24]
            midtip = hand_features[24:26]
            ringmcp = hand_features[26:28]
            ringpip = hand_features[28:30]
            ringdip = hand_features[30:32]
            ringtip = hand_features[32:34]
            pinkymcp = hand_features[34:36]
            pinkypip = hand_features[36:38]
            pinkydip = hand_features[38:40]
            pinkytip = hand_features[40:42]

            thumbangle = ang(thumbtip,thumbmcp,indexmcp)
            d1 = dis(wrist,midtip)
            d2 = dis(thumbtip,indextip)
            out = '....'
            if thumbangle is None:
                out = '....'

            elif thumbangle >= 50 and d1 < 180:
                if indextip[1] - ringtip[1] > 30:
                    out = 'UP'
                elif ringtip[1] - indextip[1] > 30:
                    out = 'DOWN'
                elif indextip[0] - ringtip[0] > 30:
                    out = 'RIGHT'
                elif ringtip[0] - indextip[0] > 30:
                    out = 'LEFT'
            else:
                if d1 < 220 and d2 < 60:
                    out = 'BACKWARD'
                elif midtip[1] > indextip[1] and d2 > 50:
                    out = 'FORWARD'


    cv2.putText(frame,out,(50,50),font,1,(0,100,255),5)
    cv2.imshow('HAND GESTURES',frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
         break
cap.release()
cv2.destroyAllWindows()










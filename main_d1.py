# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 10:44:37 2022

@author: E
"""

#ライブラリのインポート
import cv2
import numpy as np
import random

files = []
files_2 = []
z = 0
clearframe = 0
frameRate = 0
second = 10
is_clear = False
length = 0

def createOutline(img_sample, img_origin):
    # TODO: 消去
    img_sample = cv2.resize(img_sample, dsize = (640, 480))
    #img_sample = cv2.bitwise_not(img_sample)
    img_gray = cv2.cvtColor(img_sample, cv2.COLOR_BGR2GRAY)
    cv2.imshow("createOutput_debug_1", img_gray)
    ret, img_binary = cv2.threshold(img_gray, 1, 255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_with_outline = cv2.drawContours(img_origin, contours, -1, (0, 255, 0), 5)
    return img_with_outline

def createrandom():
    return random.randrange(len(files))


# 画像にテキストをつける関数
def putText(img, text, x, y):
    cv2.putText(
            img,
            text,
            (x, y),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (0, 255, 0),
            2,
        )
    
    
def framecount(f):
    return f + 1

#1枚
img1 = cv2.imread('./data/pose/pose1.png')
img1 = cv2.bitwise_not(img1)
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)


for n in range(1, 11):
    img = cv2.imread("./data/pose/pose"+str(n)+".png")
    img = cv2.bitwise_not(img)
    files_2.append(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("createOutput_debug_1", gray)
    ret, change = cv2.threshold(gray, 1, 255,cv2.THRESH_BINARY)
    # TODO: 消去
    change2 = cv2.resize(change, dsize = (640, 480))
    files.append(change2)

cap = cv2.VideoCapture(0)
screenshot = False
photo = None
#cv2.imshow("debug_a",gray)
createrandom()
'''
img2 = cv2.threshold(img1, 100, 255, cv2.THRESH_BINARY)

'''   

#cv2.imshow("sample", img2)
img2 = files[z]
cv2.imshow("img2debug",img2)
img3 = files_2[z]
y = np.sum(img2) / 255


#無限ループで差分をとる
while True:    
    ret,frame = cap.read()
    cv2.putText(frame, 'progress', (140, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    cv2.rectangle(frame, (140, 30), (500, 60), (255, 255, 255), thickness=2)
    # スクショがあるなら差分を出力
    if screenshot:
        # 背景差分のクラスを定義(リセット)
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        # 背景画像を指定(スクショ)
        background = fgbg.apply(photo)
        # 差分画像(カメラの入力フレーム)
        fgmask = fgbg.apply(frame)
        
        mask_tfout = fgmask - img2
        cv2.imshow("flow1", mask_tfout)
        
        mask_tfin = np.abs(img2 - fgmask)
        #cv2.imshow("debug", photo)
        cv2.imshow("flow2", mask_tfin)
        out_number = np.sum(mask_tfout)
        in_number = np.sum(mask_tfin)
        x = (out_number + in_number) / 255
        # 経過秒数のカウント
        frameRate += 1
    
        if int(frameRate) % cap.get(cv2.CAP_PROP_FPS) == 0:
            second -= 1
        putText(frame, str(int(second)), 0, 50)
        createOutline(img3, frame)
        
    
        #判定
        if 0.80 >= x / (y):
            clearframe += 1
            print(clearframe)
            #cv2.rectangle(frame, (142,32), ())
            
            if clearframe >= 90:
                print("clear")
                z = createrandom()
                img2 = files[z]
                img3 = files_2[z]
                y = np.sum(img2) / 255
                clearframe = 0
                second = 10
                #print(z)
        elif 0.80 <= x / (y) and clearframe > 0:
            clearframe -= 1
        
        #timeout
        if second == 0:
            print("failure")
            z = createrandom()
            img2 = files[z]
            img3 = files_2[z]
            y = np.sum(img2) / 255
            clearframe = 0
            second = 20
        length = 140 + (500 - 140)*clearframe/90
        cv2.rectangle(frame, (140, 30), (int(length), 60), (255, 255, 255), thickness=-1)
    
    #text = "{}{:.0f}{}".format(clearframe)
    #cv2.putText(frame, text, (150, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    
    cv2.imshow("output",frame)
    
        
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    # フレームを保存 (スクショ)
    elif k == ord("s"):
        photo = frame
        screenshot = True
    elif k == ord("r"):
        z = createrandom()
        img2 = files[z]
        img3 = files_2[z]
        y = np.sum(img2) / 255
        print(z)
        mask_tfout = 0
              
#ポーズ画像と比較

#一致したら次のポーズに映る
 
    
 
#終了


cap.release()
cv2.destroyAllWindows()

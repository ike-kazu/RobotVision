# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 10:44:37 2022

@author: E
"""

#ライブラリのインポート
import cv2
import numpy as np

def createOutline(img_sample, img_origin):
    # TODO: 消去
    img_sample = cv2.resize(img_sample, dsize = (640, 480))
    img_gray = cv2.cvtColor(img_sample, cv2.COLOR_BGR2GRAY)
    ret, img_binary = cv2.threshold(img_gray, 1, 255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_with_outline = cv2.drawContours(img_origin, contours, -1, (0, 255, 0), 5)
    return img_with_outline

img1 = cv2.imread('./data/sample/Reyna.png')
gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
cap = cv2.VideoCapture(0)
screenshot = False
photo = None
'''
img2 = cv2.threshold(img1, 100, 255, cv2.THRESH_BINARY)

'''
hsvLower = np.array([0, 0, 30])  # 下限
hsvUpper = np.array([179, 255, 255])  # 上限
hsv_mask = cv2.inRange(img1, hsvLower, hsvUpper)
# TODO: 消去
img2 = cv2.resize(hsv_mask, dsize = (640, 480))
cv2.imshow("sample", img2)


#無限ループで差分をとる
while True:
    
    ret,frame = cap.read()
    # スクショがあるなら差分を出力
    if screenshot:
        # 背景差分のクラスを定義(リセット)
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        # 背景画像を指定(スクショ)
        background = fgbg.apply(photo)
        # 差分画像(カメラの入力フレーム)
        fgmask = fgbg.apply(frame)
        
        mask_tfout = fgmask - img2
        cv2.imshow("flow1",mask_tfout)
        
        mask_tfin = np.abs(img2 - fgmask)
        cv2.imshow("flow2", mask_tfin)
        out_number = np.sum(mask_tfout)
        in_number = np.sum(mask_tfin)
        x = out_number + in_number
        print(type(mask_tfin))
        #判定
        if x <= 40000000:
            print("hello")
    
    createOutline(img1, frame)
    cv2.imshow("output",frame)
        
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    # フレームを保存 (スクショ)
    elif k == ord("s"):
        photo = frame
        screenshot = True

#ポーズ画像と比較

#一致したら次のポーズに映る
 
    
 
#終了


cap.release()
cv2.destroyAllWindows()

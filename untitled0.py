# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 10:44:37 2022

@author: E
"""

#ライブラリのインポート
import cv2
import numpy as np

img1 = cv2.imread('reyna2.png')
gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
cap = cv2.VideoCapture(0)
screenshot = False
photo = None
'''
img2 = cv2.threshold(img1, 100, 255, cv2.THRESH_BINARY)

'''
hsvLower = np.array([0, 0, 0])  # 下限
hsvUpper = np.array([179, 255, 255])  # 上限
hsv_mask = cv2.inRange(img1, hsvLower, hsvUpper)
img2 = cv2.resize(hsv_mask, dsize = (640, 480))
cv2.imshow("sample", img2)


#無限ループで差分をとる
while True:
    
    ret,frame = cap.read()
    cv2.imshow("output",frame)
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
        mask_tfin = img2 - fgmask
        cv2.imshow("flow2", mask_tfin)
        out_number = np.sum(mask_tfout)
        in_number = np.sum(mask_tfin)
        x = out_number + in_number
        #判定
        if x <= 40000000:
            print("hello")
        
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

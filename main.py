import cv2
import numpy as np
from skimage.feature import hog
from sklearn.neighbors import NearestNeighbors

cap = cv2.VideoCapture(0)

# 実行
while True:
    
    # Webカメラのフレーム取得
    ret, frame = cap.read() 
    cv2.putText(
        src, display_str, (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 1,
    )
    cv2.imshow("camera", frame)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("q"):
        break


# カメラリリース、windowの開放
cap.release()
cv2.destroyAllWindows()

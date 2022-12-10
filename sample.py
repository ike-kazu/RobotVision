# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:45:21 2022

@author: E
"""

import cv2
import numpy as np
from skimage.feature import hog
from sklearn.neighbors import NearestNeighbors

img_sample = cv2.imread("./data/sample/Phx.png", 1)

# 画像をこの関数に入れると
def createOutline(img_sample):
    img_bit = cv2.bitwise_not(img_sample)
    img_gray = cv2.cvtColor(img_bit, cv2.COLOR_BGR2GRAY)
    img_gray =  cv2.bitwise_not(img_gray)
    ret, img_binary = cv2.threshold(img_gray, 1, 255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_with_outline = cv2.drawContours(img_sample, contours, -1, (0, 255, 0), 5)
    return img_with_outline
    
img_with_outline = createOutline(img_sample)
cv2.imshow("outline", img_with_outline)
cv2.waitKey(0)

cv2.destroyAllWindows()
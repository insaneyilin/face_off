# -*- coding: utf-8 -*-
# @Author: yilin
# @Date:   2019-07-21 20:18:50
# Python version: 2.7

import cv2
import face_tracker

facetracker = face_tracker.FaceTracker()

img = cv2.imread('data/images/lena.jpg')

facetracker.update(img)

img_face = img.copy()
for face in facetracker.faces:
    print face.face_rect
    x, y, w, h = face.face_rect
    cv2.rectangle(img_face, (x,y), (x+w,y+h), (0,255,0), 2)

cv2.imshow('image', img)
cv2.imshow('image_face', img_face)
cv2.waitKey()

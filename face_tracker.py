# -*- coding: utf-8 -*-
# @Author: yilin
# @Date:   2019-07-21 19:07:17
# Python version: 2.7

import numpy as np
import cv2
import utils


class Face(object):

    def __init__(self):
        self.face_rect = None
        self.left_eye_rect = None
        self.right_eye_rect = None
        self.nose_rect = None
        self.mouse_rect = None


class FaceTracker(object):

    def __init__(self, scale_factor=1.2, min_neighbors=2,
            detect_flags=cv2.CASCADE_DO_CANNY_PRUNING):
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.detect_flags = detect_flags

        self._faces = []
        self._face_classifier = cv2.CascadeClassifier(
            'data/haarcascades/haarcascade_frontalface_alt2.xml')
        self._eye_classifier = cv2.CascadeClassifier(
            'data/haarcascades/haarcascade_eye.xml')
        self._nose_classifier = cv2.CascadeClassifier(
            'data/haarcascades/haarcascade_mcs_nose.xml')
        self._mouth_classifier = cv2.CascadeClassifier(
            'data/haarcascades/haarcascade_mcs_mouth.xml')


    @property
    def faces(self):
        return self._faces


    def update(self, image):
        if image is None:
            return
        self._faces = []
        if utils.is_gray_image(image):
            image = cv2.equalizeHist(image)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.equalizeHist(image)

        min_size = utils.width_height_divide_by(image, 8)
        face_rects = self._face_classifier.detectMultiScale(
                image, self.scale_factor, self.min_neighbors,
                self.detect_flags, min_size)

        if face_rects is None:
            return

        for face_rect in face_rects:
            face = Face()
            face.face_rect = face_rect
            x, y, w, h = face_rect

            # Seek an eye in the upper-left part of the face.
            search_rect = (x+w/7, y, w*2/7, h/2)
            face.left_eye_rect = self._detect_one_object(
                    self._eye_classifier, image, search_rect, 64)

            # Seek an eye in the upper-right part of the face.
            search_rect = (x+w*4/7, y, w*2/7, h/2)
            face.right_eye_rect = self._detect_one_object(
                    self._eye_classifier, image, search_rect, 64)

            # Seek a nose in the middle part of the face.
            search_rect = (x+w/4, y+h/4, w/2, h/2)
            face.nose_rect = self._detect_one_object(
                    self._nose_classifier, image, search_rect, 64)

            # Seek a mouth in the lower-middle part of the face.
            search_rect = (x+w/6, y+h*2/3, w*2/3, h/3)
            face.nose_rect = self._detect_one_object(
                    self._mouth_classifier, image, search_rect, 64)

            # append new face
            self._faces.append(face)


    def _detect_one_object(self, classifier, image, rect,
            image_size_to_min_size_ratio):
        x, y, w, h = rect
        min_size = utils.width_height_divide_by(
            image, image_size_to_min_size_ratio)
        sub_image = image[y:y+h, x:x+w]
        sub_rects = classifier.detectMultiScale(
            sub_image, self.scale_factor, self.min_neighbors,
            self.detect_flags, min_size)
        if len(sub_rects) == 0:
            return None

        sub_x, sub_y, sub_w, sub_h = sub_rects[0]
        return (x+sub_x, y+sub_y, sub_w, sub_h)

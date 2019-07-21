# -*- coding: utf-8 -*-
# @Author: yilin
# @Date:   2019-07-21 19:07:17
# Python version: 2.7

import cv2
import numpy as np
from window_manager import WindowManager
from capture_manager import CaptureManager
from face_tracker import Face
from face_tracker import FaceTracker


class VideoCaptureApp(object):

    def __init__(self, face_img_path=None, should_mirror=False):
        self._window_manager = WindowManager(self.on_keypress)
        self._capture_manager = CaptureManager(cv2.VideoCapture(0))
        self._window_name = 'FaceOff'
        self._should_mirror = should_mirror
        self._face_tracker = FaceTracker()
        self._show_face_rect = True
        self._swap_face = False
        self._template_face = None
        if face_img_path is not None:
            self._template_face = cv2.imread(face_img_path)


    def run(self):
        self._window_manager.create_window(self._window_name)
        while self._window_manager.is_window_created(self._window_name):
            self._capture_manager.enter_frame()
            frame = self._capture_manager.frame

            # process frame
            # detect face
            self._face_tracker.update(frame)
            face_num = len(self._face_tracker.faces)
            face_rect = None if face_num == 0 else \
                    self._face_tracker.faces[0].face_rect
            if self._show_face_rect:
                txt_str = 'face_num: {}'.format(face_num)
                for face in self._face_tracker.faces:
                    x, y, w, h = face.face_rect
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    # only show the 1st face
                    break

            if face_rect is not None and self._swap_face and \
                    self._template_face is not None:
                x, y, w, h = face_rect
                template_face = self._template_face.copy()
                template_face = cv2.resize(template_face, (w,h))
                frame[y:y+h,x:x+w] = template_face

            # show frame window
            if self._should_mirror:
                # horizontal flipping
                frame = cv2.flip(frame, 1)
            # draw text
            if self._show_face_rect:
                cv2.putText(frame, txt_str, (50,100), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0,255,0), 2)
            self._window_manager.show_window(self._window_name, frame)

            self._capture_manager.exit_frame()
            self._window_manager.process_event()


    def on_keypress(self, keycode):
        if keycode == ord('m'):
            self._should_mirror = not self._should_mirror
        elif keycode == ord('s'):
            self._swap_face = not self._swap_face
        elif keycode == ord('f'):
            self._show_face_rect = not self._show_face_rect
        elif keycode == 27:
            # Escape
            self._window_manager.destroy_all_window()

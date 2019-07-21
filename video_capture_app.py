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

    def __init__(self, should_mirror=False):
        self._window_manager = WindowManager(self.on_keypress)
        self._capture_manager = CaptureManager(cv2.VideoCapture(0))
        self._window_name = 'FaceOff'
        self._should_mirror = should_mirror
        self._face_tracker = FaceTracker()
        self._show_face_rect = True


    def run(self):
        self._window_manager.create_window(self._window_name)
        while self._window_manager.is_window_created(self._window_name):
            self._capture_manager.enter_frame()
            frame = self._capture_manager.frame

            # process frame
            # detect face
            self._face_tracker.update(frame)
            face_num = len(self._face_tracker.faces)
            if self._show_face_rect:
                txt_str = 'face_num: {}'.format(face_num)
                for face in self._face_tracker.faces:
                    x, y, w, h = face.face_rect
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    # only show the 1st face
                    break

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
        elif keycode == ord('f'):
            self._show_face_rect = not self._show_face_rect
        elif keycode == 27:
            # Escape
            self._window_manager.destroy_all_window()

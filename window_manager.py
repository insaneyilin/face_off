# -*- coding: utf-8 -*-
# @Author: yilin
# @Date:   2019-07-21 18:38:41
# Python version: 2.7

import numpy as np
import cv2


class WindowManager(object):
    def __init__(self, key_pressdown_callback=None):
        self._window_name_dict = {}
        self.key_pressdown_callback = key_pressdown_callback


    def is_window_created(self, window_name):
        if window_name in self._window_name_dict:
            return self._window_name_dict[window_name]
        return False


    def create_window(self, window_name):
        cv2.namedWindow(window_name)
        cv2.moveWindow(window_name, 100, 50)
        self._window_name_dict[window_name] = True


    def show_window(self, window_name, frame):
        if not window_name in self._window_name_dict or\
                not self._window_name_dict[window_name]:
            return
        cv2.imshow(window_name, frame)


    def destroy_window(self, window_name):
        cv2.destroyWindow(window_name)
        self._window_name_dict[window_name] = False


    def destroy_all_window(self):
        cv2.destroyAllWindows()
        for win_name in self._window_name_dict:
            self._window_name_dict[win_name] = False


    def process_event(self):
        keycode = cv2.waitKey(1)
        if self.key_pressdown_callback is not None and keycode != -1:
            self.key_pressdown_callback(keycode)

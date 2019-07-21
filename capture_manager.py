# -*- coding: utf-8 -*-
# @Author: yilin
# @Date:   2019-07-21 18:38:41
# Python version: 2.7

import cv2


class CaptureManager(object):

    def __init__(self, capture):
        self._capture = capture
        self._frame = None
        self._is_entered_frame = False


    @property
    def frame(self):
        if self._is_entered_frame and self._frame is None:
            _, self._frame = self._capture.retrieve()
        return self._frame


    def enter_frame(self):
        """
        Capture the next fame, if any
        """
        assert not self._is_entered_frame, \
            'previous enter_frame() had no matching exit_frame()'

        if self._capture is not None:
            self._is_entered_frame = self._capture.grab()


    def exit_frame(self):
        """
        Draw to the window. / Write to file.
        Release the frame.
        """
        if self.frame is None:
            self._is_entered_frame = False
            return

        # TODO: write to file

        # Release the frame.
        self._frame = None
        self._is_entered_frame = False

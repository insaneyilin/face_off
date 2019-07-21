# -*- coding: utf-8 -*-
# @Author: yilin
# @Date:   2019-07-21 19:07:17
# Python version: 2.7

import numpy as np
import cv2


def is_gray_image(image):
    return image.ndim == 1


def width_height_divide_by(image, divisor):
    h, w = image.shape[:2]
    return w/divisor, h/divisor

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Make noisy image  """

import argparse
import numpy as np
import cv2

__autor__ = 'Kyosuke Yamamoto (kyon)'
__date__ = '22 Dec 2016'

if __name__ == '__main__':

    #argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='+', type=str, help='path to images')
    args = parser.parse_args()

    #init
    method = cv2.INTER_CUBIC

    #main
    for imgpath in args.path:
        im = cv2.imread(imgpath, 3)
        mini_img = cv2.resize(im, (im.shape[1]/2, im.shape[0]/2), interpolation=method)
        gaus_img = cv2.GaussianBlur(mini_img, (3, 3), sigmaX=1, sigmaY=1)
        noisy_img = cv2.resize(gaus_img, (im.shape[1], im.shape[0]), interpolation=method)
        noisy_img = noisy_img.astype(np.uint8)
        cv2.imwrite(imgpath, noisy_img)
        print 'saved as', imgpath

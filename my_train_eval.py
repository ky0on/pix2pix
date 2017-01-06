#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""   """

from __future__ import print_function
import sys
sys.path.append('../..')
import cv2
import shutil
import argparse
import subprocess
from os.path import basename, join, splitext
from common import make_noisy

__autor__ = 'Kyosuke Yamamoto (kyon)'
__date__ = '01 Jan 2017'


def set_images(images, dtype):
    ''' Copy train/val images '''

    #assert
    if dtype not in ('train', 'val'):
        raise Exception('unknown dtype ' + dtype)

    #copy images
    for src in images:
        src = join(args.base, src)
        fn, ext = splitext(basename(src))
        im = cv2.imread(src, 3)

        #noisy image
        noisy = make_noisy(im)
        blocks = blockshaped(noisy, size, size)
        for i, block in enumerate(blocks):
            dst = join(args.dst, 'A', dtype, '{}_{}{}'.format(fn, i, ext))
            cv2.imwrite(dst, block)
            print(src, '->', dst)

        #original image
        blocks = blockshaped(im, size, size)
        for i, block in enumerate(blocks):
            dst = join(args.dst, 'B', dtype, '{}_{}{}'.format(fn, i, ext))
            cv2.imwrite(dst, block)
            print(src, '->', dst)


def blockshaped(arr, nrows, ncols):
    ''' Split arr into blocks with same shapes
    http://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays '''

    h, w, d = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols, 3)
            .swapaxes(1, 2)
            .reshape(-1, nrows, ncols, 3))


if __name__ == '__main__':

    #argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', '-t', default='../../dataset/row/20_512/train.csv', help='path to list of training images')
    parser.add_argument('--eval', '-e', default='../../dataset/row/20_512/eval.csv', help='path to list of evaluation images')
    parser.add_argument('--base', default='../../', help='path to image dir')
    parser.add_argument('--dst', default='datasets/row')
    parser.add_argument('--epoch', type=int, default=500)
    args = parser.parse_args()

    #param
    size = 256    # input size to pix2pix

    #init
    for t1 in ('A', 'B'):
        for t2 in ('train', 'val'):
            subprocess.check_call('mkdir -p {}/{}/{}'.format(args.dst, t1, t2), shell=True)

    #images for training/validation
    with open(args.train) as f:
        train_images = f.read().splitlines()
    with open(args.eval) as f:
        val_images = f.read().splitlines()

    #copy train images
    set_images(train_images, 'train')
    set_images(train_images + val_images, 'val')

    #combine
    cmd = 'python scripts/combine_A_and_B.py \
        --fold_A {} --fold_B {} --fold_AB {}'.format(join(args.dst, 'A'), join(args.dst, 'B'), args.dst)
    subprocess.check_call(cmd, shell=True)

    #train
    # cmd = 'DATA_ROOT={} name=row which_direction=AtoB niter={} th train.lua'.format(args.dst, args.epoch)
    # print('running', cmd)
    # subprocess.check_call(cmd, shell=True)

    #eval
    # cmd = 'DATA_ROOT={} name=row which_direction=AtoB which_epoch={} th test.lua'.format(args.dst, args.epoch)
    # print('running', cmd)
    # subprocess.check_call(cmd, shell=True)

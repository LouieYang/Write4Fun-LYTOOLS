# Copyright @2016
# LouieYang <lyng_95@zju.edu.cn>
# 
# https://github.com/LouieYang/Write4Fun-LYTOOLS
#
# Convert gifs to separate frame images
#
from PIL import Image
import json
import sys
import time
import argparse
import os

def simple_alpha_composite(bottom, top):
    """
        Thanks to Kris Kowal answers to http://stackoverflow.com/questions/3374878/
    """
    r, g, b, a = top.split()
    top = Image.merge("RGB", (r, g, b))
    mask = Image.merge("L", (a, ))
    bottom.paste(top, (0, 0), mask)
    return bottom

def gif2im(gif_file, save_dir):
    
    if not gif_file.endswith('.gif'):
        print "Cant processing file format that is not GIF"
        return

    try:
        im = Image.open(gif_file)
    except IOError:
        print "Cant load ", gif_file
        raise

    im_name = gif_file[:-4]
    folder_new = save_dir + '/' + im_name
    try:
        os.makedirs(folder_new)
    except OSError:
        # if file already exists, create another folder with time info
        folder_new += time.strftime('-%YY%mM%dD%HH%MM%SS',time.localtime(time.time()))
        os.makedirs(folder_new)
        time.sleep(1)
    idx = 0
    try:
        imframe = im.convert('RGBA')

        while True:
            imframe.save(folder_new + '/' + str(idx) + '.png')
            im.seek(im.tell() + 1)
            imframe = simple_alpha_composite(imframe, im.convert('RGBA'))
            idx += 1
    except EOFError:
        pass

    return (idx, folder_new)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--gif_file', default = '', help = 'gif file that want to transform')
    parser.add_argument('--save_dir', default = 'gif-frames', help = 'the root of transformed image stored')
    parser.add_argument('--batch_gif_dirs', default = '', help = 'text stores batches of gifs to be transformed')

    args = parser.parse_args()
    params = vars(args)
    print 'parsed input parameters:'
    print json.dumps(params, indent = 2)

    if params['gif_file']:
        try:
            count, folder = gif2im(params['gif_file'], params['save_dir'])
            print 'converted {0} to {1} png images and store in {2}'.format(params['gif_file'], count, folder)
        except IOError:
            print 'convert {0} failed'.format(params['gif_file'])
            pass

    if params['batch_gif_dirs']:
        batch_dirs = open(params['batch_gif_dirs'], 'r')
        lines = batch_dirs.readlines()

        for line in lines:
            line = line[:-1]
            if not line:
                break

            try:
                if line.endswith('\n'):
                    line = line[:-1]
                count, folder = gif2im(line, params['save_dir'])
                print 'converted {0} to {1} png images and store in {2}'.format(line, count, folder)
            except IOError:
                print 'convert {0} failed'.format(params['gif_file'])
                pass



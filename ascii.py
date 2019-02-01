# coding=utf-8
from bearlibterminal import terminal as blt
import sys
import os
from PIL import Image
import numpy as np
import random
from matplotlib import pyplot as plt


width = 380
height = 110
cell_width = 5
cell_height = 9

font_name = "Media/VeraMono.ttf"
font_size = 7
font_hintings = ["normal", "autohint", "none"]
font_hinting = 0

exit = False


def convert_pixel_val(pixel_val):
    #pixel_val = 255 - pixel_val

    char_list = [(".", "'", "´", ","), (":", ";", '"', "-", "~", "_"), ("<", ">", "+", "*", "i", "/", "\\", "(", ")"),
                 ("o", "a", "e", "5", "p", "d"), ("&", "#", "§", "8", "ß", "@")]

    if(pixel_val < 10):
        return " "
    else:
        idx = pixel_val//(int((255-10)/len(char_list)))
        if idx > len(char_list) - 1:
            idx = len(char_list) - 1
        return random.choice(char_list[idx])

def convert_row(row):
    ascii_row = ""
    for i in range(row.shape[0]):
        ascii_row += "[color=%d]"+convert_pixel_val(row[i])+"[/color]"
    return ascii_row

def color_from_rgb(col):
    if type(col) is np.ndarray:
        result = '0xff%02x%02x%02x' % (col[0], col[1], col[2])
    else:
        result = '0xff%02x%02x%02x' % (col, col, col)
    return int(result,0)

def load_and_preprocess(img_path):
    global width
    global height
    img = Image.open(im_path)
    size = img.size

    resize_ratio = min(width / (size[0] * cell_height / cell_width), height / size[1])
    img = img.resize((int(size[0] * resize_ratio * cell_height / cell_width), int(size[1] * resize_ratio)))
    size = img.size
    width = size[0]
    height = size[1]
    tmp = np.array(img)

    gray_scale = False

    if len(tmp.shape) > 2:
        grey = (np.add.reduce(np.array(img), 2)/3).astype(np.uint8)
    else:
        gray_scale = True
        grey = tmp

    col = np.zeros(grey.shape, dtype=np.uint32)
    for (i,j), _ in np.ndenumerate(col):
        if gray_scale:
            col[i, j] = color_from_rgb(tmp[i, j])
        else:
            col[i,j] = color_from_rgb(tmp[i,j,:])

    return col, grey

def plot_image(img, grey=False):
    if grey:
        plt.imshow(img, cmap="gray")
        plt.show()
    else:
        plt.imshow(img)
        plt.show()

def handle_key_presses(key):
    global exit
    if key in (blt.TK_CLOSE, blt.TK_ESCAPE):
        exit = True
        return

def setup_font():
    global font_name
    global font_size
    global font_hintings
    global font_hinting
    blt.set("font: %s, size=%d, hinting=%s" % (font_name, font_size, font_hintings[font_hinting]))
def setup_cellsize():
    global cell_height
    global cell_width
    blt.set("window: cellsize=%dx%d" % (cell_width, cell_height))

def setup_terminal():
    blt.open()
    blt.set("window: size=%dx%d, cellsize=auto, title='ASCII'" % (width, height))
    setup_cellsize()
    setup_font()
    blt.refresh()






if __name__ == "__main__":
    [_, im_path] = sys.argv
    color, grey = load_and_preprocess(im_path)

    setup_terminal()
    while not exit:
        blt.clear()
        blt.color("white")

        for i in range(grey.shape[0]):
            row = convert_row(grey[i,:])
            blt.puts(0, i, row % tuple(color[i,:]))
        blt.refresh()

        handle_key_presses(blt.read())

    blt.close()



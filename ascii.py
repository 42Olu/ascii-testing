# coding=utf-8

from bearlibterminal import terminal as blt

width = 240
height =110
cell_width = 6
cell_height = 8

font_name = "Media/VeraMono.ttf"
font_size = 7
font_hintings = ["normal", "autohint", "none"]
font_hinting = 0

exit = False

def check_key_presses(key):
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

if __name__ == "__main__":
    blt.open()
    blt.set("window: size=%dx%d, cellsize=auto, title='ASCII' font: default" % (width, height))
    setup_cellsize()
    setup_font()
    blt.refresh()

    while not exit:
        blt.clear()
        blt.color("white")

        blt.puts(2, 1, "Hello, world!")
        blt.puts(1, 2, "[color=orange]Font size:[/color] %d" % font_size)
        blt.puts(0, 3, "[color=orange]Cell size:[/color] %dx%d" % (cell_width, cell_height))
        blt.refresh()

        check_key_presses(blt.read())

    blt.close()
from collections import Iterable

from PIL import Image
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm

from pagesizes import pagesizes
from skinmap import Face, skinmap, unit


def __load_pixelmap__(filename):
    skin = Image.open(filename)
    data = list(skin.getdata())
    return [data[n * 64:(n + 1) * 64] for n in range(64)]


class SkinUtils:

    def __init__(self, pixelmap, pdf_file_name, mob_name='',
                 pdf_pagesize='A4', pdf_landscape=False,
                 pdf_left_bound=10, pdf_top_bound=10,
                 grid_size=5,
                 dash_grid=False,
                 pdf_face_padding=3, pdf_part_padding=15,
                 face_flip_horizontally=False,
                 place_mask_on_head=True):
        self.pixelmap = __load_pixelmap__(pixelmap) if isinstance(pixelmap, str) else pixelmap
        if (not isinstance(self.pixelmap, Iterable)) or\
                (len(self.pixelmap) != 64) or\
                (len(min(self.pixelmap, key=len)) < 64):
            raise Exception("Invalid skin pixelmap")

        self.pdf_file_name = pdf_file_name
        self.mob_name = mob_name
        self.pdf_pagesize = pagesizes[pdf_pagesize] if not pdf_landscape else landscape(pagesizes[pdf_pagesize])
        self.pdf_left_bound = pdf_left_bound * mm
        self.pdf_top_bound = pdf_top_bound * mm
        self.grid_size = grid_size * mm
        self.dash_grid = dash_grid
        self.pdf_face_padding = pdf_face_padding * mm
        self.pdf_part_padding = pdf_part_padding * mm
        self.face_flip_horizontally = face_flip_horizontally
        self.place_mask_on_head = place_mask_on_head
        self.pdf_left, self.pdf_top = self.pdf_left_bound, self.pdf_pagesize[1] - self.pdf_top_bound
        self.current_xpos, self.current_ypos = self.pdf_left, self.pdf_top

        min_bound_part = min(skinmap.values(), key=lambda p: self.get_bound_rect(p)[0] * self.get_bound_rect(p)[1])
        self.min_bound_rect = self.get_bound_rect(min_bound_part)

        self.canvas = Canvas(pdf_file_name, pagesize=self.pdf_pagesize)
        self.old_y_size = 0

    def get_pixelmap(self, face: Face):
        return [self.pixelmap[y][face.x * unit:face.x * unit + face.dx * unit]
                for y in range(face.y * unit, face.y * unit + face.dy * unit)]

    def draw_face_grid(self, face: Face, current_x, current_y, transparent=False):
        pixelmap = self.get_pixelmap(face)
        xs = current_x + face.xpos * unit * self.grid_size + face.xpos / 2 * self.pdf_face_padding
        ys = current_y - face.ypos * unit * self.grid_size - face.ypos / 2 * self.pdf_face_padding

        for dy, line in enumerate(pixelmap):
            line = line if not self.face_flip_horizontally else line[::-1]
            for dx, dot in enumerate(line):
                x = xs + dx * self.grid_size
                y = ys - dy * self.grid_size
                if dot[3] > 0:
                    self.canvas.setStrokeColorRGB(dot[0] / 255, dot[1] / 255, dot[2] / 255, 1)
                    self.canvas.setFillColorRGB(dot[0] / 255, dot[1] / 255, dot[2] / 255, 1)
                    self.canvas.rect(x, y, self.grid_size, -self.grid_size, False, True)
                elif not transparent:
                    self.canvas.setFillColorRGB(0.85, 0.85, 0.85, 0)
                    self.canvas.rect(x, y, self.grid_size / 2, -self.grid_size / 2, False, True)
                    self.canvas.rect(x + self.grid_size / 2, y - self.grid_size / 2, self.grid_size / 2,
                                     -self.grid_size / 2, False,
                                     True)

        rows = range(len(pixelmap) + 1)
        cols = range(len(pixelmap[0]) + 1)
        if self.dash_grid:
            self.canvas.setStrokeColorRGB(0.75, 0.75, 0.75)
            self.canvas.setFillColorRGB(1, 1, 1)
            self.canvas.setDash(1, 1)
        else:
            self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.grid([xs + dx * self.grid_size for dx in cols],
                         [ys - dy * self.grid_size for dy in rows])

    def get_bound_rect(self, part):
        return max(
            map(lambda it: (it.xpos + it.dx) * unit * self.grid_size + (it.xpos + 2) / 2 * self.pdf_face_padding,
                part)), \
               max(map(
                   lambda it: (it.ypos + it.dy) * unit * self.grid_size + (it.ypos + 2) / 2 * self.pdf_face_padding,
                   part))

    def draw_mob_name(self):
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.setFillColorRGB(0, 0, 0)
        self.canvas.setFontSize(20);
        self.canvas.drawRightString(self.pdf_pagesize[0] - self.pdf_left, self.pdf_top - self.pdf_top_bound,
                                    self.mob_name)
        self.canvas.setFontSize(12);

    def draw_part_name(self, text):
        self.canvas.setStrokeColorRGB(0, 0, 0, 1)
        self.canvas.setFillColorRGB(0, 0, 0, 1)
        self.canvas.drawString(self.current_xpos, self.current_ypos, text)

    def draw_bound_rect(self, xsize, ysize):
        self.canvas.setDash()
        self.canvas.setFillColorRGB(1, 0, 0, 0)
        self.canvas.setStrokeColorRGB(1, 0, 0, 1)
        self.canvas.rect(self.current_xpos, self.current_ypos, xsize, ysize)

    def draw_part(self, part_name, update_position=True):
        part = skinmap[part_name]
        x_size, y_size = self.get_bound_rect(part)

        if self.current_xpos + x_size > self.pdf_pagesize[0] - self.pdf_left:
            self.current_xpos = self.pdf_left
            self.current_ypos = self.current_ypos - self.old_y_size - self.pdf_part_padding
            self.old_y_size = 0
        if self.current_ypos - y_size < self.pdf_top_bound:
            self.canvas.showPage()
            self.current_ypos = self.pdf_top

        for face in part:
            self.draw_face_grid(face, self.current_xpos, self.current_ypos)
        #self.draw_bound_rect(x_size, -y_size)

        if update_position:
            self.draw_part_name(part_name)
        else:
            return

        self.current_xpos = self.current_xpos + x_size + self.pdf_part_padding
        self.old_y_size = y_size if y_size > self.old_y_size else self.old_y_size

    def draw(self):
        self.draw_mob_name()
        part_names = list(filter(lambda n: n != 'mask', skinmap.keys()) if self.place_mask_on_head else skinmap.keys())

        self.old_y_size = 0
        for part_name in part_names:
            self.draw_part(part_name, update_position=not (self.place_mask_on_head and part_name == 'head'))
            if self.place_mask_on_head and part_name == 'head':
                self.draw_part('mask')

        self.canvas.save()

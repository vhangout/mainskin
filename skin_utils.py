from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from skinmap import Face, skinmap, unit

#only for A4 portret paper size 210mm x 297mm
paper_type = A4


class SkinUtils:
    def __init__(self, pixelmap, pdf_file_name, mob_name='',
                 pdf_left_bound=1 * cm, pdf_top_bound=1 * cm,
                 pdf_grid_size=5 * mm,
                 pdf_face_padding=3 * mm, pdf_part_padding=1.5 * cm,
                 face_flip_horizontally=False,
                 place_mask_on_head=True):
        self.pixelmap = pixelmap
        self.pdf_file_name = pdf_file_name
        self.mob_name = mob_name
        self.pdf_left_bound = pdf_left_bound
        self.pdf_top_bound = pdf_top_bound
        self.pdf_grid_size = pdf_grid_size
        self.pdf_face_padding = pdf_face_padding
        self.pdf_part_padding = pdf_part_padding
        self.face_flip_horizontally = face_flip_horizontally
        self.place_mask_on_head = place_mask_on_head
        self.pdf_left, self.pdf_top = self.pdf_left_bound, paper_type[1] - self.pdf_top_bound
        self.current_xpos, self.current_ypos = self.pdf_left, self.pdf_top

        min_bound_part = min(skinmap.values(), key=lambda p: self.get_bound_rect(p)[0] * self.get_bound_rect(p)[1])
        self.min_bound_rect = self.get_bound_rect(min_bound_part)

        self.canvas = Canvas(pdf_file_name, pagesize=paper_type)

    def get_pixelmap(self, face: Face):
        return [self.pixelmap[y][face.x * unit:face.x * unit + face.dx * unit]
                for y in range(face.y * unit, face.y * unit + face.dy * unit)]

    def draw_face_grid(self, face: Face, current_x, current_y, transparent=False):
        pixelmap = self.get_pixelmap(face)
        xs = current_x + face.xpos * unit * self.pdf_grid_size + face.xpos / 2 * self.pdf_face_padding
        ys = current_y - face.ypos * unit * self.pdf_grid_size - face.ypos / 2 * self.pdf_face_padding

        for dy, line in enumerate(pixelmap):
            line = line if not self.face_flip_horizontally else line[::-1]
            for dx, dot in enumerate(line):
                x = xs + dx * self.pdf_grid_size
                y = ys - dy * self.pdf_grid_size
                if dot[3] > 0:
                    self.canvas.setStrokeColorRGB(dot[0] / 255, dot[1] / 255, dot[2] / 255, 1)
                    self.canvas.setFillColorRGB(dot[0] / 255, dot[1] / 255, dot[2] / 255, 1)
                    self.canvas.rect(x, y, self.pdf_grid_size, -self.pdf_grid_size, False, True)
                elif not transparent:
                    self.canvas.setFillColorRGB(0.85, 0.85, 0.85, 0)
                    self.canvas.rect(x, y, self.pdf_grid_size / 2, -self.pdf_grid_size / 2, False, True)
                    self.canvas.rect(x + self.pdf_grid_size / 2, y - self.pdf_grid_size / 2, self.pdf_grid_size / 2,
                                     -self.pdf_grid_size / 2, False,
                                     True)

        rows = range(len(pixelmap) + 1)
        cols = range(len(pixelmap[0]) + 1)
        self.canvas.setStrokeColorRGB(0.75, 0.75, 0.75)
        self.canvas.setFillColorRGB(1, 1, 1)
        self.canvas.setDash(1, 1)
        self.canvas.grid([xs + dx * self.pdf_grid_size for dx in cols],
                         [ys - dy * self.pdf_grid_size for dy in rows])

    def get_bound_rect(self, part):
        return max(
            map(lambda it: (it.xpos + it.dx) * unit * self.pdf_grid_size + (it.xpos + 2) / 2 * self.pdf_face_padding,
                part)), \
               max(map(
                   lambda it: (it.ypos + it.dy) * unit * self.pdf_grid_size + (it.ypos + 2) / 2 * self.pdf_face_padding,
                   part))

    def draw_mob_name(self):
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.setFillColorRGB(0, 0, 0)
        self.canvas.setFontSize(20);
        self.canvas.drawRightString(paper_type[0] - self.pdf_left, self.pdf_top - self.pdf_top_bound, self.mob_name)
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

        for face in part:
            self.draw_face_grid(face, self.current_xpos, self.current_ypos)
        #self.draw_bound_rect(x_size, -y_size)
        if update_position:
            self.draw_part_name(part_name)

        if not update_position:
            return
        self.current_xpos = self.current_xpos + x_size + self.pdf_part_padding
        if self.current_xpos + self.min_bound_rect[0] > paper_type[0] - self.pdf_left:
            self.current_xpos = self.pdf_left
            self.current_ypos = self.current_ypos - y_size - self.pdf_part_padding
        if self.current_ypos - self.min_bound_rect[1] < self.pdf_top_bound:
            self.canvas.showPage()
            self.current_ypos = self.pdf_top

    def draw_skin(self):
        self.draw_mob_name()
        part_names = list(filter(lambda n: n != 'mask', skinmap.keys()) if self.place_mask_on_head else skinmap.keys())
        for part_name in part_names:
            self.draw_part(part_name, update_position=not (self.place_mask_on_head and part_name == 'head'))
            if self.place_mask_on_head and part_name == 'head':
                self.draw_part('mask')
        self.canvas.save()


# def place_mask(self.canvas, bitmap):
#    for face in skinmap['mask0']:
#        face_pixelmap = get_pixelmap(bitmap, face)
#        draw_grid(self.canvas, face_pixelmap, face, True)

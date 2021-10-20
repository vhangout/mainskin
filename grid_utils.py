from math import trunc, pi, sin, cos, radians
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4

#only for A4 portret paper size 210mm x 297mm
paper_type = A4

class GridUtils:
    def __init__(self, pdf_file_name,
                 pdf_left_bound=1 * cm, pdf_top_bound=1 * cm,
                 pdf_padding=3 * mm):
        self.pdf_file_name = pdf_file_name
        self.pdf_left_bound = pdf_left_bound
        self.pdf_top_bound = pdf_top_bound
        self.pdf_padding = pdf_padding
        self.pdf_left = pdf_left_bound
        self.pdf_top = paper_type[1] - self.pdf_top_bound

        self.canvas = Canvas(pdf_file_name, pagesize=paper_type)

        self.current_x = self.pdf_left
        self.current_y = self.pdf_top

    def draw_grid(self, grid_size, row_count):
        xs = self.current_x
        ys = self.current_y

        self.canvas.setStrokeColorRGB(0, 0, 0)

        col_count = trunc((paper_type[0] - 2 * self.pdf_left) / grid_size)

        for dy in range(row_count + 1):
            y = ys - dy * grid_size
            self.canvas.line(xs, y, xs + grid_size * col_count, y)
        for dx in range(col_count + 1):
            x = xs + dx * grid_size
            self.canvas.line(x, ys, x, ys - grid_size * row_count)

    def draw_angles(self, height):
        xs = self.current_x
        ys = self.current_y

        for angle in range(5, 85, 5):
            self.canvas.line(xs, ys, xs + height * cos(radians(angle)),
                             ys - height * sin(radians(angle)))
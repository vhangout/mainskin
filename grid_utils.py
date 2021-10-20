from math import trunc, pi, sin, cos, radians
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4

# only for A4 portret paper size 210mm x 297mm
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

    def __draw_grid(self, size, rows, cols):
        xs = self.current_x
        ys = self.current_y
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.grid([xs + size * dx for dx in range(cols + 1)], [ys - size * dy for dy in range(rows + 1)])

    def __draw_angles(self, height):
        xs = self.current_x
        ys = self.current_y
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.lines([(xs, ys, xs + height * cos(radians(angle)),
                            ys - height * sin(radians(angle))) for angle in range(5, 85, 5)])
        self.canvas.setFillColorRGB(1, 1, 1, 1)
        self.canvas.wedge(xs - cm, ys + cm, xs + cm, ys - cm, 0, -90, 1, 1)

    def __draw_grid_mm(self, grid_size, height):
        size = grid_size * mm
        rows = trunc(height / size)
        cols = trunc((paper_type[0] - 2 * self.pdf_left) / size)

        self.__draw_grid(size, rows, cols)
        self.__draw_angles(height * 0.95)
        self.canvas.setFontSize(8)
        self.canvas.setFillColorRGB(0, 0, 0, 1)
        self.canvas.drawString(self.current_x + 0.5 * mm, self.current_y - 5 * mm, f'{int(grid_size)}mm')

        self.current_y = self.current_y - rows * size - self.pdf_padding
        if self.current_y - rows * size - self.pdf_padding < self.pdf_top_bound:
            self.canvas.showPage()
            self.current_y = self.pdf_top

    def draw_grids(self, height, *args):
        for grid_size in args:
            self.__draw_grid_mm(grid_size, height)
        self.canvas.save()

from math import trunc, pi, sin, cos, radians

from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from pagesizes import pagesizes

class GridUtils:
    def __init__(self, pdf_file_name,
                 grid_height=139,
                 grids=[],
                 pdf_pagesize='A4', pdf_landscape=False,
                 pdf_left_bound=10, pdf_top_bound=10,
                 pdf_padding=3):
        self.pdf_file_name = pdf_file_name
        self.grid_height = grid_height * mm
        self.grids = grids
        self.pdf_pagesize = pagesizes[pdf_pagesize] if not pdf_landscape else landscape(pagesizes[pdf_pagesize])
        self.pdf_left_bound = pdf_left_bound * mm
        self.pdf_top_bound = pdf_top_bound * mm
        self.pdf_padding = pdf_padding * mm
        self.pdf_left = self.pdf_left_bound
        self.pdf_top = self.pdf_pagesize[1] - self.pdf_top_bound

        self.canvas = Canvas(pdf_file_name, pagesize=self.pdf_pagesize)

        self.current_x = self.pdf_left
        self.current_y = self.pdf_top

    def __draw_grid(self, size, rows, cols):
        xs = self.current_x
        ys = self.current_y
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.grid([xs + size * dx for dx in range(cols + 1)], [ys - size * dy for dy in range(rows + 1)])

    def __draw_angles(self):
        xs = self.current_x
        ys = self.current_y
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.lines([(xs, ys, xs + self.grid_height * 0.95 * cos(radians(angle)),
                            ys - self.grid_height * 0.95 * sin(radians(angle))) for angle in range(5, 85, 5)])
        self.canvas.setFillColorRGB(1, 1, 1, 1)
        self.canvas.wedge(xs - cm, ys + cm, xs + cm, ys - cm, 0, -90, 1, 1)

    def __draw_grid_mm(self, grid_size):
        size = grid_size * mm
        rows = trunc(self.grid_height / size)
        cols = trunc((self.pdf_pagesize[0] - 2 * self.pdf_left) / size)

        self.__draw_grid(size, rows, cols)
        self.__draw_angles()
        self.canvas.setFontSize(8)
        self.canvas.setFillColorRGB(0, 0, 0, 1)
        self.canvas.drawString(self.current_x + 0.5 * mm, self.current_y - 5 * mm, f'{int(grid_size)}mm')

        self.current_y = self.current_y - rows * size - self.pdf_padding
        if self.current_y - rows * size - self.pdf_padding < self.pdf_top_bound:
            self.canvas.showPage()
            self.current_y = self.pdf_top

    def draw(self):
        for grid in self.grids:
            self.__draw_grid_mm(grid)
        self.canvas.save()

from collections import namedtuple
from reportlab.lib.units import cm, mm

pdf_left = 1 * cm
pdf_top = 1 * cm
pdf_grid_size = 5 * mm
pdf_padding = 3 * mm
pdf_pad_model = 1.5 * cm

Face = namedtuple('Face', ['x', 'y', 'dx', 'dy', 'xpos', 'ypos'])

# 1 unit is 4 squares (pixels)

unit = 4

skinmap = {
    'head': [
        Face(2, 0, 2, 2, 2, 0),
        Face(0, 2, 2, 2, 0, 2),
        Face(2, 2, 2, 2, 2, 2),
        Face(4, 2, 2, 2, 4, 2),
        Face(6, 2, 2, 2, 6, 2),
        Face(4, 0, 2, 2, 2, 4)
    ],

    'body': [
        Face(5, 4, 2, 1, 1, 0),
        Face(4, 5, 1, 3, 0, 1),
        Face(5, 5, 2, 3, 1, 1),
        Face(7, 5, 1, 3, 3, 1),
        Face(8, 5, 2, 3, 4, 1),
        Face(7, 4, 2, 1, 1, 4)
    ],

    'left hand': [
        Face(11, 4, 1, 1, 4 * pdf_grid_size + pdf_padding, 0),
        Face(10, 5, 1, 3, 0, 4 * pdf_grid_size + pdf_padding),
        Face(11, 5, 1, 3, 4 * pdf_grid_size + pdf_padding, 4 * pdf_grid_size + pdf_padding),
        Face(12, 5, 1, 3, 8 * pdf_grid_size + 2 * pdf_padding, 4 * pdf_grid_size + pdf_padding),
        Face(13, 5, 1, 3, 12 * pdf_grid_size + 3 * pdf_padding, 4 * pdf_grid_size + pdf_padding),
        Face(12, 4, 1, 1, 4 * pdf_grid_size + pdf_padding, 16 * pdf_grid_size + 2 * pdf_padding)
    ],
    'right hand': [
        Face(9, 12, 1, 1, 22 * pdf_grid_size + pdf_padding, 0),
        Face(8, 13, 1, 3, 18 * pdf_grid_size, 4 * pdf_grid_size + pdf_padding),
        Face(9, 13, 1, 3, 22 * pdf_grid_size + pdf_padding, 4 * pdf_grid_size + pdf_padding),
        Face(10, 13, 1, 3, 26 * pdf_grid_size + 2 * pdf_padding, 4 * pdf_grid_size + pdf_padding),
        Face(11, 13, 1, 3, 30 * pdf_grid_size + 3 * pdf_padding, 4 * pdf_grid_size + pdf_padding),
        Face(10, 12, 1, 1, 22 * pdf_grid_size + pdf_padding, 16 * pdf_grid_size + 2 * pdf_padding)
    ],
    'left leg': [
        Face(1, 4, 1, 1, 4 * pdf_grid_size + pdf_padding, 24 * pdf_grid_size + pdf_pad_model),
        Face(0, 5, 1, 3, 0, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(1, 5, 1, 3, 4 * pdf_grid_size + pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(2, 5, 1, 3, 8 * pdf_grid_size + 2 * pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(3, 5, 1, 3, 12 * pdf_grid_size + 3 * pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(2, 4, 1, 1, 4 * pdf_grid_size + pdf_padding, 40 * pdf_grid_size + pdf_pad_model + 2 * pdf_padding),
    ],
    'right leg': [
        Face(5, 12, 1, 1, 22 * pdf_grid_size + pdf_padding, 24 * pdf_grid_size + pdf_pad_model),
        Face(4, 13, 1, 3, 18 * pdf_grid_size, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(5, 13, 1, 3, 22 * pdf_grid_size + pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(6, 13, 1, 3, 26 * pdf_grid_size + 2 * pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(7, 13, 1, 3, 30 * pdf_grid_size + 3 * pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(6, 12, 1, 1, 22 * pdf_grid_size + pdf_padding, 40 * pdf_grid_size + pdf_pad_model + 2 * pdf_padding)
    ],

    'mask': [
        Face(10, 0, 2, 2, 2, 0),
        Face( 8, 2, 2, 2, 0, 2),
        Face(10, 2, 2, 2, 2, 2),
        Face(12, 2, 2, 2, 4, 2),
        Face(14, 2, 2, 2, 6, 2),
        Face(12, 0, 2, 2, 2, 4)
    ]
}

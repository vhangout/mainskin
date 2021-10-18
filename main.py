import os
import re
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from collections import namedtuple

face_flip_horizontally = False
#place_mask_on_head = False

pdf_left = 1 * cm
pdf_top = 1 * cm
pdf_grid_size = 5 * mm
pdf_padding = 3 * mm
pdf_pad_model = 1.5 * cm

Face = namedtuple('Face', ['x', 'y', 'dx', 'dy', 'xpos', 'ypos'])

skinmap = {
    'head': [
        Face(2, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 0),
        Face(0, 2, 2, 2, 0, 8 * pdf_grid_size + pdf_padding),
        Face(2, 2, 2, 2, 8 * pdf_grid_size + pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(4, 2, 2, 2, 16 * pdf_grid_size + 2 * pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(6, 2, 2, 2, 24 * pdf_grid_size + 3 * pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(4, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 16 * pdf_grid_size + 2 * pdf_padding)
    ],

    'body': [
        Face(5, 4, 2, 1, 4 * pdf_grid_size + pdf_padding, 24 * pdf_grid_size + pdf_pad_model),
        Face(4, 5, 1, 3, 0, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(5, 5, 2, 3, 4 * pdf_grid_size + pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(7, 5, 1, 3, 12 * pdf_grid_size + 2 * pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(8, 5, 2, 3, 16 * pdf_grid_size + 3 * pdf_padding, 28 * pdf_grid_size + pdf_pad_model + pdf_padding),
        Face(7, 4, 2, 1, 4 * pdf_grid_size + pdf_padding, 40 * pdf_grid_size + pdf_pad_model + 2 * pdf_padding)
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
        Face(10, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 0),
        Face(8, 2, 2, 2, 0, 8 * pdf_grid_size + pdf_padding),
        Face(10, 2, 2, 2, 8 * pdf_grid_size + pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(12, 2, 2, 2, 16 * pdf_grid_size + 2 * pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(14, 2, 2, 2, 24 * pdf_grid_size + 3 * pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(12, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 16 * pdf_grid_size + 2 * pdf_padding)
    ],
    'mask0': [
        Face(10, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 0),
        Face(8, 2, 2, 2, 0, 8 * pdf_grid_size + pdf_padding),
        Face(10, 2, 2, 2, 8 * pdf_grid_size + pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(12, 2, 2, 2, 16 * pdf_grid_size + 2 * pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(14, 2, 2, 2, 24 * pdf_grid_size + 3 * pdf_padding, 8 * pdf_grid_size + pdf_padding),
        Face(12, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 16 * pdf_grid_size + 2 * pdf_padding)
    ],
    'mask': [
        Face(10, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 28 * pdf_grid_size),
        Face(8, 2, 2, 2, 0, 28 * pdf_grid_size + 8 * pdf_grid_size + pdf_padding),
        Face(10, 2, 2, 2, 8 * pdf_grid_size + pdf_padding, 28 * pdf_grid_size + 8 * pdf_grid_size + pdf_padding),
        Face(12, 2, 2, 2, 16 * pdf_grid_size + 2 * pdf_padding, 28 * pdf_grid_size + 8 * pdf_grid_size + pdf_padding),
        Face(14, 2, 2, 2, 24 * pdf_grid_size + 3 * pdf_padding, 28 * pdf_grid_size + 8 * pdf_grid_size + pdf_padding),
        Face(12, 0, 2, 2, 8 * pdf_grid_size + pdf_padding, 28 * pdf_grid_size + 16 * pdf_grid_size + 2 * pdf_padding)
    ]
}


def get_pixelmap(pixelmap, face: Face):
    return [pixelmap[y][face.x * 4:face.x * 4 + face.dx * 4] for y in range(face.y * 4, face.y * 4 + face.dy * 4)]


def get_min_left(faces):
    return pdf_left + min(faces, key=lambda it: it.xpos).xpos


def draw_title(cnv: Canvas, text):
    cnv.setStrokeColorRGB(0, 0, 0)
    cnv.setFillColorRGB(0, 0, 0)
    cnv.setFontSize(24);
    cnv.drawRightString(210 * mm - pdf_left, 297 * mm - 2 * pdf_top, text)
    cnv.setFontSize(12);


def draw_text(cnv: Canvas, text, faces):
    cnv.setStrokeColorRGB(0, 0, 0)
    cnv.setFillColorRGB(0, 0, 0)
    cnv.drawString(get_min_left(faces), 297 * mm - pdf_top - faces[0].ypos, text)


def draw_grid(cnv, pixelmap, face: Face, transparent=False):
    xs = pdf_left + face.xpos
    ys = 297 * mm - pdf_top - face.ypos
    cnv.setStrokeColorRGB(0, 0, 0)
    cnv.rect(xs, ys, pdf_grid_size * len(pixelmap[0]), -pdf_grid_size * len(pixelmap), True, False)

    for dy, line in enumerate(pixelmap):
        line = line if not face_flip_horizontally else line[::-1]
        for dx, dot in enumerate(line):
            x = xs + dx * pdf_grid_size
            y = ys - dy * pdf_grid_size
            if dot[3] > 0:
                cnv.setFillColorRGB(dot[0]/255, dot[1]/255, dot[2]/255)
                cnv.rect(x, y, pdf_grid_size+1, -pdf_grid_size-1, False, True)
                #cnv.line(x, y, x + pdf_grid_size, y)
                #cnv.line(x, y, x, y - pdf_grid_size)
            elif not transparent:
                cnv.setFillColorRGB(0.85, 0.85, 0.85)
                cnv.rect(x, y, pdf_grid_size/2, -pdf_grid_size/2, False, True)
                cnv.rect(x + pdf_grid_size/2, y - pdf_grid_size/2, pdf_grid_size/2, -pdf_grid_size/2, False, True)

    for dy in range(len(pixelmap) + 1):
        y = ys - dy * pdf_grid_size
        cnv.line(xs, y, xs + pdf_grid_size * len(pixelmap[0]), y)
    for dx in range(len(pixelmap[0]) + 1):
        x = xs + dx * pdf_grid_size
        cnv.line(x, ys, x, ys - pdf_grid_size * len(pixelmap))





def place_mask(cnv, bitmap):
    for face in skinmap['mask0']:
        face_pixelmap = get_pixelmap(bitmap, face)
        draw_grid(cnv, face_pixelmap, face, True)


if __name__ == '__main__':
    filename = r'd:\_MA_.png'
    mob_name = re.findall(r'(?:.*/|.*\\)?(.*).png|$', filename, re.IGNORECASE)[0];
    pdf_file_name = fr'{os.path.dirname(filename)}{mob_name}{"_flip" if face_flip_horizontally else ""}.pdf'

    skin = Image.open(filename)
    data = list(skin.getdata())
    bitmap = []
    for n in range(64):
        bitmap.append(data[n * 64:(n + 1) * 64])

    canvas = Canvas(pdf_file_name)
    draw_title(canvas, f'{mob_name}{" flip" if face_flip_horizontally else ""}')
    
    for key in ['head', 'body']:
        draw_text(canvas, key, skinmap[key])
        for face in skinmap[key]:
            face_pixelmap = get_pixelmap(bitmap, face)
            draw_grid(canvas, face_pixelmap, face)

    canvas.showPage()
    draw_title(canvas, f'{mob_name}{" flip" if face_flip_horizontally else ""}')
    for key in ['left hand', 'right hand']:
        draw_text(canvas, key, skinmap[key])
        for face in skinmap[key]:
            face_pixelmap = get_pixelmap(bitmap, face)
            draw_grid(canvas, face_pixelmap, face)

    for key in ['left leg', 'right leg']:
        draw_text(canvas, key, skinmap[key])
        for face in skinmap[key]:
            face_pixelmap = get_pixelmap(bitmap, face)
            draw_grid(canvas, face_pixelmap, face)

    #if not place_mask_on_head:
    canvas.showPage()
    draw_title(canvas, f'{mob_name}{" flip" if face_flip_horizontally else ""}')
    for key in ['head', 'mask']:
        draw_text(canvas, key, skinmap[key])
        for face in skinmap[key]:
            face_pixelmap = get_pixelmap(bitmap, face)
            draw_grid(canvas, face_pixelmap, face)
    #draw_text(canvas, 'mask', skinmap['mask'])
    place_mask(canvas, bitmap)

    #if place_mask_on_head:
    #    place_mask(canvas, bitmap)

    canvas.save()

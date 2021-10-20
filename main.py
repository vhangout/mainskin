import os
import re
from PIL import Image
from reportlab.lib.units import cm, mm
from draw_utils import DrawUtils
from grid_utils import GridUtils

face_flip_horizontally = False

if __name__ == '__main__':
    filename = r'd:\_MA_.png'
    mob_name = re.findall(r'(?:.*/|.*\\)?(.*).png|$', filename, re.IGNORECASE)[0];
    pdf_file_name = fr'{os.path.dirname(filename)}{mob_name}{"_flip" if face_flip_horizontally else ""}.pdf'

    #Load skin
    skin = Image.open(filename)
    data = list(skin.getdata())
    pixelmap = [data[n * 64:(n + 1) * 64] for n in range(64)]

    #draw_utils = DrawUtils(pixelmap, pdf_file_name, place_mask_on_head=False)

    #draw_title(canvas, f'{mob_name}{" flip" if face_flip_horizontally else ""}')

    #draw_utils.draw_skin()
    grid_utils = GridUtils(r'd:\grid.pdf')
    grid_utils.draw_grid(5*mm, 20)
    grid_utils.draw_angles(20 * 5 * mm)
    grid_utils.canvas.save()
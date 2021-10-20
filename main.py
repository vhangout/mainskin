import os
import re
from PIL import Image
from reportlab.lib.units import cm, mm
from skin_utils import SkinUtils
from grid_utils import GridUtils

face_flip_horizontally = False

if __name__ == '__main__':
    #filename = r'd:\_MA_.png'
    filename = r'd:\evgen_bro.png'
    mob_name = re.findall(r'(?:.*/|.*\\)?(.*).png|$', filename, re.IGNORECASE)[0];
    pdf_file_name = fr'{os.path.dirname(filename)}{mob_name}{"_flip" if face_flip_horizontally else ""}.pdf'

    #Load skin
    skin = Image.open(filename)
    data = list(skin.getdata())
    pixelmap = [data[n * 64:(n + 1) * 64] for n in range(64)]

    draw_utils = SkinUtils(pixelmap, pdf_file_name, mob_name)#, place_mask_on_head=False)
    draw_utils.draw_skin()

    #draw_title(canvas, f'{mob_name}{" flip" if face_flip_horizontally else ""}')

    #grid_utils = GridUtils(r'd:\grid.pdf')
    #grid_utils.draw_grids(13.9 * cm, 5, 3, 7, 10)


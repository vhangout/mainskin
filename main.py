import os
import re
from PIL import Image
from draw_utils import DrawUtils

face_flip_horizontally = False

if __name__ == '__main__':
    filename = r'd:\_MA_.png'
    mob_name = re.findall(r'(?:.*/|.*\\)?(.*).png|$', filename, re.IGNORECASE)[0];
    pdf_file_name = fr'{os.path.dirname(filename)}{mob_name}{"_flip" if face_flip_horizontally else ""}.pdf'

    #Load skin
    skin = Image.open(filename)
    data = list(skin.getdata())
    pixelmap = [data[n * 64:(n + 1) * 64] for n in range(64)]

    draw_utils = DrawUtils(pixelmap, pdf_file_name)

    #draw_title(canvas, f'{mob_name}{" flip" if face_flip_horizontally else ""}')

    draw_utils.draw_part('head')
    draw_utils.draw_part('body')
    draw_utils.draw_part('mask')
    draw_utils.draw_part('head')

    draw_utils.canvas.save()
    exit()

'''    
    for key in ['head', 'body']:
        draw_text(canvas, key, skinmap[key])
        for face in skinmap[key]:
            face_pixelmap = get_pixelmap(bitmap, face)
            draw_grid(canvas, face_pixelmap, face, current_xpos, current_ypos)
        xs, ys = get_bound_rect(skinmap[key])
        draw_bound_rect(canvas, current_xpos, current_ypos, xs, -ys)




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
'''
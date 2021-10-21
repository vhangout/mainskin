import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()


'''
    #filename = r'd:\_MA_.png'
#    filename = r'd:\evgen_bro.png'
#    mob_name = re.findall(r'(?:.*/|.*\\)?(.*).png|$', filename, re.IGNORECASE)[0];
    pdf_file_name = fr'{os.path.dirname(filename)}{mob_name}{"_flip" if face_flip_horizontally else ""}.pdf'

    #Load skin
    skin = Image.open(filename)
    data = list(skin.getdata())
    pixelmap = [data[n * 64:(n + 1) * 64] for n in range(64)]

    draw_utils = SkinUtils(pixelmap, pdf_file_name, mob_name)#, place_mask_on_head=False)
    draw_utils.draw_skin()

    #grid_utils = GridUtils(r'd:\grid.pdf')
    #grid_utils.draw_grids(13.9 * cm, 5, 3, 7, 10)

'''
import re
from PIL import Image
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QComboBox, QFileDialog, QMessageBox
from PyQt5.uic import loadUi

from grid_utils import GridUtils
from pagesizes import pagesizes
from skin_utils import SkinUtils


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main_window.ui", self)
        self.pbSkinBrowsePNG.clicked.connect(self.browsePNG)

        self.cbSkinPaperSize.addItems(pagesizes.keys())
        self.setComboboxValue(self.cbSkinPaperSize, 'A4')

        self.pbSkinSavePDF.clicked.connect(self.saveSkinPDF)

        self.cbGridPaperSize.addItems(pagesizes.keys())
        self.setComboboxValue(self.cbGridPaperSize, 'A4')

        self.pbGridSavePDF.clicked.connect(self.saveGridPDF)

        self.errorDialog = QMessageBox()
        self.errorDialog.setIcon(QMessageBox.Critical)
        self.errorDialog.setText("Error")
        self.errorDialog.setWindowTitle("Error")

    @pyqtSlot()
    def browsePNG(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Maincraft skin PNG file', filter='Images (*.png)')[0]
        if fname:
            self.leSkinPNGFile.setText(fname)

    @pyqtSlot()
    def saveSkinPDF(self):
        if not self.leSkinPNGFile.text():
            self.errorDialog.setInformativeText('Please select Maincraft skin PNG file')
            self.errorDialog.exec_()
            return

        fname = QFileDialog.getSaveFileName(self, 'Save PDF Document', filter='PDF Documents (*.pdf)')[0]
        if fname:
            skin = Image.open(self.leSkinPNGFile.text())
            data = list(skin.getdata())
            pixelmap = [data[n * 64:(n + 1) * 64] for n in range(64)]

            draw_utils = SkinUtils(pixelmap=pixelmap,
                                   pdf_file_name=fname,
                                   mob_name=self.leMobName.text(),
                                   pdf_pagesize=str(self.cbSkinPaperSize.currentText()),
                                   pdf_landscape='Landscape' == str(self.cbSkinPageOrientation.currentText()),
                                   pdf_left_bound=self.sbSkinMarginHor.value(),
                                   pdf_top_bound=self.sbSkinMarginVert.value(),
                                   pdf_grid_size=self.sbSkinGridSize.value(),
                                   pdf_face_padding=self.sbSkinFacePadding.value(),
                                   pdf_part_padding=self.sbSkinPartPadding.value(),
                                   face_flip_horizontally=self.checkSkinFlipHor.isChecked(),
                                   place_mask_on_head=self.checkSkinMergeMask.isChecked())
            draw_utils.draw()

    @pyqtSlot()
    def saveGridPDF(self):
        if not re.fullmatch(r'(?:\d+,?)+', self.leGridGridsSizes.text()):
            self.errorDialog.setInformativeText('Please select grid sizes')
            self.errorDialog.exec_()
            return

        fname = QFileDialog.getSaveFileName(self, 'Save PDF Document', filter='PDF Documents (*.pdf)')[0]
        if fname:
            grid_utils = GridUtils(pdf_file_name=fname,
                                   grid_height=139,
                                   grids=[int(size) for size in self.leGridGridsSizes.text().split(',')],
                                   pdf_pagesize=str(self.cbGridPaperSize.currentText()),
                                   pdf_landscape='Landscape' == str(self.cbGridPageOrientation.currentText()),
                                   pdf_left_bound=self.sbGridMarginHor.value(),
                                   pdf_top_bound=self.sbGridMarginVert.value(),
                                   pdf_padding=self.sbGridPadding.value())
            grid_utils.draw()

    @staticmethod
    def setComboboxValue(cb: QComboBox, value: str):
        index = cb.findText(value)
        if index >= 0:
            cb.setCurrentIndex(index)

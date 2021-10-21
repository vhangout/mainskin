from PIL import Image
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QComboBox, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
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

        self.errorDialog = QMessageBox()
        self.errorDialog.setIcon(QMessageBox.Critical)
        self.errorDialog.setText("Error")
        self.errorDialog.setWindowTitle("Error")

    @pyqtSlot()
    def browsePNG(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Maincraft skin PNG file', filter='Images (*.png)')
        if fname[0]:
            self.leSkinPNGFile.setText(fname[0])

    @pyqtSlot()
    def saveSkinPDF(self):
        if not self.leSkinPNGFile.text():
            self.errorDialog.setInformativeText('Please select Maincraft skin PNG file')
            self.errorDialog.exec_()
            return

        fname = QFileDialog.getSaveFileName(self, 'Save PDF Document', filter='PDF Documents (*.pdf)')
        if fname[0]:
            skin = Image.open(self.leSkinPNGFile.text())
            data = list(skin.getdata())
            pixelmap = [data[n * 64:(n + 1) * 64] for n in range(64)]

            draw_utils = SkinUtils(pixelmap
                                   )#, pdf_file_name, mob_name)  # , place_mask_on_head=False)
            draw_utils.draw_skin()

    @staticmethod
    def setComboboxValue(cb: QComboBox, value: str):
        index = cb.findText(value)
        if index >= 0:
            cb.setCurrentIndex(index)
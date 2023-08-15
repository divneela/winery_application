import sys
import os
import datetime
import re
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from DATA225utils import *
from Customization import *

customer_id=1001
wine_id="WINE001"

class Checkoutdummy(QMainWindow):
    def __init__(self):
        super().__init__()

        # create the button
        button = QPushButton('Add to Cart', self)
        button.clicked.connect(self.add_to_cart)

        # set the central widget
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(button)
        self.setCentralWidget(widget)

    def add_to_cart(self):
        # create and show the checkout window
        '''
        current_path = os.getcwd()
        self.checkout_window = Customization(current_path+"/images",CustomerID,WineId)
        self.checkout_window.show()
        
        self.checkout_window = Checkout(CustomerID,WineId)
        self.checkout_window.show()
        '''
        self.ask_for_customization()
        
        
    def ask_for_customization(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Customization Confirmation')
        layout = QVBoxLayout()
        label = QLabel('Would you like to Customize your order?', dialog)
        layout.addWidget(label)
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, dialog)
        buttons.accepted.connect(lambda: self.open_custom(dialog))
        buttons.rejected.connect(lambda: self.open_checkout(dialog))
        
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        
        dialog.exec_()

    def open_custom(self, dialog):
        # close the dialog box
        dialog.accept()

        current_path = os.getcwd()
        self.checkout_window = Customization(current_path+"/images",customer_id,wine_id)
        self.checkout_window.show()

    def open_checkout(self, dialog):
        # close the dialog box
        dialog.reject()

        # create and show window B
        self.checkout_window = Checkout(customer_id,wine_id)
        self.checkout_window.show()


if __name__ == '__main__':
    app = QApplication([])
    window = Checkoutdummy()
    window.show()
    app.exec_()

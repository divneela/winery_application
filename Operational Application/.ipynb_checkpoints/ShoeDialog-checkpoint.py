import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from DATA225utils import make_connection

class ShoeDialog(QDialog):
    def __init__(self, shoe_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shoe Information")
        layout = QVBoxLayout(self)
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # Create labels and set their text to the shoe information
        brand_label = QLabel("Brand:")
        brand_value_label = QLabel(shoe_info.get("brand", ""))
        model_label = QLabel("Model:")
        model_value_label = QLabel(shoe_info.get("model", ""))
        price_label = QLabel("Price:")
        price_value_label = QLabel(shoe_info.get("price", ""))

        # Add labels to the grid layout
        grid_layout.addWidget(brand_label, 0, 0)
        grid_layout.addWidget(brand_value_label, 0, 1)
        grid_layout.addWidget(model_label, 1, 0)
        grid_layout.addWidget(model_value_label, 1, 1)
        grid_layout.addWidget(price_label, 2, 0)
        grid_layout.addWidget(price_value_label, 2, 1)

        # Add a button to close the dialog
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

# Create a function to handle the Add to Cart button click event
def add_to_cart_clicked():
    # Create a dictionary containing some basic information about the shoe
    shoe_info = {"brand": "Nike", "model": "Air Max 270", "price": "$150"}

    # Create a dialog box and display the shoe information
    dialog = ShoeDialog(shoe_info)
    dialog.exec_()

# Create the application and main window
app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.setWindowTitle("My Application")

# Create a button and connect its clicked signal to the add_to_cart_clicked function
add_to_cart_button = QPushButton("Add to Cart")
add_to_cart_button.clicked.connect(add_to_cart_clicked)

# Add the button to the main window
main_window.setCentralWidget(add_to_cart_button)
main_window.show()

# Start the application event loop
sys.exit(app.exec_())

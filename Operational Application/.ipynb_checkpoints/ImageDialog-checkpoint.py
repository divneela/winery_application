import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from DATA225utils import make_connection

conn = make_connection(config_file='bossbunch_db.ini')
cursor = conn.cursor()
cust_img=""
bottle_name_text=""
price=0
CustomerID=1001
pers_id="PERS001"

class ImageDialog(QMainWindow):
    def __init__(self, folder_path):
        super().__init__()
        
        # Set the title and window properties
        self.setWindowTitle("Customize your Wine")
        self.setFixedSize(850, 700)
        
        '''
        # Add the background image
        self.bg = QLabel(self)
        self.bg.setAlignment(Qt.AlignBottom)
        pic=QPixmap("bg2.jpg")
        self.bg.setPixmap(pic)
        
        # Create an opacity effect and set its opacity
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.378)
        self.bg.setGraphicsEffect(opacity)
        self.bg.setGeometry(0, 0, pic.width(), pic.height())
        self.bg.raise_()
        
        '''

        # Get a list of all image files in the specified folder
        self.image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                            if os.path.isfile(os.path.join(folder_path, f))
                            and f.lower().endswith(('.png'))]
        self.current_index = 0  # Index of the currently displayed image

        
        self.image_label = QLabel(self)
        self.display_image()
        
        # ***** INNER LAYOUT  **********#
        
        # Add some space between the logo and the username/password fields
        #spacer_item = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Create a QFrame widget with a QVBoxLayout
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.innerLayout = QVBoxLayout(self.frame)
        self.innerLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Add a QLabel to the inner layout
        innerLabel = QLabel(" Lets personalize your Wine ! ")
        innerLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = innerLabel.font()
        font.setFamily("Brush Script MT")
        font.setPointSize(35)
        font.setBold(True)
        innerLabel.setFont(font)
        
        bottle_name = QLabel("", self.frame)
        bottle_name.setText(str(bottle_name_text))
        bottle_name.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = bottle_name.font()
        font.setPointSize(40)
        font.setBold(True)
        bottle_name.setFont(font)
        
        
        # Add price
        priceLabel = QLabel("$24.99 ", self.frame)
        priceLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = priceLabel.font()
        font.setPointSize(20)
        font.setBold(True)
        priceLabel.setFont(font)
        
        
        # Create a checkbox and connect it to a function
        self.checkbox = QCheckBox("Is it a Gift? Add Custom Message", self.frame)
        self.checkbox.stateChanged.connect(self.show_text_box)
        
        
        # Create a text box and hide it initially
        self.textbox = QLineEdit(self.frame)
        self.textbox.setPlaceholderText("Type here")
        #self.textbox.setFixedWidth(1000)
        self.textbox.setFixedHeight(60)
        self.textbox.hide()
        
        self.checkbox_gift_wrap = QCheckBox("Would you like to Gift wrap?", self.frame)
        self.checkbox_gift_wrap.hide()
        
        
        #Add Cart Button
        self.add_cart_button = QPushButton("Add to Cart", self.frame)
        self.add_cart_button.clicked.connect(self.add_to_cart_clicked)
        
        
        
        

        self.innerLayout.addWidget(innerLabel)
        self.innerLayout.addSpacing(80)
        self.innerLayout.addWidget(bottle_name)
        self.innerLayout.addWidget(priceLabel)
        self.innerLayout.addWidget(self.checkbox)
        self.innerLayout.addWidget(self.textbox)
        self.innerLayout.addWidget(self.checkbox_gift_wrap)
        self.innerLayout.addWidget(self.add_cart_button)
        #innerLayout.addSpacerItem(spacer_item) 
        #self.innerLayout.addWidget(self.next_button)
        
        
        
        
        
        

        # ***** INNER LAYOUT ENDS **********#
        
        # ***** TOP LAYOUT  **********#
        
        #Next Button
        self.next_button = QPushButton(">", self)
        self.next_button.setFixedSize(70, 150)
        self.next_button.clicked.connect(self.next_image)


        self.topLayout = QHBoxLayout(self)
        self.topLayout.addWidget(self.image_label)
        self.topLayout.addWidget(self.frame)
        self.topLayout.addWidget(self.next_button)
        
        # ***** TOP LAYOUT ends **********#
        
        
        centralWidget = QWidget()
        centralWidget.setLayout(QVBoxLayout())
        centralWidget.layout().addLayout(self.topLayout)
       # centralWidget.layout().addLayout(bottomLayout)

        # Set the central widget
        self.setCentralWidget(centralWidget)



    def display_image(self):
        # Load the current image and display it in the label
        pixmap = QPixmap(self.image_paths[self.current_index])
        desired_width = 200  # Set the desired width here
        scaled_pixmap = pixmap.scaledToWidth(desired_width, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignHCenter)
        print(self.image_paths[self.current_index])
        
        # Check DB
        
        global cust_img
        global bottle_name_text
        global price
        global pers_id
        
        cust_img = os.path.basename(self.image_paths[self.current_index])
        bottle_name_text,price,pers_id=self.fetch_customization_details()
       
        
    def next_image(self):
        # Increment the current index and display the next image
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.display_image()

        item = self.topLayout.itemAt(1)
        if type(item.widget()) == QFrame:
            # Find the first QLabel inside the QFrame
            label = item.widget().findChild(QLabel)
            if label:
                label.setText(str(bottle_name_text))

            # Find the second QLabel inside the QFrame
            label1 = item.widget().findChildren(QLabel)[1]
            if label1:
                label1.setText("$"+str(price))
        
        
        
    def fetch_customization_details(self):
        # Retrieve the security question and answer for the user
        global cust_img
        
        query = f"SELECT bottle_name,price,pers_id FROM customization WHERE image='{cust_img}'"
        cursor.execute(query)
        result = cursor.fetchone()
        bottle_name=""

        if result is not None:
            # Prompt the user to answer the security question
            bottle_name = result[0]
            price=result[1]
            pers_id=result[2]
        
        print("fetch data")
        print(cust_img)
        print(bottle_name)
        return bottle_name,price,pers_id
            
    def show_text_box(self, state):
        # Show or hide the text box based on the checkbox state
        if state == Qt.Checked:
            self.textbox.show()
            self.checkbox_gift_wrap.show()
        else:
            self.textbox.hide()  
            self.checkbox_gift_wrap.hide()
            
    def add_to_cart_clicked(self):
        
        if self.checkbox_gift_wrap.isChecked():
            dialog = QDialog(self)
            dialog.setWindowTitle('Confirmation')
            layout = QVBoxLayout()
            label = QLabel('Additional charges of $3.99 will be applicable for gift wrapping. Are you sure you want to proceed?', dialog)
            layout.addWidget(label)
            buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, dialog)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            dialog.setLayout(layout)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                print('Confirm button clicked')
                self.insert_to_cart(CustomerID)
            else:
                print('Cancel button clicked')
                
        else:
            self.insert_to_cart(CustomerID)
                
    def insert_to_cart(self, CustomerID):
        # Get the quantity of the selected wine in stock
        gift_wrap=False
        custom_message = self.textbox.text()
        
        if self.checkbox_gift_wrap.isChecked():
            gift_wrap=True
            customization_price=price+3.99
        else:
            customization_price=price
            
        print("customization_Details: " )
        print(pers_id,customization_price,gift_wrap,custom_message )
        
        query = f"UPDATE Cart set pers_id='{pers_id}',customization_price={customization_price},gift_wrap={gift_wrap},custom_message='{custom_message}' where CustomerID={CustomerID} "
        cursor.execute(query)
        conn.commit()

        '''
            QMessageBox.information(self, "Success", f"{wine_name} added to cart.")

        # If there is no stock available, show an error message
        else:
            wine_name = self.find_child_by_attribute("objectName", str(wine_id)).wine_name
            QMessageBox.warning(self, "Error", f"{wine_name} is out of stock.")
        '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    current_path = os.getcwd()
    slider = ImageDialog(current_path)
    slider.show()
    sys.exit(app.exec_())

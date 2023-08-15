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


conn = make_connection(config_file='bossbunch_db.ini')
cursor = conn.cursor()
cust_img=""
bottle_name_text=""
price=0
pers_id="PERS001"
add_to_cart=False
total_amount=0
no_coupon=True
coupon_used=""
quant=0
gift_wrap=False
new_cc=False

#HARDCODED
CustomerID=0
WineId=""


class Customization(QMainWindow):
    def __init__(self, folder_path,customer_id,wine_id):
        super().__init__()
        
        global CustomerID
        global WineId
        
        CustomerID=customer_id
        WineId=wine_id
        
        print("LOADED CUSTOM PAGE")
        print(CustomerID , WineId,customer_id,wine_id)
        
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
        
        self.checkout_button = QPushButton("Proceed to Checkout", self.frame)
        self.checkout_button.clicked.connect(self.checkout_clicked)
        
        

        self.innerLayout.addWidget(innerLabel)
        self.innerLayout.addSpacing(80)
        self.innerLayout.addWidget(bottle_name)
        self.innerLayout.addWidget(priceLabel)
        self.innerLayout.addWidget(self.checkbox)
        self.innerLayout.addWidget(self.textbox)
        self.innerLayout.addWidget(self.checkbox_gift_wrap)
        self.innerLayout.addWidget(self.add_cart_button)
        self.innerLayout.addWidget(self.checkout_button)
        #innerLayout.addSpacerItem(spacer_item) 
       
        
        
        
        
        
        

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
        
        global gift_wrap
        
        
        if self.checkbox.isChecked():
            custom_message = self.textbox.text()
            if self.checkbox_gift_wrap.isChecked():
                gift_wrap=True
                customization_price=price
            else:
                customization_price=price
        else:
            custom_message=""
            customization_price=price
        
            
        print("customization_Details: " )
        print(pers_id,customization_price,gift_wrap,custom_message )
        
        query = f"UPDATE Cart set pers_id='{pers_id}',customization_price={customization_price},gift_wrap={gift_wrap},custom_message='{custom_message}' where CustomerID={CustomerID} and WineId='{WineId}'"
        cursor.execute(query)
        conn.commit()
        
        global add_to_cart
        add_to_cart=True
        
        #self.show_checkout_page --CHECKOUT PAGE
        
    def checkout_clicked(self):
        if add_to_cart is True:
            print("Checkout clicked")
            self.show_checkout_page()
        else:
            QMessageBox.warning(self, "Error", "Your cart is empty!")
            return

    def show_checkout_page(self):
        print("show_checkout_page function")
        self.checkout = Checkout(CustomerID,WineId)
        self.checkout.show()
        
class Checkout(QDialog):
    def __init__(self,customer_id,wine_id, parent=None):
        super().__init__(parent)
        
        global CustomerID
        global WineId
        
        CustomerID=customer_id
        WineId=wine_id
        
        print(CustomerID , WineId)
        
        conn = make_connection(config_file='bossbunch_db.ini')
        cursor = conn.cursor()

        # Set up the UI elements
        self.setWindowTitle("Checkout Page")
        self.setFixedSize(650, 500)

        # create a widget
        self.widget = QWidget()
        
        #Wine Cost
         
        self.WineLabel = QLabel("")
        font = self.WineLabel.font()
        font.setPointSize(16)
        self.WineLabel.setFont(font)
        
        self.Winequantity = QLabel("")
        font = self.Winequantity.font()
        font.setPointSize(16)
        self.Winequantity.setFont(font)
        
        self.totalprice = QLabel("")
        font = self.totalprice.font()
        font.setPointSize(16)
        self.totalprice.setFont(font)
        
        
        #Customization Cost
        self.cust_Label = QLabel("Customization Cost:")
        font = self.cust_Label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.cust_Label.setFont(font)
        
        
        self.cust_bottle_Label = QLabel("")
        font = self.cust_bottle_Label.font()
        font.setPointSize(16)
        self.cust_bottle_Label.setFont(font)
        
        
        self.cust_bottle_totalprice = QLabel("")
        font = self.cust_bottle_totalprice.font()
        font.setPointSize(16)
        self.cust_bottle_totalprice.setFont(font)
        
        #gift wrap Cost
         
        self.gift_Label = QLabel("Gift wrap")
        font = self.gift_Label.font()
        font.setPointSize(16)
        self.gift_Label.setFont(font)
        
        
        self.gift_wrap_price = QLabel("$0.00")
        font = self.gift_wrap_price.font()
        font.setPointSize(16)
        self.gift_wrap_price.setFont(font)
        
        self.msg_Label = QLabel("Your custom message:")
        font = self.gift_Label.font()
        font.setPointSize(16)
        self.gift_Label.setFont(font)
        
        self.custom_message = QLabel("NA")
        font = self.custom_message.font()
        font.setPointSize(14)
        self.custom_message.setFont(font)
        
        #Coupon Code
        
        self.coupon_Label = QLabel("Have Coupon code? Enter Here :")
        font = self.gift_Label.font()
        font.setPointSize(16)
        self.gift_Label.setFont(font)
        
        self.coupon = QLineEdit()
        
        # Create a button to submit the input
        self.check_coupon = QPushButton('Check')
        self.check_coupon.clicked.connect(self.check_coupon_details)
        
        #Discount
        
        self.disc_Label = QLabel("Discount:")
        font = self.disc_Label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.disc_Label.setFont(font)
        
        
        self.disc_code = QLabel("NA")
        font = self.disc_code.font()
        font.setPointSize(16)
        self.disc_code.setFont(font)
        
        
        self.discount_amount = QLabel("-$0.00")
        font = self.discount_amount.font()
        font.setPointSize(16)
        self.discount_amount.setFont(font)
        
        
        #Total amt
        
        self.total_amt_Label = QLabel("Total amount payable:")
        font = self.total_amt_Label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.total_amt_Label.setFont(font)
        
        self.total_amount = QLabel("")
        font = self.total_amount.font()
        font.setPointSize(16)
        self.total_amount.setFont(font)
        
        self.cancel_button = QPushButton("CANCEL")
        self.cancel_button.clicked.connect(self.close)
        self.order_button = QPushButton("CONFIRM ORDER")
        self.order_button.clicked.connect(self.show_order_page)
        
        
        # create a grid layout
        layout = QGridLayout()

        # add the buttons to the grid layout
        layout.addWidget(self.WineLabel, 0, 0)
        layout.addWidget(self.Winequantity, 0, 1)
        layout.addWidget(self.totalprice,0,2)
        layout.addWidget(self.cust_Label, 1, 0)
        layout.addWidget(self.cust_bottle_Label, 2, 0)
        layout.addWidget(self.cust_bottle_totalprice, 2, 2)
        layout.addWidget(self.gift_Label, 3, 0)
        layout.addWidget(self.gift_wrap_price, 3, 2)
        layout.addWidget(self.msg_Label, 4,0)
        layout.addWidget(self.custom_message, 5,0)
        
        layout.addWidget(self.disc_Label, 6,0)
        layout.addWidget(self.coupon_Label, 7,0)
        layout.addWidget(self.coupon, 7,2)
        layout.addWidget(self.check_coupon, 8,2)
        
        
        layout.addWidget(self.disc_code, 9,0)
        layout.addWidget(self.discount_amount, 9,2)
        
        
        layout.addWidget(self.total_amt_Label, 12,0)
        layout.addWidget(self.total_amount, 12,2)
        
        layout.addWidget(self.cancel_button, 15,0)
        layout.addWidget(self.order_button, 15,2)

        # set the layout of the widget
        #self.widget.setLayout(layout)
        
        self.get_cart_details(CustomerID)
        
        self.setLayout(layout)
        
    def get_cart_details(self, cust_id):
        # Call the stored procedure
        cursor.callproc("get_cart_details", [cust_id])
    
        for result in cursor.stored_results():
            columns = [column[0] for column in result.description]
            print(f"Column names: {columns}")
            
            global total_amount
            global quant
            
            total_amount=0
            
            for row in result.fetchall():
                print(f"ROW:{row}")
                self.WineLabel.setText(row[1])
                self.Winequantity.setText(str(row[2])+"x"+str(round(row[3],2)))
                quant=row[2]
                total_amount=total_amount+(round(float(row[2])*float(row[3]),2))
                self.totalprice.setText("$"+str(round(float(row[2])*float(row[3]),2)))
                self.cust_bottle_Label.setText(row[4])
                self.cust_bottle_totalprice.setText("$"+ str(round(row[5],2)) )
                total_amount=total_amount+round(row[5],2)
                self.gift_wrap_price.setText("$"+str(round(row[6] , 2)))
                total_amount=total_amount+round(float(row[6] ), 2)
                if row[7] != "" :
                    self.custom_message.setText("\""+row[7]+"\"")
                self.total_amount.setText("$"+str(round(float(total_amount),2)))
    
    def check_coupon_details(self): 
        
        global coupon_used
        valid=False
        user_coupon=self.coupon.text()
        
        query = f"SELECT DiscountCode FROM Discounts WHERE DiscountCode='{user_coupon}'"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result is not None:
            if user_coupon == "BIRTHDAY10":
                valid=self.check_birthdate()
            else:
                valid=True
        
        if valid is True:
            self.apply_coupon_details()
            coupon_used=user_coupon
        else:
            QMessageBox.warning(self, "Error", "Invalid Coupon!")
            return
        
    def check_birthdate(self):
        query = f"select Month(BirthDate) from bossbunch_db.Customer where CustomerID='{CustomerID}'"
        cursor.execute(query)
        result = cursor.fetchone()
        customer_bday_month = result[0]
        
        now = datetime.datetime.now()
        current_month = now.month

        if customer_bday_month == current_month:
            return True
        else:
            return False
                    
    def apply_coupon_details(self):
        
        global no_coupon
        global coupon_used
        
        if no_coupon is True:
        
            user_coupon=self.coupon.text()
            query = f"SELECT DiscountPercentage FROM Discounts WHERE DiscountCode='{user_coupon}'"
            cursor.execute(query)
            result = cursor.fetchone()
            discount_percent=0.00
        
            global total_amount

            if result is not None:
                # Prompt the user to answer the security question
                self.disc_code.setText(user_coupon)
                discount_percent = result[0]
                discount_amount = float((discount_percent / 100)) * float(total_amount)
                self.discount_amount.setText("-$"+str(round(discount_amount,2)))
                total_amount=float(total_amount)-float(discount_amount)
                self.total_amount.setText("$"+str(round(float(total_amount),2)))
                no_coupon= False
                coupon_used=user_coupon
                
            print(discount_percent)
            
    def show_order_page(self):
        self.order = Order(self)
        self.order.show()
        
class Order(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the UI elements
        self.setWindowTitle("Order Confirmation")
        self.setFixedSize(760, 600)
        
        
        # Create the label
        self.details_label = QLabel('Name and Address:')
        font = self.details_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.details_label.setFont(font)
        
        #FullName,Address=self.get_customer_details
        
        FullName,Address=self.get_customer_details()
        
        self.name = QLabel(FullName)
        font = self.name.font()
        font.setPointSize(16)
        self.name.setFont(font)
        
        self.address = QLabel(Address)
        font = self.address.font()
        font.setPointSize(16)
        self.address.setFont(font)
        
        self.pay_label = QLabel('Payment :')
        font = self.pay_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.pay_label.setFont(font)
        
        self.amt_label = QLabel('Amount Payable :'+str(round(total_amount,2)))
        font = self.pay_label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.pay_label.setFont(font)
        
        self.layout=QVBoxLayout()

        self.layout.addWidget(self.details_label)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.address)
        self.layout.addWidget(self.pay_label)
        self.layout.addWidget(self.amt_label)
        
        #Fetch credit card
        
        self.radio_buttons = QGroupBox('Credit Cards')
        self.radio_layout = QVBoxLayout()
        self.radio_buttons.setLayout(self.radio_layout)

        # fetch credit card data from database table

        cursor.execute(f'SELECT CreditCard FROM Orders_CreditCard where  CustomerID={CustomerID}')
        credit_cards = cursor.fetchall()

        # create radio buttons for each credit card
        for card in credit_cards:
            radio = QRadioButton(card[0])
            self.radio_layout.addWidget(radio)
            
        self.new_card_radio = QRadioButton('Enter new Card Details:')
        self.radio_layout.addWidget(self.new_card_radio)
        self.new_card_radio.toggled.connect(self.toggle_textbox)
        

        self.card = QLineEdit()
        self.card.hide()

        self.validator = QRegExpValidator(QRegExp("^[0-9]{13,19}$"), self.card)
        self.card.setValidator(self.validator)

        self.card.textChanged.connect(self.validate_credit_card)

        self.card_status_label = QLabel("")
        font = self.card_status_label.font()
        font.setPointSize(16)
        self.card_status_label.setFont(font)
        self.card_status_label.hide()
                                 
        self.Expiry_label = QLabel("Expiry (MM/YYYY):")
        font = self.Expiry_label.font()
        font.setPointSize(16)
        self.Expiry_label.setFont(font)
        self.Expiry_label.hide()
        
        self.expiry = QLineEdit()
        self.expiry.hide()
                                 
        self.cvv_label = QLabel("CVV :")
        font = self.cvv_label.font()
        font.setPointSize(16)
        self.cvv_label.setFont(font)
        self.cvv_label.hide()
                                
        self.cvv = QLineEdit()
        self.cvv.setEchoMode(QLineEdit.Password)
        self.cvv.hide()
                                 
        self.cancel_order = QPushButton("CANCEL")
        self.cancel_order.clicked.connect(self.close)
        self.place_order = QPushButton("PLACE ORDER")
        self.place_order.clicked.connect(self.place_order_details)
        
        
        self.layout.addWidget(self.radio_buttons)
        self.layout.addWidget(self.card)
        self.layout.addWidget(self.card_status_label)
        self.layout.addWidget(self.Expiry_label)
        self.layout.addWidget(self.expiry)
        self.layout.addWidget(self.cvv_label)
        self.layout.addWidget(self.cvv)
        
        self.layout.addWidget(self.cancel_order)
        self.layout.addWidget(self.place_order)
                                
        # Set the layout for the dialog
                                
                                
        self.setLayout(self.layout)
        
    def toggle_textbox(self, state):
        global new_cc
        if self.new_card_radio.isChecked():
            
            new_cc=True
            
            self.card.show()
            self.card_status_label.show()
            self.Expiry_label.show()
            self.expiry.show()
            self.cvv_label.show()
            self.cvv.show()
        else:
            new_cc=False
            self.card.hide()
            self.card_status_label.hide()
            self.Expiry_label.hide()
            self.expiry.hide()
            self.cvv_label.hide()
            self.cvv.hide()

        
    def validate_credit_card(self):
        card_number = self.card.text().replace(" ", "")

        if re.match(r"^4[0-9]{12}(?:[0-9]{3})?$", card_number):
            self.card_status_label.setText("Visa")
        elif re.match(r"^5[1-5][0-9]{14}$", card_number):
            self.card_status_label.setText("MasterCard")
        elif re.match(r"^3[47][0-9]{13}$", card_number):
            self.card_status_label.setText("American Express")
        elif re.match(r"^6(?:011|5[0-9]{2})[0-9]{12}$", card_number):
            self.card_status_label.setText("Discover")
        else:
            self.card_status_label.setText("Invalid Card")

    def get_customer_details(self):
        
        query = f"SELECT concat(FirstName,' ', LastName) as FullName,concat(Street,',',City,',',State,',',Countrycode,',',ZipCode) as Address FROM Customer  WHERE CustomerID={CustomerID}"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result is not None:
            FullName = result[0]
            Address=result[1]
            
        return FullName,Address
    
    def place_order_details(self):
        
        if self.insert_order_details() is True:
            QMessageBox.information(self, "Order Confirmation", "Your Order has been successfully placed. please check your email for future details", QMessageBox.Ok)
            cursor.close()
            self.close()
            
        
    def insert_order_details(self):
        
        query = f"SELECT concat('ORD',lpad(count(*)+1,3,0)) as OrderID, concat('CUSTODR',lpad(count(*)+1,3,0)) as Custom_OrderID FROM Orders"
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result is not None:
            OrderID = result[0]
            Custom_OrderID=result[1]
            
        #Insert to Orders table
            
        query = f"INSERT INTO Orders select '{OrderID}' as OrderID,curdate() as Date,'' as Instructions,round({total_amount},2) as TotalAmount, '{coupon_used}' as Coupon, {CustomerID} as CustomerID"
        cursor.execute(query)
        conn.commit()
        print("insert Order completed")
         
            
        #Insert to Custom Orders table
            
        query = f"INSERT INTO Custom_orders select '{Custom_OrderID}' as Custom_OrderID,curdate() as Date , pers_id,custom_message,gift_wrap,case when gift_wrap = False then 0 else 3.99 end as gift_wrap_cost,customization_price as custom_bottle_price , case when gift_wrap=0 then customization_price else round(customization_price+3.99,2) end total_custom_price, '{OrderID}' as OrderID from Cart where CustomerID={CustomerID}"
        cursor.execute(query)
        conn.commit()
        print("insert Custom Order completed")
        
        #Insert into Items table
        
        query = f"INSERT INTO Items select '{WineId}' as ItemID,{quant} as quantity,'{OrderID}' as OrderID"
        cursor.execute(query)
        conn.commit()
        print("insert Items completed")
        
        #Insert into CreditCard tabe
        
        if new_cc is True:
        
            CreditCard=self.card.text()
        
            query = f"INSERT INTO Orders_CreditCard select '{CreditCard}' as CreditCard,'{OrderID}' as OrderID,'{CustomerID}' as CustomerID"
            cursor.execute(query)
            conn.commit()
            print("insert CreditCard completed")
        
        #Delete Cart
        
        query = f"DELETE FROM Cart where CustomerID= '{CustomerID}'"
        cursor.execute(query)
        conn.commit()
        print("Cart deleted")

        return True
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)  
    current_path = os.getcwd()
    slider = Customization(current_path+"/images")
    slider.show()
    sys.exit(app.exec_())

# Title: Personal Finance App
# File: Main App File
# Date: June 2023
# Author: Nick Mast
#
# This is an app for users to manage their finances. The user can track their income, expenses, and view the two compared 
# to each other.
# This app is written in python and uses PyQt5 for graphics and SQLite for data storage
import sys, os
import typing, database
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QStackedWidget, QPushButton, QTabWidget, QFormLayout, QLabel, QGroupBox, QVBoxLayout, QScrollArea, QWidget, QLineEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

# Welcome Screen Widget
class welcomeScreen(QDialog):
    # Initialization method
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Load our user interface
        uic.loadUi('welcomeScreen.ui', self)
        # Call our date method to get current date
        self.getDate()
        # If login button is clicked, jump to loginButton method
        self.login_button.clicked.connect(self.loginButton)
        # If signup button is clocked, hump to signupButton method
        self.signup_button.clicked.connect(self.signupButton)
    
    # This method gets the current date from QDate and sets our date_label to that date
    def getDate(self):
        # Get our current date
        date = QDate.currentDate()
        # Set our date label to our current date
        self.date_label.setText(date.toString())

    # This method connects our login_button to our login widget
    def loginButton(self):
        # Create an instance of loginScreen(The Class)
        login_var = loginScreen()
        # Add the widget to our stack
        lwidget.addWidget(login_var)
        # Increment the index of our stack by 1
        lwidget.setCurrentIndex(lwidget.currentIndex() + 1)

    # This method connects our signup_button to our signup widget
    def signupButton(self):
        for i in range(2):
            # Create an instance of signupScreen(The Class)
            signup_var = signupScreen()
            # Add the widget to our stack
            lwidget.addWidget(signup_var)
            # Increment the index of our stack by 2
            lwidget.setCurrentIndex(lwidget.currentIndex() + 1)



# Login Screen Widget
class loginScreen(QDialog):
    # Initialization method
    def __init__(self):
        super().__init__()
        # Load our user interface
        uic.loadUi('loginScreen.ui', self)
        # Set the password field so we can't see the text
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        # If back is clicked go to goBack method
        self.back_button.clicked.connect(self.goBack)
        # If login button is clicked go to login method
        self.login_button.clicked.connect(self.login)

    # This method handles the back button being clicked
    def goBack(self):
        remove = lwidget.currentWidget()
        lwidget.removeWidget(remove)
        lwidget.setCurrentIndex(lwidget.currentIndex() - 1)
    # This method handles the singup button being clicked
    def login(self):
        # Get the users email from the email field
        email = self.email_field.text()
        # Get the users password from the password field
        password = self.password_field.text()
        # Call the database login method to verify user data
        num = database.databaseMethods.login(email, password)
        # If num is -1 either the username or password is incorrect, if it is 0, not all fields are filled in, 
        # otherwise the user succesfully logs in
        if num == -1:
            self.error_label.setText("Incorrect email or password")
        elif num == 0:
            self.error_label.setText("Enter all fields")
        else:
            # Create an instance of homePage class
            firstName = database.databaseMethods.firstName(email)
            home_var = homePage(firstName, email)
            # Add the widget to our stack
            lwidget.addWidget(home_var)
            # Increment the index of our stack by 1
            lwidget.setCurrentIndex(lwidget.currentIndex() + 1)


# Signup Screen Widget
class signupScreen(QDialog):
    # Initialization method
    def __init__(self):
        super().__init__()
        # Load our user interface
        uic.loadUi('signupScreen.ui', self)
        # Set the password fields so we can't see the text
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        # If back is clicked go to goBack method
        self.back_button.clicked.connect(self.goBack)
        # If signup button is clicked, go to signup method
        self.signup_button.clicked.connect(self.signup)

    # This method handles the back button being clicked
    def goBack(self):
        for i in range(2):
            remove = lwidget.currentWidget()
            lwidget.removeWidget(remove)
            lwidget.setCurrentIndex(lwidget.currentIndex() - 2)
    # This method handles the singup button being clicked
    def signup(self):
        # Get the data the user entered
        firstName = self.first_name_field.text()
        lastName = self.last_name_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        confirmPassword = self.confirm_password_field.text()
        # Call our database method to store our new user data
        num = database.databaseMethods.signup(firstName, lastName, email, password, confirmPassword)
        if num == -2:
            self.error_label.setText("Email is already signed up")
        elif num == -1:
            self.error_label.setText("Passwords do not Match")
        elif num == 0:
            self.error_label.setText("Enter all fields")
        else:
            for i in range(2):
                # Create an instance of homePage class
                home_var = homePage(firstName, email)
                # Add the widget to our stack
                lwidget.addWidget(home_var)
                # Increment the index of our stack by 1
                lwidget.setCurrentIndex(lwidget.currentIndex() + 1)

# Homepage Class
class homePage(QDialog):
    def __init__(self, firstName, email):
        super().__init__()
        uic.loadUi('homePage.ui', self)
        self.email = email
        self.firstName = firstName

        # Get the users first name by calling our specific database method
        users_name = database.databaseMethods.firstName(email)
        # Set our My Account information
        self.accountInfo(firstName, email)

        # If our method returned -1, don't set the text to anything, else set the text to the name returned
        if users_name == -1:
            self.name_label.setText("")
        else:
            self.name_label.setText(users_name)

        # Set our homepage total label
        self.homeTotalLabel(firstName, email)
        # Set our income screen total label
        self.incomeTotalLabel(firstName, email)
        # Set our expenses screen total label
        self.expensesTotalLabel(firstName, email)

        # Create our pie chart on our home screen
        # Create a box layout
        vbox = QVBoxLayout()
        # Call our helper method to setup our pie chart
        chartview = self.donutChart(firstName, email)
        # Add our chart view to our box layout
        vbox.addWidget(chartview)
        # Make our groupBox border and background clear
        self.groupBox.setStyleSheet("QGroupBox { border: none; background-color: transparent; }")
        # Set the layout of our group box to our box layout
        self.groupBox.setLayout(vbox)

        # Create our income scroll bar
        # Call our incomeScrollBar method
        incomeGroupBox = self.incomeScrollBar(firstName, email)
        # Set the groupBox widget to our income_scroll_bar (The actual scroll bar)
        self.income_scroll_bar.setWidget(incomeGroupBox)

        # Create our expenses scroll bar
        # Call our expensesScrollBar method
        expensesGroupBox = self.expensesScrollBar(firstName, email)
        # Set the groupBox widget to our expenses_scroll_bar (The actual scroll bar)
        self.expense_scroll_bar.setWidget(expensesGroupBox)

        # If our add income button is clicked go to our addIncome method
        self.add_income_button.clicked.connect(lambda: self.addIncome(firstName, email, vbox))
        # If our add expense button is clicked go to our addExpense method
        self.add_expense_button.clicked.connect(lambda: self.addExpense(firstName, email, vbox))

        # If the new month button is clicked create a new month
        self.new_month_button.clicked.connect(lambda: self.newMonth(firstName, email, vbox))

        # If the delete account button is clicked delete the users account
        self.delete_account_button.clicked.connect(lambda: self.deleteAccount(email))
        # If edit info button is clicked go to the edit info method
        self.change_password_button.clicked.connect(lambda: self.editInfo(firstName, email))

    def donutChart(self, firstName, email):
        # Create a pie series for our pie chart
        series = QPieSeries()
        series.setHoleSize(0.35)
        # Create slices for our pie chart
        slice = QPieSlice()
        # Create our pie chart
        chart = QChart()
        # Call our database methods to get income and expenses totals
        income_total = database.databaseMethods.incomeTotal(firstName, email)
        expenses_total = database.databaseMethods.expensesTotal(firstName, email)
        # Add our totals to our donut chart
        series.append("Income", float(income_total))
        series.append("Expenses", float(expenses_total))
        # Set emploded state for our chart(The slice is seperate from the pie)
        slice.setExploded()
        # Makes the labels visible
        slice.setLabelVisible()
        # Add our pie series to our chart
        chart.addSeries(series)
        # Add animations to make it look cool
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # Set a title for our chart
        chart.setTitle("Overview")
        # Make our background transparent
        chart.setBackgroundBrush(QBrush(QColor("transparent")))
        # Make a chart view and add it to our chart
        chartview = QChartView(chart)
        return chartview
    
    def incomeScrollBar(self, firstName, email):
        # Create a form layout
        incomeFormLayout = QFormLayout()
        # Set our vertical spacing
        incomeFormLayout.setVerticalSpacing(15)
        # Create a groupBox
        incomeGroupBox = QGroupBox("")

        # Get all our data from our database
        income_array = database.databaseMethods.income(firstName, email)
        # Create new arrays
        amount = []
        desc = []
        # Organize the descriptions and amounts into their own lists
        for i in income_array:
            desc.append(i[0])
            amount.append(i[1])
        # Go through description list and create label, format
        for i, num in enumerate(desc):
            string = "      " + num
            desc[i] = QLabel(string)
            desc[i].setStyleSheet("font-family: Times New Roman; font-size: 12pt; color: rgb(78, 211, 96);")
            desc[i].setFixedSize(100, 25)
        # Go through amount list and create label, format
        for i, num in enumerate(amount):
            string = "       $" + str(num)
            amount[i] = QLabel(string)
            amount[i].setStyleSheet("font-family: Times New Roman; font-size: 12pt; color: rgb(78, 211, 96);")
            amount[i].setFixedSize(80, 25)
        # Add each description and amount as a new row in our form layout
        for i in range(len(income_array)):
            incomeFormLayout.addRow(desc[i], amount[i])
        # Add our formLayout to our groupbox
        incomeGroupBox.setLayout(incomeFormLayout)
        return incomeGroupBox
    
    def expensesScrollBar(self, firstName, email):
        # Create a form layout
        expensesFormLayout = QFormLayout()
        # Set our vertical spacing
        expensesFormLayout.setVerticalSpacing(15)
        # Create a groupBox
        expenseGroupBox = QGroupBox("")
        # Get all our data from our database
        expenses_array = database.databaseMethods.expenses(firstName, email)
        # Create new arrays
        amount = []
        desc = []
        # Organize the descriptions and amounts into their own lists
        for i in expenses_array:
            desc.append(i[0])
            amount.append(i[1])
        # Go through description list and create label, format
        for i, num in enumerate(desc):
            string = "      " + num
            desc[i] = QLabel(string)
            desc[i].setStyleSheet("font-family: Times New Roman; font-size: 12pt; color: red;")
            desc[i].setFixedSize(100, 25)
        # Go through amount list and create label, format
        for i, num in enumerate(amount):
            string = "       $" + str(num)
            amount[i] = QLabel(string)
            amount[i].setStyleSheet("font-family: Times New Roman; font-size: 12pt; color: red;")
            amount[i].setFixedSize(80, 25)
        # Add each description and amount as a new row in our form layout
        for i in range(len(expenses_array)):
            expensesFormLayout.addRow(desc[i], amount[i])
        # Add our formLayout to our groupbox
        expenseGroupBox.setLayout(expensesFormLayout)
        return expenseGroupBox

    def homeTotalLabel(self, firstName, email):
        # Call our database methods to get income and expenses totals
        income_total = database.databaseMethods.incomeTotal(firstName, email)
        expenses_total = database.databaseMethods.expensesTotal(firstName, email)
        total = round(income_total - expenses_total, 2)
        if total < 0:
            total = abs(total)
            str_total = "-$" + str(total)
            self.total_money_label.setStyleSheet("background-color: transparent; font-size: 30px; font-family: Times New Roman; color: red;")
        else:
            str_total = "$" + str(total)
            self.total_money_label.setStyleSheet("background-color: transparent; font-size: 30px; font-family: Times New Roman; color: green;")
        self.total_money_label.setText(str_total)

    def incomeTotalLabel(self, firstName, email):
        # Call our database method to get our total
        income_total = database.databaseMethods.incomeTotal(firstName, email)
        # round to 2 decimal points
        income_total = round(income_total, 2)
        # Set our text box to a string of that amount
        self.total_amount_label.setText("$" + str(income_total))

    def expensesTotalLabel(self, firstName, email):
        # Call our database method to get our total
        expenses_total = database.databaseMethods.expensesTotal(firstName, email)
        # round to 2 decimal points
        expenses_total = round(expenses_total, 2)
        # Set our text box to a string of that amount
        self.total_amount_label_2.setText("$" + str(expenses_total))

    def addIncome(self, firstName, email, vbox):
        if self.income_amount_edit.text() == "" or self.income_description_edit.text() == "":
            self.income_error_label.setText("Make sure all boxes are filled out")
        else:
            try:
                # Get our description and amount from our labels
                amount =  float(self.income_amount_edit.text())
                desc = self.income_description_edit.text()
                # Call our database method to store the new transaction
                num = database.databaseMethods.newIncome(firstName, email, amount, desc)
                # If the database method returns -1 or -2 set our error text label
                if num == -1 or amount == None:
                    self.income_error_label.setText("Make sure your amount is a number")
                elif num == -2 or desc == None:
                    self.income_error_label.setText("Make sure your description is present")
                else:
                    self.income_error_label.setText("")
                # Update our income total label
                self.incomeTotalLabel(firstName, email)
                # Update our home total label
                self.homeTotalLabel(firstName, email)

                # Update our donut chart
                # Remove our current donut chart
                vbox.takeAt(0)
                # Call our helper method to setup our pie chart
                chartview = self.donutChart(firstName, email)
                # Add our chart view to our box layout
                vbox.addWidget(chartview)
                # Set the layout of our group box to our box layout
                self.groupBox.setLayout(vbox)

                # Update our income scroll bar
                # Call our incomeScrollBar method
                incomeGroupBox = self.incomeScrollBar(firstName, email)
                # Set the groupBox widget to our income_scroll_bar (The actual scroll bar)
                self.income_scroll_bar.setWidget(incomeGroupBox)
                
                # Clear our text boxes
                self.income_amount_edit.clear()
                self.income_description_edit.clear()
            except:
                self.income_error_label.setText("There seems to be an error, please check data and try again")

    def addExpense(self, firstName, email, vbox):
        # Check if either of our text boxes are blank
        if self.expenses_amount_edit.text() == "" or self.expenses_description_edit.text() == "":
            self.expense_error_label.setText("Make sure all boxes are filled out")
        else:
            try:
                # Get our description and amount from our labels
                amount =  float(self.expenses_amount_edit.text())
                desc = self.expenses_description_edit.text()
                # Call our database method to store the new transaction
                num = database.databaseMethods.newExpense(firstName, email, amount, desc)
                # If the database method returns -1 or -2 set our error text label
                if num == -1 or amount == None:
                    self.expense_error_label.setText("Make sure your amount is a number")
                elif num == -2 or desc == None:
                    self.expense_error_label.setText("Make sure your description is present")
                else:
                    self.expense_error_label.setText("")
                # Update our expenses total label
                self.expensesTotalLabel(firstName, email)
                # Update our home total label
                self.homeTotalLabel(firstName, email)

                # Update our donut chart
                # Remove our current donut chart
                vbox.takeAt(0)
                # Call our helper method to setup our pie chart
                chartview = self.donutChart(firstName, email)
                # Add our chart view to our box layout
                vbox.addWidget(chartview)
                # Set the layout of our group box to our box layout
                self.groupBox.setLayout(vbox)

                # Update our expense scroll bar
                # Call our expenseScrollBar method
                expensesGroupBox = self.expensesScrollBar(firstName, email)
                # Set the groupBox widget to our expense_scroll_bar (The actual scroll bar)
                self.expense_scroll_bar.setWidget(expensesGroupBox)

                # Clear our text boxes
                self.expenses_amount_edit.clear()
                self.expenses_description_edit.clear()
            except:
                self.expense_error_label.setText("There seems to be an error, please check data and try again")

    def newMonth(self, firstName, email, vbox):
        # Call our database methods to clear all the tables in our users database
        database.databaseMethods.clearIncome(firstName, email)
        database.databaseMethods.clearExpenses(firstName, email)
        database.databaseMethods.clearTotalIncome(firstName, email)
        database.databaseMethods.clearTotalExpenses(firstName, email)

        # Update our income total label
        self.incomeTotalLabel(firstName, email)
        # Update our expenses total label
        self.expensesTotalLabel(firstName, email)
        # Update our home total label
        self.homeTotalLabel(firstName, email)

        # Update our donut chart
        # Remove our current donut chart
        vbox.takeAt(0)
        # Call our helper method to setup our pie chart
        chartview = self.donutChart(firstName, email)
        # Add our chart view to our box layout
        vbox.addWidget(chartview)
        # Set the layout of our group box to our box layout
        self.groupBox.setLayout(vbox)

        # Update our income scroll bar
        # Call our incomeScrollBar method
        incomeGroupBox = self.incomeScrollBar(firstName, email)
        # Set the groupBox widget to our income_scroll_bar (The actual scroll bar)
        self.income_scroll_bar.setWidget(incomeGroupBox)

        # Update our expense scroll bar
        # Call our expenseScrollBar method
        expensesGroupBox = self.expensesScrollBar(firstName, email)
        # Set the groupBox widget to our expense_scroll_bar (The actual scroll bar)
        self.expense_scroll_bar.setWidget(expensesGroupBox)

    def accountInfo(self, firstName, email):
        # Set the labels based on the info passed in
        self.first_name_box.setText(firstName)
        self.email_box.setText(email)
        # Get our new data
        lastName, password = database.databaseMethods.myAccount(email)
        # Set the labels of the new data we got
        self.last_name_box.setText(lastName)
        self.password_label_2.setText(password)

    def deleteAccount(self, email):
        # Call the database method to clear the users username and password from our accounts database
        database.databaseMethods.deleteAccount(email)

        # Remove all the stacked widgets
        for i in range(2):
            remove = lwidget.currentWidget()
            lwidget.removeWidget(remove)
            lwidget.setCurrentIndex(lwidget.currentIndex() - 2)

    def editInfo(self, firstName, email):
        global edit_var
        # Create an instance of the editInfo class
        edit_var = editInfo(email)
        edit_var.show()

# Class for our popup window for the user to edit their personal info
class editInfo(QMainWindow):
    # Inititalization method
    def __init__(self, email):
        super().__init__() 
        # Set our email variable
        self.email = email
        # Load our user interface
        uic.loadUi('editInfoPopup.ui', self)

        # Set the password field so we can't see the text
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # If user clicked Edit Password button then go to our database method
        self.change_password_button.clicked.connect(lambda: self.edit(email))

    def edit(self, email):
        # Get the info from the password boxes
        newPassword = self.password_edit.text().replace(" ", "")
        confirmPassword = self.confirm_password_edit.text().replace(" ", "")
        # Make sure the password is not empty
        if newPassword == "" or confirmPassword == "":
            # Display an error message
            self.error_label.setText("Please enter a new password")
        # Check to make sure they are the same
        elif newPassword == confirmPassword:
            # Clear our error label
            self.error_label.setText("")
            # Call our database method to update the users information
            database.databaseMethods.editInfo(email, password=newPassword)
            # Close the window
            self.close()
        else:
            # Display an error message
            self.error_label.setText("Please make sure your passwords match")




# Main Program Creation Code
# Create our QApplication
app = QApplication(sys.argv)
# Create and instance of our welcome screen
welcome = welcomeScreen()
# Create our stacked widget instance
lwidget = QStackedWidget()
# Add our welcome widget to our stacked widget
lwidget.addWidget(welcome)
# Set fixed height and width of our application
lwidget.setFixedHeight(600)
lwidget.setFixedWidth(800)
# Show our stacked widget instance
lwidget.show()
# Close our application
sys.exit(app.exec_())
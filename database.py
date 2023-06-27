# Title: Personal Finance App
# File: Database Retrieval/Storage File
# Date: June 2023
# Author: Nick Mast

# This is the database file for our app. This file reads and writes from and to our SQLite database
# This file uses SQLite3 to write and read data
import sqlite3, os
class databaseMethods():

    # Method to verify the email and password of a user trying to login
    def login(email, password):
        # Create a connection to our database file
        conn = sqlite3.connect('accounts.db')
        # Create a cursor
        cursor = conn.cursor()
        # If either of our fields are empty then return 0
        if len(email) == 0 or len(password) == 0:
            conn.close()
            return 0
        # Try to execute a statement on the accounts table to see if it exists or not, if not return -1
        try:
            cursor.execute("SELECT * FROM accounts WHERE email=:email", {'email':email})
        except:
            conn.close()
            return -1
        # Retrieve our found email from our cursor
        found_email = cursor.fetchone()
        # If our found_email is nothing return -1
        if found_email is None:
            conn.close()
            return -1
        else:
            # Get the password associated with the email
            found_password = found_email[3]
            # If the passwords match return 1, if not return -1
            if found_password == password:
                conn.close()
                return 1
            conn.close()
            return -1

    # Method to get a new user signed up and in the database when they signup for an account
    def signup(firstName, lastName, email, password, confirmPassword):
        # Create a connection to our database file
        conn = sqlite3.connect('accounts.db')
        # Create a cursor
        cursor = conn.cursor()
        # If the passwords do not match return -1
        if password != confirmPassword:
            conn.close()
            return -1
        # If any of the fields are empty return 0
        if len(firstName) == 0 or len(lastName) == 0 or len(email) == 0 or len(password) == 0 or len(confirmPassword) == 0:
            conn.close()
            return 0
        # Try to execute a statement on our table, if there is not one then create one
        try:
            cursor.execute("SELECT * FROM accounts WHERE email=:email", {'email':email})
        except:
            cursor.execute("""CREATE TABLE accounts (firstName text, lastName text, email text, password text)""")
        # Check to see if the email the user input is already in our table
        cursor.execute("SELECT * FROM accounts WHERE email=?", (email,))
        alr_present = cursor.fetchone()
        if alr_present:
            alr_present = alr_present[0]
            if alr_present == email:
                conn.close()
                return -2
        # If all is good so far execute our insert staement to insert our data into the accounts table
        cursor.execute("INSERT INTO accounts VALUES (:firstName, :lastName, :email, :password)", {'firstName':firstName, 'lastName':lastName, 'email':email, 'password':password})
        # Create a new db file for the user
        databaseMethods.newUserFile(firstName, email)
        # Commit our changes, close the connection and return 1
        conn.commit()
        conn.close()
        return 1

    # Method for when a new user creates an account. This method create a personal db file for the new user
    def newUserFile(firstName, email):
        # Create the file name
        file_name = firstName + "_" + email + ".db"
        # Create the file
        conn = sqlite3.connect(file_name)
        # Create a cursor in the file
        cursor = conn.cursor()
        # Create new tables in the new file for income, expenses, and totals
        cursor.execute("""CREATE TABLE income (description text, amount real)""")
        cursor.execute("""CREATE TABLE expenses (description text, amount real)""")
        cursor.execute("""CREATE TABLE incomeTotal (amount real)""")
        cursor.execute("""CREATE TABLE expensesTotal (amount real)""")
        # Update the incomeTotal and expensesTotal values to hold $0.00
        value = 0.00
        cursor.execute("INSERT INTO incomeTotal (amount) VALUES (ROUND(?, 2))", (value,))
        cursor.execute("INSERT INTO expensesTotal (amount) VALUES (ROUND(?, 2))", (value,))
        conn.commit()
        conn.close()

    # Method to get the firstname of the user to display on the home screen
    def firstName(email):
        # Create connection
        conn = sqlite3.connect('accounts.db')
        # Create a cursor
        cursor = conn.cursor()
        # Return all lines that has our specified email
        cursor.execute("SELECT * FROM accounts WHERE email=?", (email,))
        # Store the first line returned into the first_name variable
        first_name = cursor.fetchone()
        # If first_name exists get the first index of the row which is the users first name, else return -1
        if first_name:
            first_name = first_name[0]
        else:
            conn.close()
            return -1
        # Close connection
        conn.close()
        # Return the first name we found
        return first_name
    
    # Method to update our incomeTotal database table
    def updateIncomeTotal(firstName, email, form_amount):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get our current total
        cursor.execute("SELECT * FROM incomeTotal")
        total = cursor.fetchone()
        total = total[0]
        # Update our total
        total += float(form_amount)
        # Save our new total amount
        cursor.execute("UPDATE incomeTotal SET amount = ? WHERE rowid = 1", (total,))
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

    # Method to update our expensesTotal database table
    def updateExpenseTotal(firstName, email, form_amount):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get our current total
        cursor.execute("SELECT * FROM expensesTotal")
        total = cursor.fetchone()
        total = total[0]
        # Update our total
        total += float(form_amount)
        # Save our new total amount
        cursor.execute("UPDATE expensesTotal SET amount = ? WHERE rowid = 1", (total,))
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()
    
    # Method to get all the income transactions from our table
    def income(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get all the transactions
        cursor.execute("SELECT * FROM income")
        # Fetch all the rows from the result
        rows = cursor.fetchall()
        conn.close()
        # Put our data into a list and return
        income_array = [list(row) for row in rows]
        return income_array


    # Method to get all the expense transactions from our table
    def expenses(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get all the transactions
        cursor.execute("SELECT * FROM expenses")
        # Fetch all the rows from the result
        rows = cursor.fetchall()
        conn.close()
        # Put our data into a list and return
        expenses_array = [list(row) for row in rows]
        return expenses_array

    # Method to get our income total
    def incomeTotal(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get the total from our totalIncome table and return it
        cursor.execute("SELECT * FROM incomeTotal")
        total = cursor.fetchone()
        conn.close()
        return total[0]

    # Method to get our expenses total
    def expensesTotal(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get the total from our totalIncome table and return it
        cursor.execute("SELECT * FROM expensesTotal")
        total = cursor.fetchone()
        conn.close()
        return total[0]
    
    # Method to add new income to our database
    def newIncome(firstName, email, amount, desc):
        # Make sure our amount is a number and our description is a string
        if not isinstance(amount, (int, float)):
            return -1
        elif not isinstance(desc, (str)):
            return -2
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Make our number into a 2 decimal place number
        form_amount = "{:.2f}".format(amount)
        # Add amount and desc to database
        cursor.execute("INSERT INTO income VALUES (:description, :amount)", {'description':desc, 'amount':form_amount})
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()
        # Update our incomeTotal table
        databaseMethods.updateIncomeTotal(firstName, email, form_amount)
        return 1
    
    # Method to add new expense to our database
    def newExpense(firstName, email, amount, desc):
        # Make sure our amount is a number and our description is a string
        if not isinstance(amount, (int, float)):
            return -1
        elif not isinstance(desc, (str)):
            return -2
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Make our number into a 2 decimal place number
        form_amount = "{:.2f}".format(amount)
        # Add amount and desc to database
        cursor.execute("INSERT INTO expenses VALUES (:description, :amount)", {'description':desc, 'amount':form_amount})
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()
        # Update our incomeTotal table
        databaseMethods.updateExpenseTotal(firstName, email, form_amount)
        return 1
    
    # Method to clear our income in our database
    def clearIncome(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Clear our data in our table
        cursor.execute("DELETE FROM income")
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

    # Method to clear our expenses from our database
    def clearExpenses(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Clear our data in our table
        cursor.execute("DELETE FROM expenses")
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

    # Method to set our income total to 0
    def clearTotalIncome(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get our total amount and set to 0
        total = 0
        # Save our new total amount
        cursor.execute("UPDATE IncomeTotal SET amount = ? WHERE rowid = 1", (total,))
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

    # Method to set our expenses total to 0
    def clearTotalExpenses(firstName, email):
        # Get the file name
        file_name = firstName + "_" + email + ".db"
        # Create connection
        conn = sqlite3.connect(file_name)
        # Create a cursor
        cursor = conn.cursor()
        # Get our total amount and set to 0
        total = 0
        # Save our new total amount
        cursor.execute("UPDATE expensesTotal SET amount = ? WHERE rowid = 1", (total,))
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

    # Method to delete the users account from our database
    def deleteAccount(email):
        # Create connection
        conn = sqlite3.connect('accounts.db')
        # Create a cursor
        cursor = conn.cursor()
        # Delete our users line from our accounts database
        cursor.execute("DELETE FROM accounts WHERE email = ?", (email,))
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

    # Method to get our info for our My Account page
    def myAccount(email):
        # Create connection
        conn = sqlite3.connect('accounts.db')
        # Create a cursor
        cursor = conn.cursor()
        # Operation to get the users line in the database
        cursor.execute("SELECT * FROM accounts WHERE email = ?", (email,))
        user = cursor.fetchone()
        # Get the users lastName and password
        lastName = user[1]
        password = user[3]
        return lastName, password
    
    def editInfo(email, password):
        # Create connection
        conn = sqlite3.connect('accounts.db')
        # Create a cursor
        cursor = conn.cursor()
        # Update the users info
        cursor.execute("UPDATE accounts SET password = ? WHERE email = ?", (password, email,))
        # Commit the current transaction to the file
        conn.commit()
        # Close the connection
        conn.close()

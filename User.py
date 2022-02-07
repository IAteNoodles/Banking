import tkinter as Tk
from tkinter import *
from tkinter import messagebox
from mysql import connector

from Bank import Account, Current, Savings, User
from TFA import check_2fa

def functions(account_id: str, account_type: int):
    root = Tk()
    root.title("User Panel")
    root.geometry("750x500")
    main_frame = Frame(root)
    main_frame.pack(expand=True, fill = BOTH)
    
    account : Account
    if account_type == 0:
        account = Savings(account_id)
    else:
        account = Current(account_id)
   
    _labelFrame["Balance"] = LabelFrame(main_frame, text="Balance", fg="green")
    _entry["Balance"] = Entry(_labelFrame["Amount"])
    _labelFrame["Amount"] = LabelFrame(main_frame, text="Amount", fg="blue")  
    _entry["Amount"] = Entry(_labelFrame["Amount"])
    
    #This fetches the balance of the account and saves it in the dictionary, for later.
    def fetch_balance():
        datasource.execute("SELECT BALANCE FROM ACCOUNT WHERE ID = '%s'" %account.__ID)
        account.__BALANCE = int(datasource.fetchone()[0])   
        Label(_labelFrame["Balance"], text=account.__BALANCE).pack()
        _labelFrame["Balance"].pack(expand=True, fill = BOTH)
        
    #This deposites money into the account and update the _account_data key.
    def deposit():
        _entry["Amount"].pack()
        _labelFrame["Amount"].pack(expand=True, fill=BOTH)
        amount = int(_entry["Amount"].get())
        if amount < 0:
            messagebox.showerror("Error", "Your entered amount is invalid. Please try again")
            return
        account.__BALANCE += amount
        datasource.execute("UPDATE ACCOUNT SET BALANCE = %s WHERE ID = '%s'" % (account.__BALANCE, account.__ID))
        connector.commit()
        
    #This withdraws money into the account and update the _account_data key.
    def withdraw():
        _entry["Amount"].pack()
        _labelFrame["Amount"].pack(expand=True, fill=BOTH)
        amount = int(_entry["Amount"].get())
        if amount < 0:
            messagebox.showerror("Error", "Your entered amount is invalid. Please try again")
            return
        account.__BALANCE -= amount
        datasource.execute("UPDATE ACCOUNT SET BALANCE = %s WHERE ID = '%s'"%account.__BALANCE, account.__ID)
        connector.commit()
        
    def fetch_transaction():
        temp = account.fetch_transaction(25)
        if len(temp) == 0:
            messagebox.showerror("Error", "No transaction found for this account")
        else:
            transaction_Window = Toplevel(root)
            transaction_Window.title("Transaction History")
            import tktable
            
            
            
    Button(main_frame, text="Check Balance",command=fetch_balance).pack()
    Button(main_frame, text="Deposit", command=deposit).pack()
    Button(main_frame, text="Withdraw", command=withdraw).pack()
    Button(main_frame, text="Check Transaction", command=fetch_transaction).pack()
    pass
def welcome():
    root = Tk()
    root.title("User Panel")
    root.geometry("750x500")
    welcome_frame = Frame(root)
    welcome_frame.pack(expand=True, fill=BOTH)
    #Creating _labelFrame and _entry for User ID and Social Security Number.

    _labelFrame["User ID"] = LabelFrame(welcome_frame, text="User ID", fg="green")
    _entry["User ID"] = Entry(_labelFrame["User ID"])
    _labelFrame["Social Security Number"] = LabelFrame(welcome_frame, text="Social Security Number", fg="green")
    _entry["Social Security Number"] = Entry(_labelFrame["Social Security Number"])
    
    #Packing User ID and Social Security Number
    
    _labelFrame["User ID"].pack(expand=True, fill=BOTH)
    _labelFrame["Social Security Number"].pack(expand=True, fill=BOTH)
    _entry["User ID"].pack()
    _entry["Social Security Number"].pack()
    
    #Packed User ID and Social Security Number.
    
    #Creating login interface for User.
    def login_user():
        _user_data["User ID"] = _entry["User ID"].get()
        _user_data["Social Security Number"] = _entry["Social Security Number"].get()
        _user_data["Panel"]=User(_user_data["User ID"], _user_data["Social Security Number"])
        if not _user_data["Panel"].__VERIFIED:
            messagebox.showerror("Login failed", "Given credentials didn't match")
        else:
            #select account and use function
            print("You are logged in")
    
    #Creating helping interface for User.
    def askhelp():
        welcome_frame.destroy()
        help_frame = Frame(root)
        help_frame.pack(expand=True, fill=BOTH)
        help = LabelFrame(help_frame, text="Select your problem", fg="blue")
        help.pack(expand=True, fill=BOTH)
        
        #Recovering Credentials.
        def recover_number():
            import TFA
            if not "USER ID" in _user_data:
                
                _labelFrame["User ID"] = LabelFrame(help_frame, text="User ID", fg="red")
                _entry["User ID"] = Entry(_labelFrame["User ID"])
                _entry["User ID"].pack()
                _labelFrame["User ID"].pack()
                
            #Fetching the 2FA Token from database.
            
            def validate_otp():
                _user_data["User ID"] = _entry["User ID"].get()
                datasource.execute("SELECT 2FA_TOKEN_ID FROM PEOPLE WHERE UNIQUE_ID = '{uid}'".format(uid=_user_data["User ID"]))
                secret = datasource.fetchone()[0]
                otp_frame = LabelFrame(help_frame, text="OTP", fg="blue")
                otp_frame.pack(expand=True, fill=BOTH)
                otp = Entry(otp_frame)
                otp.pack()
                if check_2fa(secret, otp.get()):
                    print("Pass")
                else:
                    print("Fail")
                    
            Button(help_frame, text="Submit", command=validate_otp).pack()    
        Button(help, text="Forgot your Social Security Number?", command=recover_number).pack()
        
        #Recovering Credentials.
        def recover_id():
            _labelFrame["Contact"] = LabelFrame(help_frame, text="Email/Phone", fg="red")
            _entry["Contact"] = Entry(_labelFrame["Contact"])
            _labelFrame["Contact"].pack(expand=True, fill=BOTH)
            _entry["Contact"].pack()
            _labelFrame["Social Security Number"] = LabelFrame(help_frame, text="Social Security Number", fg="green")
            _entry["Social Security Number"] = Entry(_labelFrame["Social Security Number"])
            _labelFrame["Social Security Number"].pack(expand=True, fill=BOTH)
            _entry["Social Security Number"].pack()
            
            def get_id():
                _user_data["Social Security Number"] = _entry["Social Security Number"].get()
                datasource.execute("SELECT UNIQUE_ID FROM PEOPLE WHERE EMAIL = '{contact}' or PHONE_NUMBER = '{contact}'".format(contact=_entry["Contact"].get()))
                temp = datasource.fetchone()
                if temp is None:
                    messagebox.showerror("Failed to recover ID", "No ID match with the given credentials")
                else:
                    messagebox.showinfo("Sucessfully recovered ID", "Your ID is: {}".format(temp))
                    
            Button(help_frame, text="Submit", command = get_id).pack()
        Button(help, text="Forgot your User ID?", command=recover_id).pack()
        #Button(help, text="Can't access your phone/email?", command=lost_details).pack()
        
    login_button = Button(root, text="Login into your your user panel", fg="green", command=login_user)
    login_button.pack()
    need_help = Button(root, text="Need help?", fg="blue", command=askhelp)
    need_help.pack()
    root.mainloop()

#All the childrens will be stored in these variables to ease access and naming.
_labelFrame = dict()
_entry = dict()
#This dict will contain the most recalled variables.
_user_data = dict()
connection = connector.connect(user="user_bank", host="localhost", password="USER@BANK", database="Bank")
global datasource
datasource = connection.cursor()
welcome()
connector.commit()
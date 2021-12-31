from mysql import connector 
from tkinter import *
from tkcalendar import Calendar, DateEntry
from Bank import ROOT, Staff, Supervisor
from tkinter import messagebox                    
                    


def welcome(root: Tk):
    welcome_frame=Frame(root)
    welcome_frame.pack()
    _id = LabelFrame(welcome_frame, text="Admin ID:", fg="red")
    _id.pack(expand=True, fill="both")
    Id = Entry(_id)
    _passwd = LabelFrame(welcome_frame, text="Password:", fg="red")
    _passwd.pack(expand=True, fill="both")
    Password = Entry(_passwd)
    Id.pack()
    Password.pack()
    def login():
        """
        Handles the login process

        Once both ID and Password are entered, this function checks if an admin exists with the given ID, and if it does,
        then it checks if the hash of the password matches with the hash of the admin in login table. Otherwise it returns
        an Toplevel object with the appropriate error message.
        """
        id = Id.get()
        password = Password.get()
        datasource.execute(r"SELECT TYPE FROM ADMIN WHERE ADMIN_ID = '%s'"%id)
        result = datasource.fetchone()
        if result is None:
                messagebox.showerror("Login failed","No admin with the given ID exists")
        else: 
            if result[0] == "STAFF":
                admin = Staff(id, password)
            elif result[0] == "MODERATOR":
                admin = Supervisor(id, password)
            else:
                admin = ROOT(id, password)   
            if not admin._Staff__VERIFIED:
                messagebox.showerror("Invalid Credentials!!!", "Either the ID or the password are incorrect. Please try again")
            else:
                #Admin has been verified successfully.
                welcome_frame.destroy()
                admin_frame = Frame(root)
                admin_frame.pack()
                _type = admin._Staff__TYPE
                color = "green" if _type == "STAFF" else "blue" if _type == "MODERATOR" else "red"
                _Actions = list()
                #List of actions that can be performed by the admin. (STAFF)
                _Actions.append("Check Transaction") 
                _Actions.append("Track Application")
                _Actions.append("Modify Application")
                _Actions.append("Delete Application")
                
                #List of actions that can be performed by the admin. (MODERATOR)
                if admin.ISSUPERVISOR:
                    _Actions.append("Create User")
                    _Actions.append("Modify User Date")
                    _Actions.append("Delete User")
                    _Actions.append("Create Admin")
                    _Actions.append("Modify Admin Date")
                    
                #List of actions that can be performed by the admin. (ROOT)
                    
                if admin.ISROOT:
                    _Actions.append("Delete Admin")
                    
                def check():
                    track_frame = Frame(root)
                    track_frame.pack(expand=True, fill="both")
                    track_lFrame = LabelFrame(track_frame, text="Application ID")
                    track_lFrame.pack(expand=True, fill="both")
                    _id = Entry(track_lFrame)
                    _id.pack()
                    def track():
                        details = iter(admin.track_application(_id.get()))
                        _details = LabelFrame(track_frame, text="Details for Application ID: %s"% _id.get(), fg="green")
                        _details.pack(expand=True, fill="both")
                        _details_date = PanedWindow(_details,orient="vertical")
                        _details_info = PanedWindow(_details,orient="vertical")
                        _dc = Label(_details_date, text=details.__next__())
                        _dc.pack(side= TOP)
                        _dlm = Label(_details_date, text=details.__next__())
                        _dlm.pack(side= TOP)
                        _details_date.add(_dc)
                        _details_date.add(_dlm)
                        _details_date.pack(expand=True, fill=BOTH)
                        _ds = Label(_details_info, text=details.__next__())
                        _ds.pack(side= TOP)
                        _dr = Label(_details_info, text=details.__next__())
                        _dr.pack(side=TOP)
                        _details_info.add(_ds)
                        _details_info.add(_dr)
                        _details_info.pack(expand=True, fill=BOTH)
                        
                    Button(track_lFrame, text="Track Application", command=track).pack()
                Button(admin_frame, text="Check Application", command=check).pack()

                def check_transaction():
                    transaction_frame = Frame(root)
                    transaction_frame.pack(expand=True, fill=BOTH)
                    tracking_window = Toplevel(root)
                    tracking_window.geometry("400x400")
                    def track_id():
                        tracking_window.title("Track Transaction ID")
                        lFrame = LabelFrame(tracking_window, text="Transaction ID", fg="green")
                        lFrame.pack(expand=True, fill=BOTH)
                        transaction_id = Entry(tracking_window)
                        transaction_id.pack(expand=True, fill=BOTH)
                        def track():
                            Tk.Separator(tracking_window,orient='horizontal').pack()
                            datasource.execute("SELECT * FROM TRANSACTION WHERE TRANSACTION_ID = {trid}".format(trid=transaction_id.get()))
                            temp = datasource.fetchone()
                            if temp is None:
                                messagebox.showerror("Error", "No transaction with such transaction id was found.")
                            else:
                                by, to, amount, time = temp
                                fromLFrame = LabelFrame(lFrame, text="From", fg="green")
                                fromLFrame.pack(fill=BOTH, expand=True)
                                Label(fromLFrame, text=by).pack()
                                toLFrame = LabelFrame(lFrame, text="To", fg="green")
                                toLFrame.pack(fill=BOTH, expand=True)
                                Label(toLFrame, text=to).pack()
                                exchangeLFrame = LabelFrame(lFrame, text="Amount",fg="green")
                                exchangeLFrame.pack(fill=BOTH,expand=True)
                                Label(exchangeLFrame, text=amount).pack()
                                timelFrame = LabelFrame(lFrame, text="Time", fg="green")
                                timelFrame.pack(fill=BOTH, expand=True)
                                Label(timelFrame, text=time).pack()
                            
                        Button(tracking_window, text="Track", command=track, fg="green")
                    
                    def track_account():
                        tracking_window.title("Track Account")
                        lFrame = LabelFrame(tracking_window, text="Account ID:", fg="blue")
                        lFrame.pack(fill=BOTH, expand=True)
                        account_id = Entry(tracking_window)
                        account_id.pack(expand=True, fill=BOTH)
                        datasource.execute("SELECT * FROM TRANSACTION WHERE BY = '{acc_id}' OR TO = '{acc_id}'".format(acc_id = account_id.get()))
                        temp = datasource.fetchall()
                        if temp is None:
                            messagebox.showwarning("No records found.", "Either no transaction with the given account have taken place or the account id is invalid. Please check and try again.")
                        else:
                            tran_no = len(temp)
                            global first_tran, last_tran
                            last_tran = 25
                            first_tran = 0
                            def show():
                                global last_tran, first_tran
                                for count in range(first_tran,last_tran):
                                    id, by, to, amount, time = temp[count]
                                    if by == account_id.get():
                                        statement = "{sender} sent {money} to {to}".format(sender = by, money =amount, to = to) 
                                    else:
                                        statement = "{to} received {money} from {sender}".format(sender = by, money =amount, to = to)
                                    tLFrame = LabelFrame(tracking_window, text = "Transaction ID : %s" % id, fg = "blue")
                                    tLFrame.pack(fill=BOTH, expand=True)
                                    Label(tLFrame, text = statement).pack()
                                    Label(tLFrame, text="Time : %s" % time).pack()
                                    Tk.Separator(tracking_window,orient='horizontal').pack()
                                    if first_tran >= tran_no:
                                        return
                                
                                first_tran = last_tran+1
                                last_tran += 25
                                    
                            recordFrame = LabelFrame(tracking_window, text= "Displaying records: {first_tran} out of {tran_no}".format(first_tran=first_tran,tran_no=tran_no))
                            recordFrame.pack(fill=BOTH, expand=True)
                            if first_tran < tran_no:
                                Button(tracking_window, text="Next", command = show, fg="green").pack()
                    Button(transaction_frame, text="Details of Transaction with an Transaction ID", command=track_id).pack()
                    Button(transaction_frame, text="Latest transaction of an account", command=track_account).pack()
                _LabelActions = list()
                #List of all the LabelFrames; Parent to the Buttons that can be clicked.
                for action in _Actions:
                    _LabelActions.append(LabelFrame(admin_frame, text=action, fg=color))
                
                #Packing all the LabelFrames.
                for lFrames in _LabelActions:
                    lFrames.pack()                
                    
    login_button = Button(welcome_frame, text="Login", command=login)       
    login_button.pack()
    def Recover():
        """
        Sets up a new admin credentials if the given admin can provide enough information.

        This function will send an application after taking enough information from the admin.
        This application will then be reviewed a top-level executive and a temporary password will be assigned to the admin.
        Once the admin has successfully logged in the function will ask for a new password and update the database.

        Returns:
            str: This will be the application_id which can be used to check the status of a previously submitted application.
        """
        welcome_frame.destroy()
        Recovery_Frame = Frame(root)
        Recovery_Frame.pack()
        Application_New = LabelFrame(Recovery_Frame, text="New Application", fg="blue")
        Application_Old = LabelFrame(Recovery_Frame, text="Previous Application", fg="green")
        Application_New.pack(expand=True, fill='both')
        Application_Old.pack(expand=True, fill='both')  
        
        #This will accept details from the admin.
        def fill_application():
            """
            Takes the needed user data. 
            
            Generates a form that asks the admin for the required details and checks if any box has been left blank.
            If no, then it sends the details for a server-side verification and if details match, an application is created and the Reference ID is send to the email provided by the admin in the Community Record (People Table)
            """
            Recovery_Frame.destroy()
            Form = Frame(root)
            Form.pack(expand=True, fill='both')
            _labelFrame = list() #List of LabelFrame objects for the form.
            _labelNames = ["Unique ID", "First Name", "Middle Name", "Last Name", "Phone Number", "Email Address", "Date of Birth", "Admin ID", "Admin Type"]
            #List of all the Names for the LabelFrame objects.
            _Entry = list()
            #List of all the Entry objects for the LabelFrame objects.
            count = 0
            for name in _labelNames:
                _fg = "blue"
                if "Admin" in name:
                    _fg = "red"
                _labelFrame.append(LabelFrame(Form, text=name, fg=_fg, labelanchor="n"))
                if count == 6:
                    _Entry.append(DateEntry(_labelFrame[6]))
                elif count == 8:
                    types = {"STAFF","MODERATOR"}
                    default = StringVar(_labelFrame[8])
                    default.set("STAFF")
                    _Entry.append(OptionMenu(_labelFrame[8],default,*types))
                     
                else:
                    _Entry.append(Entry(_labelFrame[count]))
                    
                _labelFrame[count].pack(expand=True, fill='both')
                _Entry[count].pack()
                count += 1
            #This will create LabelFrame and will pack then as well as append.
            del count
            def submit():
                """
                Matches the data provided to the data in the  database.

                Once the form is submitted, before being send to the database for the verification, the details are matched to the database.
                If no errors are found, then a ticket is created. The Tracking ID is sent to the provided email address.
                """
                _Iterator = iter(_Entry)
                _uuid = _Iterator.__next__().get()
                _name = (str(_Iterator.__next__().get()),str(_Iterator.__next__().get()),str(_Iterator.__next__().get()))
                _p_n = _Iterator.__next__().get()
                _email = _Iterator.__next__().get()
                _dob = _Iterator.__next__().get_date()
                _id = _Iterator.__next__().get()
                admin_type = default.get()
                if "" in locals().values():
                    messagebox.showerror("Error", "All the fields are required.")
                    for count in range(9):
                        if count == 6 or count == 8:
                            continue
                        if not _Entry[count].get() == "":
                            _Entry[count].delete(0, END)
                else:
                    datasource.execute("SELECT EXISTS(SELECT * from RECOVERY_TABLE WHERE ADMIN_ID = '%s')" % (_id))
                    datasource.execute("SELECT UNIQUE_ID FROM ADMIN WHERE ADMIN_ID = '{id}' AND TYPE = '{admin_type}'".format(id=_id,admin_type=admin_type))
                    test = datasource.fetchone()
                    if _uuid in test:
                        datasource.execute("SELECT FIRST_NAME, MIDDLE_NAME, LAST_NAME FROM PEOPLE WHERE UNIQUE_ID = '{uuid}'".format(uuid=_uuid))
                        test = datasource.fetchone()
                        if _name == test:
                            datasource.execute("SELECT PHONE_NUMBER, EMAIL FROM PEOPLE WHERE UNIQUE_ID = '{uuid}'".format(uuid=_uuid))
                            if _p_n and _email in datasource.fetchone():
                                import secrets
                                _token = secrets.token_urlsafe(16)
                                print(len(_token))
                                datasource.execute("INSERT INTO RECOVERY_TABLE (ID, ADMIN_ID, CREATION_TIME, STATUS) VALUES ('{token}','{id}',NOW(),'PENDING')".format(token=_token,id=_id))
                                import email_client 
                                message = "Use this ID for future reference."
                                htmlPart = """Your account recovery application has been created and is now send for verification. Once it has been approved, you will recieve another email regarding future procedures.\n
                                Your Recovery_ID for future reference is: <big>{token}</big>""".format(token=_token)
                                email_client.send_mail(_email,_name[0],"Your Admin Recovery ID",message, htmlPart, "Admin@Recovery{id}".format(id=_id))
                            
                    messagebox.showinfo("Admin Recovery","If the details you have entered are correct, check your email for the Reference ID.")
        
            Button(Form, text="Submit", command=submit).pack()
            Form.pack(expand=True, fill='both')
        Button(Application_New, text="Fill a new application", command=fill_application).pack()
        
        def check_status():
            Recovery_Frame.destroy()
            application = Frame(root)
            application.pack()
            _form = LabelFrame(application, text="Application Id", fg="green")
            _form.pack(expand=True, fill='both')
            app_id = Entry(_form)
            app_id.pack()
            def fetch():    
                _id = app_id.get()
                datasource.execute("SELECT  STATUS FROM RECOVERY_TABLE WHERE ID = '{id}'".format(id=_id))
                status = datasource.fetchone()
                if not status is None:
                    status = status[0]
                else:
                    status = "No application found with the given ID."
                    application.destroy()
                    if messagebox.askretrycancel("No application found with the given", "Check your email for the Application ID and try again.") == True:
                        check_status()
                    welcome(root)
            Button(application, text="Check", command=fetch).pack()
        Button(Application_Old, text="Check the status of your application", command=check_status).pack()
    Button(welcome_frame, text="Forgot Password", command=Recover).pack()
    root.mainloop()
    
if __name__ == "__main__":
    global datasource
    database = connector.connect(user="python",passwd="Python",database="Bank", host="localhost")
    datasource = database.cursor()
    TK_ROOT = Tk()
    TK_ROOT.title("Admin Panel")
    TK_ROOT.geometry("750x500")
    admin: Staff
    welcome(TK_ROOT)
    database.commit()

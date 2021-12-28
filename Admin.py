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
                Error = Toplevel(root)
                Error.geometry("400x20")
                Error.title("Login failed!!!")
                Label(Error, text="No Admin exists in the database with the given ID.").pack()
        else: 
            if result[0] == "STAFF":
                admin = Staff(id, password)
            elif result[0] == "MODERATOR":
                admin = Supervisor(id, password)
            else:
                admin = ROOT(id, password)   
            if not admin._Staff__VERIFIED:
                Error = Toplevel(root)
                Error.geometry("400x20")
                Error.title("Invalid Credentials!!!")
                Label(Error, text="THe given credentials are invalid.")  
    admin: Staff
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
            count = 0
            for name in _labelNames:
                _fg = "blue"
                if "Admin" in name:
                    _fg = "red"
                _labelFrame.append(LabelFrame(Form, text=name, fg=_fg, labelanchor="n"))
                _labelFrame[count].pack(expand=True, fill='both')
                count += 1
            #This will create LabelFrame and will pack then as well as append.
            del count

            unique_id = Entry(_labelFrame[0])
            unique_id.pack()

            admin_first_name = Entry(_labelFrame[1])
            admin_first_name.pack()
            
            admin_middle_name = Entry(_labelFrame[2])            
            admin_middle_name.pack()
            
            admin_last_name = Entry(_labelFrame[3])
            admin_last_name.pack()

            admin_p_n = Entry(_labelFrame[4])
            admin_p_n.pack()

            admin_email = Entry(_labelFrame[5])
            admin_email.pack()
            
            admin_dob = DateEntry(_labelFrame[6])
            admin_dob.pack()
            date = admin_dob.get_date()
            
            admin_id = Entry(_labelFrame[7])
            admin_id.pack()
            
            types = {"STAFF","MODERATOR"}
            default = StringVar(_labelFrame[8])
            default.set("STAFF")
            admin_types = OptionMenu(_labelFrame[8],default,*types)
            admin_types.pack()
            

            def submit():
                """
                Matches the data provided to the data in the  database.

                Once the form is submitted, before being send to the database for the verification, the details are matched to the database.
                If no errors are found, then a ticket is created. The Tracking ID is sent to the provided email address.
                """
                _uuid = unique_id.get()
                _name = (admin_first_name.get(), admin_middle_name.get(), admin_last_name.get())
                _id = admin_id.get()
                _p_n = admin_p_n.get()
                _email = admin_email.get()
                admin_type = default.get()
                if "" in locals().values():
                    messagebox.showerror("Error", "All the fields are required.")
                    for key in locals().keys():
                        if "" in locals()[key]:
                            continue
                        locals()[key].delete(0, END)
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
                            htmlPart = """Your account recovery application has been created and is now send for verification. Once it has been approved, you will recieve another email regarding future procedures.
                            <big>Your Recovery_ID for future reference is: {token}</big>".format(token=_token)"""
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
                    if messagebox.askretrycancel("No application found with the given", "Check your email for the Application ID and try again.") == True:
                        application.destroy()
                        check_status()
                    application.destroy()
                    welcome(root)
            Button(application, text="Check", command=fetch).pack()
        Button(Application_Old, text="Check the status of your application", command=check_status).pack()
    Button(welcome_frame, text="Forgot Password", command=Recover).pack()
    root.mainloop()
    #return admin
    
if __name__ == "__main__":
    global datasource
    database = connector.connect(user="python",passwd="Python",database="Bank", host="localhost")
    datasource = database.cursor()
    TK_ROOT = Tk()
    TK_ROOT.title("Admin Panel")
    TK_ROOT.geometry("750x500")
    welcome(TK_ROOT)
    database.commit()


"""import gi

gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository import Notify

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Banking Management System - Admin")
        Gtk.Window.set_default_size(self, 640, 480)
        Notify.init("Admin")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
       
        Admin_label = Gtk.Label()
        Admin_label.set_markup(
            "<big>Admin Login Panel</big>")
        #Admin_label.set_halign(Gtk.Align.CENTER)
        #Admin_label.set_valign(Gtk.Align.CENTER)
        self.box.pack_start(Admin_label, True, True,0)
        self.button = Gtk.Button(label="Login")
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.set_valign(Gtk.Align.CENTER)
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

    def on_button_clicked(self, widget):
        n = Notify.Notification.new("Admin", "Hello World !!")
        n.show()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

"""
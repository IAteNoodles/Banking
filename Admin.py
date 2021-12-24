from mysql import connector 
from tkinter import *

from Bank import ROOT, Staff, Supervisor

def welcome(root: Tk):
    welcome_frame=Frame(root)
    welcome_frame.pack()
    Label(welcome_frame, text="Admin ID:").pack()
    ID = Entry(welcome_frame)
    Label(welcome_frame, text="Password:").pack()
    Password = Entry(welcome_frame)
    ID.pack()
    Password.pack()
    def login():
        """
        Handles the login process

        Once both ID and Password are entered, this function checks if an admin exists with the given ID, and if it does,
        then it checks if the hash of the password matches with the hash of the admin in login table. Otherwise it returns
        an Toplevel object with the appropriate error message.
        """
        id = ID.get()
        password = Password.get()
        datasource = database.cursor()
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
        Application_New = LabelFrame(Recovery_Frame, text="New Submission", fg="blue")
        Application_Old = LabelFrame(Recovery_Frame, text="Previous submission", fg="green")
        Application_New.pack(expand=True, fill='both')
        Application_Old.pack(expand=True, fill='both')  
        
        #This will accept details from the admin.
        
        
    recovery_button = Button(welcome_frame, text="Forgot Password", command=Recover)
    recovery_button.pack()
    root.mainloop()
    return admin
    
    
    
if __name__ == "__main__":
    global database
    database = connector.connect(user="python",passwd="Python",database="Bank", host="localhost")
    TK_ROOT = Tk()
    TK_ROOT.title("Admin Panel")
    TK_ROOT.geometry("750x500")
    welcome(TK_ROOT)


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
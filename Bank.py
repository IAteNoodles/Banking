from json import dump as json_dump
from mysql import connector 
import hashlib
class Account:
    def __init__(self):
        pass
class User:
    def __init__(self):
        pass
class Admin:
    """A class that encapsulates the admin type user. 
    Provides root level modification to the database, and other admin features."""
    def __init__(self,ID: str,passwd: str)-> None:
        """
        Accepts the credentials and creates an Admin object after loging in.

        Takes the credentials from the constructor and checks if there is a record with the same ID in the database.
        If no record exists, it returns error message else returns a confirmation message.

        Args:
            ID (str): Identification number of the admin object.
            passwd (str): Password of the admin object.
            host (str): Hostname of the database server.
        """
        self.__VERIFIED = False
        if ID == "ROOT" or ID == "PYTHON_ADMIN":
            self.__PASSWD = hashlib.sha256(passwd.encode()).hexdigest() 
        else:
            self.__PASSWD = passwd
        self.__ID = "841a0cad-4f9a-11ec-b123-90489a3f6f77" if ID == "ROOT" else "cec4d6d5-4f9a-11ec-b123-90489a3f6f77" if ID == "PYTHON_ADMIN" else ID
        self.__CONNECTION = connector.connect(user="python",host="localhost",passwd="Python",database="Bank")
        cursor = self.__CONNECTION.cursor()
        cursor.execute(r"select * from ADMIN_LOGIN WHERE ID = '%s'"%self.__ID)
        hashed_passwd = cursor.fetchone()[1]
        if hashed_passwd == self.__PASSWD:
            print("Successfully logged in!!!")
            self.__VERIFIED = True
        else:
            print("Failed to log in")
            return
        self.__PERMISSIONS: dict()
        # {CREATE_ADMIN: True,
        # CHECK_APPLICATION: True,
        # MODIFY_ADMIN: True,
        # MODIFY_APPLICATION: True
        # ,DELETE_ADMIN: True
        # ,DELETE_APPLICATION: True
        # ,DELETE_USER: True,
        # MODIFY_USER_DATA: True}
        # Permissions alloted to ROOT.
    def change_config(self, **__CONFIG)-> bool:
        pass
    
    def add_admin(self, **__PERMISSIONS)-> None:
        """
        Adds an admin account to the database.

        Creates a new admin account and adds it to the the database.
        ***Note***
        To create a new admin account, an account with higher permissions must be used to create the admin account. i.e. Login with the account with higher previliges to the new account.  

        Args:
            **__PERMISSIONS: Dictionary of the permissions assigned to the admin account.
            Note: This cannot have a higher access level than the current admin object/account.
        """
        cursor = self.__CONNECTION.cursor()
        """cursor.execute("USE Bank")
        cursor.execute("SELECT * FROM ADMIN")
        print(cursor.fetch())"""

    def remove_admin(self):
        pass

    def check_status(self):
        pass
    
    def applications(self):
        pass
    
    def delete_account(self):
        pass
    
    def remove_user(self, ban = False):
        pass
    
Admin(input("Enter ID: "),input("Enter password for admin account (ROOT): "))
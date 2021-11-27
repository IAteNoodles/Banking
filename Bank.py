from json import dump as json_dump
import json
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
    def __init__(self,ID: str,passwd: str,host = "localhost")-> None:
        """
        Accepts the credentials and creates an Admin object after loging in.

        Takes the credentials from the constructor and checks if there is a record with the same ID in the database.
        If no record exists, it returns error message else returns a confirmation message.
        Changes the value of __VERIFIED to True if matched.

        Args:
            ID (str): Identification number of the admin object.
            passwd (str): Password of the admin object.
            host (str): Hostname of the database server.
        """
        self.__VERIFIED = False
        self.__COLUMNS = ('ID',
                          'NAME',
                          'ROOT',
                          'CREATE_ADMIN',
                          'CHECK_TRANSACTION',
                          'CHECK_APPLICATION',
                          'MODIFY_APPLICATION',
                          'DELETE_ADMIN',
                          'DELETE_USER',
                          'MODIFY_USER_DATA',
                          'MODIFY_ADMIN',
                          'DELETE_APPLICATION')
        if ID == "ROOT" or ID == "PYTHON_ADMIN":
            self.__ID = "841a0cad-4f9a-11ec-b123-90489a3f6f77" if ID == "ROOT" else "cec4d6d5-4f9a-11ec-b123-90489a3f6f77"
            self.__PASSWD = hashlib.sha256(passwd.encode()).hexdigest() # Hashes the password without salt
        else:
            self.__PASSWD = passwd
            self.__ID = ID
        self.__CONNECTION = connector.connect(user="python",host=host,passwd="Python",database="Bank")
        cursor = self.__CONNECTION.cursor()
        cursor.execute(r"select * from ADMIN_LOGIN WHERE ID = '%s'"%self.__ID)
        hashed_passwd = cursor.fetchone()[1]
        if hashed_passwd == self.__PASSWD:
            print("Successfully logged in!!!")
            self.__VERIFIED = True
        else:
            print("Failed to log in")
            return
        # Gets all the columns name from the Table.
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'ADMIN'")
        columns = cursor.fetchall()
        self.__PERMISSIONS = dict()
        for name in columns:
            if name[0] == "ID" or name[0] == "NAME": continue
            cursor.execute("SELECT {name} FROM ADMIN WHERE ID = '{ID}'".format(name=name[0],ID=self.__ID))
            self.__PERMISSIONS[name[0]] = cursor.fetchone()[0]
        print("Permissions: {}".format(json.dumps(self.__PERMISSIONS, indent=2).strip("{}").replace('"',"")))
        print(self.__COLUMNS)
        # ----------------------------------------------------Permissions for ROOT-------------------------------------------------
        # {ROOT: True,
        # CREATE_ADMIN: True,
        # CHECK_TRANSACTION: True,
        # CHECK_APPLICATION: True,
        # MODIFY_APPLICATION: True,
        # DELETE_ADMIN: True,
        # DELETE_APPLICATION: True,
        # DELETE_USER: True,
        # MODIFY_USER_DATA: True,
        # MODIFY_ADMIN: True,
        # DELETE_APPLICATION: True,}
        # ----------------------------------------------------Permissions for ROOT-------------------------------------------------
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
        # Default permissions
        self.__PERMISSIONS = {"ROOT": 0,
                              "CREATE_ADMIN": 0,
                              "CHECK_TRANSACTION": 1,
                              "CHECK_APPLICATION": 1,
                              "MODIFY_APPLICATION": 1,
                              "DELETE_ADMIN": 0,
                              "DELETE_USER": 0,
                              "MODIFY_USER_DATA": 1,
                              "MODIFY_ADMIN": 0,
                              "DELETE_APPLICATION": 1}
        print("Please fill the form carefully:")
        name = input("Admin name: ")
        password = input("Admin password: ")
        if input("Do you want to create a new admin account with the default permissions? (Y/N): ") == "Y":
            cursor.execute("SELECT UUID()")
            uuid = cursor.fetchone()
            sql = """INSERT INTO ADMIN{values}
                    VALUES (uuid,{passwd}, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """.format(name=name,passwd=password,values=self.__COLUMNS)
            cursor.execute(sql,self.__PERMISSIONS.values())
            print()
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
    
Admin(input("Enter ID: "),input("Enter password for admin account (ROOT): ")).add_admin()
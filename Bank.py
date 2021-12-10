from json import dump as json_dump
import json
from mysql import connector 
from Crypto.Hash import keccak
import sys
from os.path import exists as file_exists
class Account:
    def __init__(self, *data):
        self.__ID, self.__RATE, self.__MINIMUM_BALANCE = data        
        self.__BALANCE = 0


    def get_balance(self):
        return self.BALANCE

    def withdraw(self, amount):
        try:
            if self.BALANCE-amount < self.__MINIMUM_BALANCE:
                return False
        except NameError:      
            self.BALANCE -= amount
            return True
            
    def deposit(self, amount):
        self.BALANCE += amount
        return True

class Savings(Account):
    def __init__(self, id: str,*data):
        super().__init__(id, 0.04, None)
        del self._Account__MINIMUM_BALANCE
        self.__Times, self.__Limit = data
        
    
    
class Current(Account):
    def __init__(self, id: str):
        super().__init__(id, None, 100000)
        del self._Account__RATE
        print(self.__dict__)
    
class User:
    def __init__(self, uuid: str, passwd: str):
        self.passwd = passwd
        self.id = uuid
        self.__VERIFIED = False
        pass

    def login(self, account_id):
        pass

    def logout(self):
        pass

    def forgetpasswd(self):
        pass

    def get_accounts(self):
        pass

    def freeze_account(self):
        pass

    def change_password(self, new_password):
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
        hash = keccak.new(digest_bits = 512)
        if ID == "ROOT" or ID == "PYTHON_ADMIN":
            self.__ID = "841a0cad-4f9a-11ec-b123-90489a3f6f77" if ID == "ROOT" else "cec4d6d5-4f9a-11ec-b123-90489a3f6f77"
            hash.update(passwd.encode())
            self.__PASSWD = hash.hexdigest() # Hashes the password without salt
        else:
            hash.update(passwd.encode())
            self.__PASSWD = hash.hexdigest() # Hashes the password without salt
            self.__ID = ID
        self.__CONNECTION = connector.connect(user="python",host=host,passwd="Python",database="Bank")
        self.cursor = self.__CONNECTION.cursor()
        self.cursor.execute(r"select * from ADMIN_LOGIN WHERE ID = '%s'"%self.__ID)
        hashed_passwd = self.cursor.fetchone()[1]
        if hashed_passwd == self.__PASSWD:
            print("Successfully logged in!!!")
            self.__VERIFIED = True
        else:
            print("Failed to log in")
            return
        self.__DETAILS = dict()
        for name in self.__COLUMNS:
            # Fetches the permissions from the database and stores it.
            if name[0] == "ID" or name[0] == "NAME": continue
            self.cursor.execute("SELECT {name} FROM ADMIN WHERE ID = '{ID}'".format(name=name,ID=self.__ID))
            self.__DETAILS[name] = self.cursor.fetchone()[0]
        self.__PERMISSIONS = list(self.__DETAILS.values())[2::]
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
    
    def add_admin(self, *__PERMISSIONS)-> bool:
        """
        Adds an admin account to the database.

        Creates a new admin account and adds it to the the database.
        ***Note***
        To create a new admin account, an account with higher permissions must be used to create the admin account. i.e. Login with the account with higher previliges to the new account.  

        Args:
            *__PERMISSIONS: Tuple of the permissions assigned to the admin account.
            If __PERMISSIONS is not specified, then default permissions are used.
            Note: This cannot have a higher access level than the current admin object/account.
        """
        # Default permissions
        PERMISSION = [0, 0, 1, 1, 1, 0, 1, 1, 0, 1] # Default Permissions.
        """{"ROOT": 0,
            "CREATE_ADMIN": 0,
            "CHECK_TRANSACTION": 1,
            "CHECK_APPLICATION": 1,
            "MODIFY_APPLICATION": 1,
            "DELETE_ADMIN": 0,
            "DELETE_USER": 0,
            "MODIFY_USER_DATA": 1,
            "MODIFY_ADMIN": 0,
            "DELETE_APPLICATION": 1}"""
        print("Please fill the form carefully:")
        name = input("Admin name: ")
        password = input("Admin password: ")
        if input("Do you want to create a new admin account with the default permissions? (Y/N): ") == "N":
            print("Permissions are arranged in the following order: ")
            print("'ROOT', 'CREATE_ADMIN', 'CHECK_TRANSACTION', 'CHECK_APPLICATION', 'MODIFY_APPLICATION', 'DELETE_ADMIN', 'DELETE_USER', 'MODIFY_USER_DATA', 'MODIFY_ADMIN', 'DELETE_APPLICATION'")
            sys.stderr.write("Note: It is advised to use a json file to manage permissions, instead of entering the permissions to avoid any errors.")
            print("Enter the path to the json file or the permission_values as list; 0 -> False, 1 -> True.")
            data = eval(input(""))
            # A temporary dictionary to keep track of the permissions.
            try:
                with open(data) as file:
                    __PERMISSIONS_TEST = json.load(file)
                    print("Permissions: {permissions}".format(__PERMISSIONS))
            except TypeError:
                print("Permissions:")
                PERMISSION.clear()
                for permission_name,permission,__PERMISSION in zip(self.__COLUMNS[2::],data,self.__PERMISSIONS):
                    if permission > __PERMISSION:
                        sys.stderr.write("You do not have permission to give access to {permission}".format(permission=permission_name))
                        return
                    PERMISSION.append(permission)
        self.cursor.execute("SELECT UUID()")
        uuid = self.cursor.fetchone()[0]
        hash = keccak.new(digest_bits = 512)
        hash.update(password.encode())
        hashed_passwd = hash.hexdigest()
        self.cursor.execute("INSERT INTO ADMIN_LOGIN (ID,HASH) VALUES (%s,%s)",(uuid,hashed_passwd))
        self.__CONNECTION.commit()
        # Don't edit this line. Take some time and carefully read it and understand what this does.
        sql="INSERT INTO ADMIN {columns} VALUES ('{UUID}','{name}',%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(columns=str(self.__COLUMNS).replace("'",""),UUID=uuid,name=name)
        # Fires up an request to create a new admin account with the default permissions and the given name.
        self.cursor.execute(sql,PERMISSION)
        self.__CONNECTION.commit()
        print("ID for {user} is {uuid}".format(user=name,uuid=uuid))
    def remove_admin(self, *temp):
        admin_id,reason = temp
        self.cursor.execute("SELECT * FROM ADMIN WHERE ID='%s'"%admin_id)
        admin_data = self.cursor.fetchone()
        admin_perms = admin_data[2::]
        for permissions in zip(admin_perms,self.__PERMISSIONS):
            if permissions[0]>permissions[1]:
                sys.stderr.write("Cannot remove admin account because of lower previliges.")
                return False
        self.cursor.execute("DELETE FROM ADMIN WHERE ID='%s'"%admin_id)
        self.__CONNECTION.commit()       
    def check_status(self,application_id)-> None:
        """Checks the status of application of the given id
        Args:
            application_id(str): Application ID of the application.
        """
        self.cursor = self.__CONNECTION.cursor()
        self.cursor.execute("SELECT * FROM APPLICATION WHERE APPLICATION_ID= '%s'"%application_id)
        data = self.cursor.fetchone()[1::]
        print("Date of creation: ", data[0])
        print("Date of last modification: ", data[1])
        print("Status: ", "Pending" if data[2] is None else "Rejected" if data[2]==0 else "Verified")
        print("Remarks: ", data[3])
        action = input("Action: ")
        if action == "delete":
            self.cursor.execute("DELETE FROM APPLICATION WHERE APPLICATION_ID = '%s'"%application_id)
        elif action == "update":
            self.cursor.execute("UPDATE APPLICATION SET VERIFIED = %r WHERE APPLICATION_ID = '%s'"%((bool(input("Accept(1)/Reject(0)"))),application_id))
        elif action == "remarks":
            self.cursor.execute("UPDATE APPLICATION SET REMARKS = '%s' WHERE APPLICATION_ID = '%s'"%(input("Remarks: "),application_id))
        else:
            print("Unknown action")
        self.__CONNECTION.commit()
        
    def applications(self):
        pass
    
    def delete_account(self):
        pass
    
    def remove_user(self, ban = False):
        
        pass
    
Admin(input("Enter ID: "),input("Enter password for admin account (ROOT): ")).remove_admin("841a0cad-4f9a-11ec-b123-90489a3f6f77","Testing")
#Savings("123",52,60)

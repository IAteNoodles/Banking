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
    def __init__(self, id: str, *data):
        super().__init__(id, 0.04, None)
        del self._Account__MINIMUM_BALANCE
        self.__Times, self.__Limit = data


class Current(Account):
    def __init__(self, id: str):
        super().__init__(id, None, 100000)
        del self._Account__RATE
        print(self.__dict__)

user_connection = connector.connect(name="user_bank", host="localhost", password="USER@BANK").cursor()
class User:
    def __init__(self, uuid: str, passwd: str):
        self.passwd = passwd
        self.id = uuid
        self.__VERIFIED = False
        pass

    def login_user(self, password):
        user_connection.execute("SELECT HASH FROM USER_LOGIN WHERE USER_ID = {ID}".format(ID=self.id))
        if hash(password) == user_connection.fetchone():
            self.__VERIFIED = True
    
    def get_accounts(self):
        if not self.__VERIFIED:
            return "Please login and verify yourself first."
        user_connection.execute("SELECT ID FROM ACCOUNT WHERE USER_ID = %s" % self.id)
        return user_connection.fetchall()

    def logout(self):
        self.__VERIFIED = False
        pass

    def forgetpasswd(self, method, token):
        
        pass

    def freeze_account(self):
        pass

    def change_password(self, new_password):
        if not self.__VERIFIED:
            return "Please login before changing password."
        user_connection.execute("") #Update password.
        pass


class Staff:
    """A class that encapsulates the admin type user. 
    Provides root level modification to the database, and other admin features."""

    def __init__(self, ID: str, passwd: str, host="localhost") -> None:
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
        self.__COLUMNS = ('ADMIN_ID',
                          'TYPE',
                          'ROOT',
                          'CREATE_ADMIN',
                          'CHECK_TRANSACTION',
                          'CHECK_APPLICATION',
                          'MODIFY_APPLICATION',
                          'DELETE_ADMIN',
                          'DELETE_USER',
                          'MODIFY_USER_DATA',
                          'MODIFY_ADMIN',
                          'DELETE_APPLICATION',
                          'UNIQUE_ID')
        
        if ID == "ROOT" or ID == "PYTHON_ADMIN":
            self.__ID = "841a0cad-4f9a-11ec-b123-90489a3f6f77" if ID == "ROOT" else "cec4d6d5-4f9a-11ec-b123-90489a3f6f77"
        else:
            self.__ID = ID
        self.__PASSWD = hash(passwd)
        self.__CONNECTION = connector.connect(
            user="python", host=host, passwd="Python", database="Bank")
        self.cursor = self.__CONNECTION.cursor()
        self.cursor.execute(
            r"select * from ADMIN_LOGIN WHERE ID = '%s'" % self.__ID)
        hashed_passwd = self.cursor.fetchone()[1]
        if hashed_passwd == self.__PASSWD:
            print("Successfully logged in!!!")
            self.__VERIFIED = True
        else:
            print("Failed to log in")
            return "Invalid Credentials!!!"
        self.__DETAILS = dict()
        # Fetches the permissions from the database and stores it.
        print(self.__ID)
        self.cursor.execute(
            "SELECT * FROM ADMIN WHERE ADMIN_ID = '{ID}'".format(ID=self.__ID))
        self.__DETAILS = self.cursor.fetchone()
        print(self.__DETAILS)
        #self.__PERMISSIONS = list(self.__DETAILS.values())[2::]
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

    def check_status(self, application_id) -> str:
        """Checks the status of application of the given id
        Args:
            application_id(str): Application ID of the application.
        """
        self.cursor = self.__CONNECTION.cursor()
        self.cursor.execute(
            "SELECT * FROM APPLICATION WHERE APPLICATION_ID= '%s'" % application_id)
        data = self.cursor.fetchone()[1::]
        print("Date of creation: ", data[0])
        print("Date of last modification: ", data[1])
        print(
            "Status: ", "Pending" if data[2] is None else "Rejected" if data[2] == 0 else "Verified")
        print("Remarks: ", data[3])
        action = input("Action: ")
        if action == "delete":
            self.cursor.execute(
                "DELETE FROM APPLICATION WHERE APPLICATION_ID = '%s'" % application_id)
        elif action == "update":
            self.cursor.execute("UPDATE APPLICATION SET VERIFIED = %r WHERE APPLICATION_ID = '%s'" % (
                (bool(input("Accept(1)/Reject(0)"))), application_id))
        elif action == "remarks":
            self.cursor.execute("UPDATE APPLICATION SET REMARKS = '%s' WHERE APPLICATION_ID = '%s'" % (
                input("Remarks: "), application_id))
        else:
            print("Unknown action")
        self.__CONNECTION.commit()

    def create_applications(self, details) -> str:
        pass

    def delete_account(self, account_id) -> str:
        pass

    def remove_user(self, **details) -> str:

        pass


class Supervisor(Staff):
    def __init__(self, ID: str, passwd: str) -> None:
        super().__init__(ID, passwd)

    def change_config(self, **__CONFIG) -> bool:
        pass

    def add_staff(self, id__, password, staff_type=None) -> bool:
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
        if staff_type is None:
            staff_type = "STAFF"
            PERMISSION = [0, 0, 1, 1, 1, 0, 1, 1, 0, 1]  # Default Permissions.
        elif staff_type is "SUPERVISOR":
            PERMISSION = [0].extend([1]*9)
        else:
            PERMISSION = [1]*10
        self.cursor.execute("SELECT UUID()")
        uuid = self.cursor.fetchone()[0]
        hash = keccak.new(digest_bits=512)
        hash.update(password.encode())
        hashed_passwd = hash.hexdigest()
        self.cursor.execute(
            "INSERT INTO ADMIN_LOGIN (ID,HASH) VALUES (%s,%s)", (uuid, hashed_passwd))
        # Don't edit this line. Take some time and carefully read it and understand what this does.
        sql = "INSERT INTO ADMIN {columns} VALUES ('{UUID}','{staff_type}',%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '{id_}')".format(
            columns=str(self._Staff__COLUMNS).replace("'", ""), UUID=uuid, staff_type=staff_type, id_=id__)
        # Fires up an request to create a new admin account with the default permissions and the given name.
        self.cursor.execute(sql, PERMISSION)
        self._Staff__CONNECTION.commit()
        print("ID is {uuid}".format(uuid=uuid))


class ROOT(Supervisor):
    def __init__(self, ID: str, passwd: str) -> None:
        super().__init__(ID, passwd)
        print(self.__dict__.keys())

    def remove_admin(self, *misc):
        admin_id, reason = misc
        self.cursor.execute("SELECT * FROM ADMIN WHERE ID='%s'" % admin_id)
        admin_data = self.cursor.fetchone()
        admin_perms = admin_data[2::]
        for permissions in zip(admin_perms, self.__PERMISSIONS):
            if permissions[0] > permissions[1]:
                sys.stderr.write(
                    "Cannot remove admin account because of lower previliges.")
                return False
        self.cursor.execute("DELETE FROM ADMIN WHERE ID='%s'" % admin_id)
        self._Staff__CONNECTION.commit()

@staticmethod
def hash(passwd: str):
    hash = keccak.new(digest_bits=512)
    hash.update(passwd.encode())
    return hash.hexdigest()  # Hashes the password without salt

ROOT(input("ID: "), input("Password: ")).add_staff("1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2","123")
#Staff(input("Enter ID: "), input("Enter password for admin account (ROOT): ")).remove_admin("841a0cad-4f9a-11ec-b123-90489a3f6f77", "Testing")
# Savings("123",52,60)

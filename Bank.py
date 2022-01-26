from json import dump as json_dump
from typing import Final, List, final
import mariadb
from Crypto.Hash import keccak
account_source = mariadb.connect(user="Account", password="Account@Bank", host="localhost", database="Bank")
account_connection = account_source.cursor()
class Account:
    def __init__(self, id: str):
        self.__ID = id
        account_connection.execute("SELECT BALANACE FROM ACCOUNT WHERE ID = %s" % id)
        self.__BALANCE = account_connection.fetchone()[0]
        
    def get_balance(self):
        return self.__BALANCE
        
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
    
    def fetch_transaction(self, limit = 50):
        '''
        Acceps the limit of transactions and returns a list of transactions.
        The default limit is 50
        
        Args:
            limit (int): the maximum number of transactions
        
        Returns:
            A list of transactions with the following attributes.
            Transaction ID: Transaction ID, this can be used to identify transactions.
            By: Sender.
            To: Recipient.
            Amount: Money involved in the transaction.
            Transaction Time: Time of the transaction.
        '''
        account_connection.execute("SELECT * FROM TRANSACTION WHERE BY = '{acc_id}' OR TO = '{acc_id}'".format(acc_id = self.__ID))
        transactions = account_connection.fetch(limit)
        return transactions
    
    def change_password(self, new_password):
        pass


class Savings(Account):
    def __init__(self, id:str, limit=100):
        super().__init__(id)
        self.LIMIT = limit
        self.__Limit = limit


class Current(Account):
    def __init__(self, id: str, min_balance=1000000):
        super().__init__(id)
        self.__MINIMUM_BALANCE = min_balance
        print(self.__dict__)

user_source = mariadb.connect(user="User", host="localhost", password="User@Bank")
user_connection = user_source.cursor()

class User:
    def __init__(self, uuid: str, passwd: str):
        self.passwd = passwd
        self.id = uuid
        self.__VERIFIED = False
        user_connection.execute("SELECT SECURITY_NUMBER FROM PEOPLE WHERE UNIQUE_ID = {ID}".format(ID=self.id))
        if hash(passwd) == user_connection.fetchone():
            self.__VERIFIED = True

    def get_accounts(self):
        if not self.__VERIFIED:
            return "Please login and verify yourself first."
        user_connection.execute("SELECT ID FROM ACCOUNT WHERE USER_ID = %s" % self.id)
        return user_connection.fetchall()

    def login_account(self, id: str, password: str):
        """Inputs account id and password and checks them against the database
        Args:
            id (str): Account ID
            password (str): Password for the given account."""    
        if not self.__VERIFIED:
            return "Please login and verify yourself first."
        user_connection.execute("SELECT HASH FROM ACCOUNT_LOGIN WHERE ACCOUNT_ID = %s" % id)
        if hash(password) == user_connection.fetchone():
            user_connection.execute("SELECT TYPE FROM ACCOUNT WHERE ID = %s" % id)
            account_type = user_connection.fetchone()[0]
            if account_type == "Savings":
                account = Savings(id)
            else:
                account = Current(id)
            return account
        
    def logout(self):
        self.__VERIFIED = False
        pass
    
    def forgetpasswd(self, id):
        import secrets
        from datetime import datetime
        token = secrets.token_urlsafe()
        user_connection.execute("INSERT INTO USER_LOGIN (TOKEN) WHERE ID = %s" %id)
        SQL = """UPDATE USER_LOGIN
        SET TOKEN = ''
        WHERE timestamp &gt; DATE_SUB(NOW(), INTERVAL 10 MINUTE)"""
        user_connection.execute(SQL)
        
    def freeze_account(self):
        pass

    def change_password(self, new_password):
        if not self.__VERIFIED:
            return "Please login before changing password."
        user_connection.execute("UPDATE USER_LOGIN SET HASH = %s WHERE ID = %s" % hash(new_password),self.__ID) #Update password.


class Staff:
    """
    A class that encapsulates the admin type user. 
    Provides root level modification to the database, and other admin features.
    """

    def __init__(self, ID: str, passwd: str, nick=False,host="localhost"):
        """
        Accepts the credentials and creates an Admin object after loging in.

        Takes the credentials from the constructor and checks if there is a record with the same ID in the database.
        If no record exists, it returns error message else returns a confirmation message.\n
        Changes the value of __VERIFIED to True if matched, else updates the __ERROR with the appropriate error message.
        
        Args:
            ID (str): Identification number of the admin object. (Optional: Can be used as a nickname to ease authentication)
            passwd (str): Password of the admin object.
            nick (bool): Tells the function to treat the ID as a nickname instead. (Default is False)
            host (str): Hostname of the database server.
        
        """
        self.__ERROR = {"Message": None,
                        "Nickname": nick}
        
        self.__VERIFIED = False
        self.__COLUMNS = ('ID',
                    'Admin ID',
                    'Type',
                    'Nickname')
                          
        TYPE_DATA = {"Staff":1,
                     "Supervisor":2,
                     "Root":3} #This defines the hierarchy of each type of admin.
        
        verification_method = "Nickname" if nick else "ID"

        self.__PASSWD = hash(passwd)
        
        # We connect to the database with the set password.
        self.__CONNECTION = mariadb.connect(user="Admin", host=host, passwd="Admin@Bank", database="Bank")
        self.cursor = self.__CONNECTION.cursor()
        
        # We look for a match in the records and fetch the corresponding hashed_passwd.
        self.cursor.execute("SELECT * from ADMIN_LOGIN WHERE %s = '%s'" % (verification_method,self.__ID))
        hashed_passwd = self.cursor.fetchone()[1]
        if hashed_passwd is None:
            self.__ERROR["Message"] = "No record found."
        # We check if the hashed_passwd matches with the hash of the given password.
        if hashed_passwd == self.__PASSWD:
            self.__VERIFIED = True
        else:
            self.__ERROR["Message"] = "Invalid credentials"

        

    def track_application(self, application_id):
        """
        Tracks the application with the given application  

        Checks if the application exists in the database and returns the latest details according to the database.

        Args:
            application_id (str): Application ID 

        Returns:
            list: List of the details of the application.
                The list includes these details in the following format:
                Date of creation: Datetime
                Date of last modification: Datatime
                Status of the application : Pending/Rejected/Verified
                Remarks: Additional Information if present. May contain the reason for rejection,
                or comments for the verifiers.
        """
        #TODO: Implement this with the changed table.
        self.cursor.execute(
            "SELECT * FROM APPLICATION WHERE APPLICATION_ID= '%s'" % application_id)
        temp = self.cursor.fetchone()
        if temp is None:
            return [
                "Date of creation: None",
                "Date of last modification: None",
                "Status: Unknown",
                "Remarks: No records found for the given application id."
            ]
        data = temp[1::]
        res = list()
        res.append("Date of creation: {creationdate}".format(creationdate=data[0]))
        res.append("Date of last modification: {lastdate}".format(lastdate=data[1]))
        status = "Pending" if data[2] is None else ("Rejected" if data[2] == 0 else "Verified")
        res.append("Status: {status}".format(status=status))
        remarks = "None" if data[3] is None else data[3]
        res.append("Remarks: {remarks}".format(remarks=remarks))
        return res
    
    def modify_application(self, application_id):
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

    def create_applications(self, details):
        pass

    def delete_account(self, account_id):
        pass

    def remove_user(self, **details):

        pass


class Supervisor(Staff):
    def __init__(self, ID: str, passwd: str):
        super().__init__(ID, passwd)
        self._Staff__TYPE = "SUPERVISOR"
        self.ISSUPERVISOR: Final = True
        
    def change_config(self, **__CONFIG):
        pass

    def add_staff(self, id__, password, staff_type=None):
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
        elif staff_type == "SUPERVISOR":
            PERMISSION = [0].extend([1]*9)
        else:
            PERMISSION = [1]*10
        self.cursor.execute("SELECT UUID()")
        uuid = self.cursor.fetchone()[0]
        hash = keccak.new(digest_bits=512)
        hash.update(password.encode())
        hashed_passwd = hash.hexdigest()
        self.cursor.execute("INSERT INTO ADMIN_LOGIN (ID,HASH) VALUES (%s,%s)", (uuid, hashed_passwd))
        # Don't edit this line. Take some time and carefully read it and understand what this does.
        sql = "INSERT INTO ADMIN {columns} VALUES ('{UUID}','{staff_type}',%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '{id_}')".format(
            columns=str(self._Staff__COLUMNS).replace("'", ""), UUID=uuid, staff_type=staff_type, id_=id__)
        # Fires up an request to create a new admin account with the default permissions and the given name.
        self.cursor.execute(sql, PERMISSION)
        self._Staff__CONNECTION.commit()
        print("ID is {uuid}".format(uuid=uuid))
    
    def modify_admin():
        pass


class ROOT(Supervisor):
    def __init__(self, ID: str, passwd: str):
        super().__init__(ID, passwd)
        self._Staff__TYPE = "ROOT"
        self.ISROOT: Final = True
        print(self.__dict__.keys())

    def remove_admin(self, *misc):
        admin_id, reason = misc
        self.cursor.execute("DELETE FROM ADMIN WHERE ID='%s'" % admin_id)
        self.cursor.execute("INSERT INTO LOGS (COMMAND, INFO, TRIGGER_TIME) VALUES ('DELETED ADMIN {id}, NOW(), {info}".format(id=admin_id, info=reason))
        self._Staff__CONNECTION.commit()


def hash(passwd: str):
    hash = keccak.new(digest_bits=512)
    hash.update(passwd.encode())
    return hash.hexdigest()  # Hashes the password without salt

#ROOT(input("ID: "), input("Password: ")).create_applications
print(hash("Abhijit"))
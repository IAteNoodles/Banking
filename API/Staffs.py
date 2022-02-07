#This class is used to access the staff apis.
#This class is filled with only the base apis. Other features maybe added in future.
import mariadb
connection = mariadb.connect(user="Admin", passwd="Admin@Bank", database="Banking")
class Staff:
    
    def __init__(self, staff_id, password):
        from Hashing import sha3
        password = sha3(password)
        connection.execute("SELECT * FROM Staff WHERE ID = %s AND Password = %s", (staff_id, password))
        #Checks if there is a user with the given ID and password.
        if connection.fetchone() is None:
            return "Username or password is incorrect"
        
        self.username = staff_id
        self.password = password
        self.type = 0
        #Fetches the staff type from the database.
        connection.execute("SELECT `Type` FROM Staff WHERE ID = %s", (staff_id))
        
    def add_user(self, user_id, hashed_passwd):
        """
        Inserts a user into the user table with the hashed password.
        """
        connection.execute("INSERT INTO User (ID, Password) VALUES (%s, %s)", (user_id, hashed_passwd))
        connection.commit()
        
    def add_account(self, account_id, user_id):
        """
        
        Inserts an account into the account table and links it to the user.
        
        Args:
            account_id: ID of the account
            user_id: ID of the user (Owner of the account)
        """
        connection.execute("INSERT INTO Accounts (ID, User_ID) VALUES (%s, %s)", (account_id, user_id))
        connection.commit()
        

        
class Manager(Staff):
    def __init__(self, user_id, password):
        super(Manager, self).__init__(user_id, password)
        self.type = 1
        
    def add_staff(self, staff_id, hashed_passwd, staff_type):
        """
        Inserts a staff into the staff table with the hashed password.
        
        Args:
            staff_id: ID of the staff.
            hashed_passwd: Hash of the staff's password.
            staff_type: Type of the staff (Admin: 2 | Manager:1 | Staff:0)
        """
        if staff_type > self.type:
            return "You are not authorized to add this staff"
        
        connection.execute("INSERT INTO Staff (ID, Password, `Type`) VALUES (%s, %s, %s)", (staff_id, hashed_passwd, staff_type))
        connection.commit()
        
class Admin(Manager):
    def __init__(self, user_id, password):
        super(Admin, self).__init__(user_id, password)
        self.type = 2
        
    def remove_staff(self, staff_id):
        """
        Removes a staff from the staff table.
        
        Args:
            staff_id: ID of the staff.
        """
        connection.execute("DELETE FROM staff WHERE ID = %s", (staff_id))
        connection.commit()